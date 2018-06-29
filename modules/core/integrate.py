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
        self.pars = []
        self.r = ode(self.net.f_prime).set_integrator('vode', method='bdf')
        self.r.set_initial_value(self.net.get_state(),self.times[-1])
        
    def tip(self,tip_id_list,tolerance,t_step,realtime_break=None):
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
        TODO: Add stability checkup of fixpoint (with jacobian)"""
        break_flag = False
        t0 = time.process_time()
        while self.r.successful() and not break_flag:
            self.r.integrate(self.r.t+t_step)
            self.net.set_state(self.r.y)
            self.states.append(self.r.y)
            self.times.append(self.r.t)
            fix_point = np.less(np.abs(self.net.f_prime(self.r.t,self.r.y))
                                ,tolerance*np.ones((1
                                ,self.net.number_of_nodes())))
            
            if fix_point.all():
                break_flag = True
            if realtime_break and (time.process_time() - t0) >= realtime_break:
                raise Exception("No equilibrium found " \
                                "in "+str(realtime_break)+" realtime seconds."\
                                " Increase tolerance or breaktime.")