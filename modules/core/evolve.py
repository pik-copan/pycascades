from scipy.integrate import odeint
import numpy as np
import time

"""evolve module"""
class NoEquilibrium(Exception):
    pass

class evolve():
    def __init__( self, tipping_network, initial_state ):
        # Initialize solver
        self._net = tipping_network
        # Initialize state
        self._times = []
        self._states = []
        
        self.save_state( 0, initial_state ) 
        
    def save_state( self , t, y):
        """Save current state if save flag is set"""
        self._times.append( t )
        self._states.append( y )
    
    def get_timeseries( self ):
        times = np.array ( self._times )
        states = np.array ( self._states )
        return times , states
        
    def _integrate( self, t_step ):
        
        t_span = [ self._times [-1] , self._times [-1] + t_step ]
        y_init = self._states[-1]
        sol = odeint( self._net.f , y_init, t_span, Dfun=self._net.jac )
        self.save_state( t_span[1], sol[1] )
        
    def integrate( self, t_step, t_end ):
        """Manually integrate to t_end"""
        while self._times[-1] < t_end:
            self._integrate( t_step )
    
    def equilibrate( self, tol , t_step, t_break=None ):
        """Iterate system until it is in equilibrium. 
        After every iteration it is checked if the system is in a stable
        equilibrium"""
        t0 = time.process_time()
        while not self.is_equilibrium( tol ): 
            self._integrate( t_step )
        
            if t_break and (time.process_time() - t0) >= t_break:
                raise NoEquilibrium(
                        "No equilibrium found " \
                        "in "+str(t_break)+" realtime seconds."\
                        " Increase tolerance or breaktime."
                        )
   
    def is_equilibrium( self, tol ):
        """Check if the system is in an equilibrium state, e.g. if the 
        absolute value of all elements of f_prime is less than tolerance. 
        If True the state can be considered as close to a fixed point"""
        n = self._net.number_of_nodes()
        f = self._net.f( self._states[-1], self._times[-1])
        fix = np.less( np.abs( f) , tol * np.ones( n ))
        
        if fix.all():
            return True
        else:
            return False

    def is_stable( self ):
        """Check stability of current system state by calculating the 
        eigenvalues of the jacobian (all eigenvalues < 0 => stable)."""
        n = self._net.number_of_nodes()
        jacobian = self._net.jac( self._states[-1], self._times[-1])
        val, vec = np.linalg.eig( jacobian )
        stable = np.less( val, np.zeros( n ) )

        if stable.all():
            return True
        else:
            return False
