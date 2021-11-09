from scipy.integrate import odeint
import numpy as np
import time
import sdeint
from scipy.stats import levy, cauchy

"""evolve module"""
class NoEquilibrium(Exception):
    pass

def itoint(f, G, y0, tspan, noise = "normal"):
    """ Numerically integrate the Ito equation  dy = f(y,t)dt + G(y,t)dW
    where y is the d-dimensional state vector, f is a vector-valued function,
    G is an d x m matrix-valued function giving the noise coefficients and
    dW(t) = (dW_1, dW_2, ... dW_m) is a vector of independent Wiener increments
    Args:
      f: callable(y,t) returning a numpy array of shape (d,)
         Vector-valued function to define the deterministic part of the system
      G: callable(y,t) returning a numpy array of shape (d,m)
         Matrix-valued function to define the noise coefficients of the system
      y0: array of shape (d,) giving the initial state vector y(t==0)
      tspan (array): The sequence of time points for which to solve for y.
        These must be equally spaced, e.g. np.arange(0,10,0.005)
        tspan[0] is the intial time corresponding to the initial state y0.
    Returns:
      y: array, with shape (len(tspan), len(y0))
         With the initial value y0 in the first row
    Raises:
      SDEValueError
    """
    # In future versions we can automatically choose here the most suitable
    # Ito algorithm based on properties of the system and noise.
    (d, m, f, G, y0, tspan, __, __) = sdeint.integrate._check_args(f, G, y0, tspan, None, None)
    N = len(tspan)
    h = (tspan[N-1] - tspan[0])/(N - 1) # assuming equal time steps
    if noise == "levy":
        dW = levy.rvs(0., 1e-11, (N-1, m))+np.random.normal(0., np.sqrt(h), (N-1, m)) 
    elif noise == "cauchy":
        dW = cauchy.rvs(0., 1e-4, (N-1, m))
    else:
        dW = None
    chosenAlgorithm = sdeint.integrate.itoSRI2
    return chosenAlgorithm(f, G, y0, tspan, dW = dW)

class evolve():
    def __init__( self, tipping_network, initial_state ):
        # Initialize solver
        self._net = tipping_network
        # Initialize state
        self._times = []
        self._states = []
        
        self._t = 0
        self._x = initial_state

        self.save_state( self._t, self._x ) 
        
    def save_state( self , t, x):
        """Save current state if save flag is set"""
        self._times.append( t )
        self._states.append( x )

    def get_timeseries( self ):
        times = np.array ( self._times )
        states = np.array ( self._states )
        return [times , states]
    
    def _integrate_sde( self, t_step, initial_state, sigma=None, noise = "normal"):
        
        t_span = [ self._t , self._t + t_step ]
        x_init = self._x
         
        diffusion = lambda x,t: sigma 
        sol=itoint(self._net.f,diffusion,x_init,t_span, noise = noise)
        self._t = t_span[1]
        
        self._x = sol[1]        
        self.save_state(self._t, self._x)    
        
    def _integrate_ode( self, t_step):
        
        t_span = [ self._t , self._t + t_step ]
        x_init = self._x
        
        sol = odeint( self._net.f , x_init, t_span, Dfun=self._net.jac )
            
        self._t = t_span[1]

        self._x = sol[1]
        
        self.save_state(self._t, self._x)
        
    def integrate( self, t_step, t_end,initial_state, sigma=None , noise = "normal"):
        """Manually integrate to t_end"""
        
        if sigma is None:
            while self._times[-1] < t_end:
                self._integrate_ode( t_step )
        else:
            while self._times[-1] < t_end:
                    self._integrate_sde( t_step,initial_state,sigma, noise = noise)
    
    def equilibrate( self, tol , t_step, t_break=None,sigma=None ):
        """Iterate system until it is in equilibrium. 
        After every iteration it is checked if the system is in a stable
        equilibrium"""
        t0 = time.process_time()
        
        if sigma is None:
            while not self.is_equilibrium( tol ): 
                self._integrate_ode( t_step,sigma )
                if t_break and (time.process_time() - t0) >= t_break:
                    raise NoEquilibrium(
                            "No equilibrium found " \
                            "in " + str(t_break) + " seconds." \
                            " Increase tolerance or breaktime."
                            )
        else:
            while not self.is_equilibrium( tol ): 
                self._integrate_sde( t_step,sigma )
                if t_break and (time.process_time() - t0) >= t_break:
                    raise NoEquilibrium(
                            "No equilibrium found " \
                            "in " + str(t_break) + " seconds." \
                            " Increase tolerance or breaktime."
                            )
   
    def is_equilibrium( self, tol ):
        """Check if the system is in an equilibrium state, e.g. if the 
        absolute value of all elements of f (f is x_dot) is less than tolerance. 
        If True the state can be considered as close to a fixed point"""
        n = self._net.number_of_nodes()
        f = self._net.f( self._x, self._t)
        fix = np.less( np.abs(f) , tol * np.ones( n ))
        
        if fix.all():
            return True
        else:
            return False

    def is_stable( self ):
        """Check stability of current system state by calculating the 
        eigenvalues of the jacobian (all eigenvalues < 0 => stable)."""
        n = self._net.number_of_nodes()
        jacobian = self._net.jac( self._x, self._t)
        val, vec = np.linalg.eig( jacobian )
        stable = np.less( val, np.zeros( n ) )

        if stable.all():
            return True
        else:
            return False
