from scipy.integrate import odeint
import numpy as np

"""integrate module"""

class solver():
    """solver class
    Provides methods to solve the system and vary system parameters.
    """
    def __init__(self,network):
        """Constructor"""
        self.net = network
            
    def _iterate(self,t_end,t_step):
        """Private iterate method for constant parameter"""
        self.states = [self.net.get_state()]
        self.times = [0]
        self.pars = []
        
        t_arr = np.arange(self.times[-1],t_end,t_step)
        x = odeint(self.net.system,self.states[-1],t_arr)
        self.net.set_state(x[-1])
        self.states.append(self.net.get_state())
        self.times.append(t_end)
        
    def iterate(self,te,end,step,dpdt,opt='time'):
        """Iterate system while changing control parameter. The Control 
        Parameter should change slowly with respect to the dynamics 
        to the system, e.g. dpdt (dpar/dt) should be much smaller than one. 
        Step size and break condition can be provided as time or 
        parameter values (opt='par'). Time values are the default behaviour"""
        self.states = [self.net.get_state()]
        self.times = [0]
        self.pars = []
        
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
        
        
        
        
    