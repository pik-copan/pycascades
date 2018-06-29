from scipy.integrate import ode
import numpy as np

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
        
    def _iterate(self,t_end,t_step):
        """Private iterate method for constant parameter"""
        """
        t_arr = np.arange(self.times[-1],t_end,t_step)
        x = odeint(self.net.system,self.states[-1],t_arr)
        self.net.set_state(x[-1])
        self.states.append(self.net.get_state())
        self.times.append(t_end)
        """
    def iterate(self,te,end,step,dpdt,opt='time'):
        """Iterate system while changing control parameter. The Control 
        Parameter should change slowly with respect to the dynamics 
        to the system, e.g. dpdt (dpar/dt) should be much smaller than one. 
        Step size and break condition can be provided as time or 
        parameter values (opt='par'). Time values are the default behaviour"""
                
        if opt == 'par':
            par_step = step
            par_tstep = par_step/dpdt
            t_step = 0.01*par_tstep
            t_end = end/dpdt
        elif opt == 'time':
            t_end = end
            t_step = step
            par_tstep = 100*t_step
            par_step = dpdt*par_tstep
        else:
            raise ValueError("Unrecognized option "+opt)
            
        self.pars.append(te.c)
        for t in np.arange(self.times[-1],t_end,par_tstep):
            t_stop = t + par_tstep
            self._iterate(t_stop,t_step)
            self.pars.append(te.c)
            te.c += par_step

    def equilibrate(self,tolerance,t_step,realtime_break=None):
        """Iterate system until it is in equilibrium.
        TODO: Add stability checkup of fixpoint (with jacobian)"""
        r = ode(self.net.f_prime).set_integrator('vode', method='bdf')
        r.set_initial_value(self.net.get_state(),self.times[-1])
        break_flag = False
        while r.successful() and not break_flag:
            r.integrate(r.t+t_step)
            self.net.set_state(r.y)
            self.states.append(r.y)
            self.times.append(r.t)
            fix_point = np.less(np.abs(self.net.f_prime(r.t,r.y))
                                ,tolerance*np.ones((1
                                ,self.net.number_of_nodes())))
            
            if fix_point.all():
                break_flag = True