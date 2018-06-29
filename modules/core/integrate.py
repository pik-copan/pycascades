from scipy.integrate import ode
import numpy as np
import time

"""integrate module"""

class solver():
    """solver class
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
                     ,self.net.jac).set_integrator('vode', method='bdf')
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
        continue_flag = True
        while continue_flag:
            self.equilibrate(tolerance,t_step,realtime_break)
            for id in tip_id_list:
                self.net.node[id]['data'].c+=0.01*t_step
            continue_flag=False
            for id in tip_id_list:
                if not self.net.node[id]['data'].tipped:
                    continue_flag=True
                       
    def equilibrate(self,tolerance,t_step,realtime_break=None):
        """Iterate system until it is in equilibrium. 
        After every iteration it is checked wether the absolute value 
        of all elements of f_prime is less than tolerance. 
        If True the state can be considered as close to a fixed point 
        and the eigenvalues of the jacobian are calculated to verify
        the stability of the fixed point (all eigenvalues < 0 => stable)."""
        break_flag = False
        t0 = time.process_time()
        while self.r.successful() and not break_flag:
            self.r.integrate(self.r.t+t_step)
            self.save_state()
            
            fix = np.less(np.abs(self.net.f_prime(self.r.t,self.r.y))
                         ,tolerance*np.ones((1
                         ,self.net.number_of_nodes())))
            
            if fix.all():
                val, vec = np.linalg.eig(self.net.jac(self.r.t,self.r.y))
                stable = np.less(val,np.zeros((1,self.net.number_of_nodes())))
                if stable.all():
                    break_flag = True
                    
            if realtime_break and (time.process_time() - t0) >= realtime_break:
                raise Exception("No equilibrium found " \
                                "in "+str(realtime_break)+" realtime seconds."\
                                " Increase tolerance or breaktime.")