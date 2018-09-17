from scipy.integrate import ode
import numpy as np
from operator import xor
import time

"""evolve module"""
class NoEquilibrium(Exception):
    pass

class evolve():
    def __init__( self , tipping_network , initial_state , bif_par_arr , bif_par_func ):
        # Initialize solver
        self.dxdt_vec = tipping_network.get_dxdt_vec()
        self.jacobian = tipping_network.get_jac()
        self.r = ode(self.f,self.jac).set_integrator('vode', method='adams')
        self.bif_par_func = bif_par_func
        self.bif_par_arr = bif_par_arr
        
        # Initialize state
        self.r.set_initial_value(initial_state,0)
        self.times = []
        self.pars = []
        self.states = []
        self.save_state()
        self.init_tip_state = self.get_tip_state()
        
    def f(self,t,x):
        f = []
        for idx in range(0,len(x)):
            dxdt = self.dxdt_vec[idx][0].__call__( 
                        self.bif_par_func.__call__(t,len(x))[idx] 
                        + self.bif_par_arr[idx], x[idx] )
            
            for cpl_id in range(1,len(self.dxdt_vec[idx])):
                dxdt += self.dxdt_vec[idx][cpl_id][0].__call__( 
                             x[self.dxdt_vec[idx][cpl_id][1]] , x[idx] )
            f.append(dxdt)
        return f
    
    def jac(self,t,x):
        jac = []
        for row_idx in range(0,len(x)):
            jac_row = []
            for col_idx in range(0,len(x)):
                if row_idx == col_idx:
                    jac_row.append( self.jacobian[row_idx][col_idx].__call__(
                        self.bif_par_func.__call__(t,len(x))[row_idx] 
                        + self.bif_par_arr[row_idx] , x[row_idx]))
                else:
                    jac_row.append( self.jacobian[row_idx][col_idx].__call__( 
                                    x[col_idx] , x[row_idx] ) )
            jac.append(jac_row)
        return jac
                            
    def integrate(self,t_step,t_end):
        """Manually integrate to t_end"""
        while self.r.successful() and self.r.t<t_end:
            self.r.integrate(self.r.t+t_step)
            self.save_state()
            
    def save_state(self):
        """Save current state"""
        self.times.append(self.r.t)
        self.states.append(self.r.y)
        self.pars.append(self.bif_par_func.__call__(self.r.t,len(self.r.y)) + 
                         self.bif_par_arr )
        
    def get_tip_state(self):
        """Calculate binary array of tip states"""
        return np.array(self.states[-1]) > 0
    
    def number_tipped(self):
        """Return number of tipped elements"""
        #N = len(max(nx.weakly_connected_components(self.net),key=len))
        tip_list = list(map(xor,self.init_tip_state,self.get_tip_state()))
        return sum(tip_list)
        
    def equilibrate(self,tolerance,t_step,save,realtime_break=None):
        """Iterate system until it is in equilibrium. 
        After every iteration it is checked if the system is in a stable
        equilibrium"""
        t0 = time.process_time()
        while self.r.successful():
            self.r.integrate(self.r.t+t_step)
            if save:
                self.save_state()
            
            if self.is_fixed_point(tolerance):
                break
                    
            if realtime_break and (time.process_time() - t0) >= realtime_break:
                raise NoEquilibrium(
                        "No equilibrium found " \
                        "in "+str(realtime_break)+" realtime seconds."\
                        " Increase tolerance or breaktime."
                        )
                
    def is_fixed_point(self,tolerance):
        """Check if the system is in an equilibrium state, e.g. if the 
        absolute value of all elements of f_prime is less than tolerance. 
        If True the state can be considered as close to a fixed point"""
        fix = np.less(np.abs(self.f(self.r.t,self.r.y))
                     ,tolerance*np.ones((1
                     ,len(self.pars[-1]))))
        if fix.all():
            return True
        else:
            return False
    
    def is_stable(self):
        """Check stability of current system state by calculating the 
        eigenvalues of the jacobian (all eigenvalues < 0 => stable)."""
        val, vec = np.linalg.eig(self.jac(self.r.t,self.r.y))
        stable = np.less(val,np.zeros((1,len(self.pars[-1]))))
        if stable.all():
            return True
        else:
            return False