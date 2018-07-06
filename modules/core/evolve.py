from scipy.integrate import ode
import numpy as np
import time

"""evolve module"""

class net_evolve():
    """net_evolve class
    Provides methods to solve the system and vary system parameters.
    """
    def __init__(self,network):
        """Constructor"""
        self.net = network
        self.states = [self.net.get_state()]
        self.times = [0]
        par_list = []
        for id in self.net.nodes():
            par_list.append(self.net.node[id]['data'].c)
        self.pars = [par_list]
        self.r = ode(self.net.f_prime
                     ,self.net.jac).set_integrator('vode', method='adams')
        self.r.set_initial_value(self.net.get_state(),self.times[-1])
        
    def save_state(self):
        self.net.set_state(self.r.y)
        self.states.append(self.r.y)
        self.times.append(self.r.t)
        
        par_list = []
        for id in self.net.nodes():
            par_list.append(self.net.node[id]['data'].c)
        self.pars.append(par_list)
        
    def integrate(self,t_step,t_end):
        """Manually integrate to t_end"""
        while self.r.successful() and self.r.t<t_end:
            self.r.integrate(self.r.t+t_step)
            self.save_state()
            
    def tip(self,tip_id_list,tolerance,t_step,realtime_break=None):
        """Trigger tipping by increasing normal parameter 
        of the elements with id from tip_id_list"""
        self.net.adjust_normal_pars(0)
        continue_flag = True
        while continue_flag:
            try:
                self.equilibrate(tolerance,t_step,realtime_break)
            except NoEquilibrium:
                print("No equilibrium found " \
                      "in "+str(realtime_break)+" realtime seconds."\
                      " Increase tolerance or breaktime.")
                break
            for id in tip_id_list:
                self.net.node[id]['data'].c+=0.01*t_step
                print(self.net.node[id]['data'].c)
            continue_flag=False
            for id in tip_id_list:
                if not self.net.node[id]['data'].tipped:
                    continue_flag=True
                       
    def equilibrate(self,tolerance,t_step,realtime_break=None):
        """Iterate system until it is in equilibrium. 
        After every iteration it is checked if the system is in a stable
        equilibrium"""
        t0 = time.process_time()
        while self.r.successful():
            self.r.integrate(self.r.t+t_step)
            self.save_state()
            
            if self.check_fixed_point(tolerance):
                if self.check_stability():
                    break
                    
            if realtime_break and (time.process_time() - t0) >= realtime_break:
                raise NoEquilibrium(
                        "No equilibrium found " \
                        "in "+str(realtime_break)+" realtime seconds."\
                        " Increase tolerance or breaktime."
                        )
                
    def check_fixed_point(self,tolerance):
        """Check if the system is in an equilibrium state, e.g. if the 
        absolute value of all elements of f_prime is less than tolerance. 
        If True the state can be considered as close to a fixed point"""
        fix = np.less(np.abs(self.net.f_prime(self.r.t,self.r.y))
                         ,tolerance*np.ones((1
                         ,self.net.number_of_nodes())))
        if fix.all():
            return True
        else:
            return False
        
    def check_stability(self):
        """Check stability of current system state by calculating the 
        eigenvalues of the jacobian (all eigenvalues < 0 => stable)."""
        val, vec = np.linalg.eig(self.net.jac(self.r.t,self.r.y))
        stable = np.less(val,np.zeros((1,self.net.number_of_nodes())))
        if stable.all():
            return True
        else:
            return False
                
class NoEquilibrium(Exception):
    pass