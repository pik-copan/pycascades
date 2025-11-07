from scipy.integrate import odeint
import numpy as np
import time
import sdeint
from scipy.stats import levy, cauchy, levy_stable
from numba import jit
import warnings

"""evolve module"""
class NoEquilibrium(Exception):
    pass


   

def gen_levy_noise_preproc(alpha, sigma, dt, n = 1):
    if not isinstance(alpha, np.ndarray):
        if not isinstance(alpha, list):
            alpha = [alpha]
        alpha = np.array(alpha)
    if len(alpha) < n:
        alpha = np.repeat(alpha, n//len(alpha) + 1)[:n]
    if not isinstance(sigma, np.ndarray):
        if not isinstance(sigma, list):
            sigma = [sigma]
        sigma = np.array(sigma)
    if len(sigma) < n:
        sigma = np.repeat(sigma, n//len(sigma) + 1)[:n]
    return alpha, sigma, dt, n



@jit(nopython = True)
def semi_impl_euler_maruyama_alphastable_sde_nb_loop(n, N, x, xs, t, ts, dt_scaled, coupl, c, L, dt):
    for i in range(1,N):
        x_new = x.copy()        

        transp = (coupl @ x)
            
        for j in range(n):
            if (not np.isnan(x[j])) and (not np.isinf(x[j])):           
                candidates = np.roots(np.array([dt_scaled[j], 0.0, 1.0 - dt_scaled[j], - x[j] - (c[j] + transp[j]) * dt_scaled[j]]).astype(np.complex128))
                if (np.abs(candidates.imag)<1e-5).sum() == 1:
                    drift = (candidates[np.abs(candidates.imag)<1e-5][0]).real 
                else:
                    best_idx = np.argmin(np.abs(candidates - x[j]))
                    drift = (candidates[best_idx]).real
            else:
                drift = x[j]

            x_new[j] = drift + L[j, i]

            # x2 = x1 + (-x2^3 + x2 + c)*dt/taos

        t += dt
        ts[i] = t
        x = x_new#.copy()
        xs[i,:] = x

    return ts, xs
    

def semi_impl_euler_maruyama_alphastable_sde(x0 = [-1.0, -1.0, -1.0], dt = 0.1, cs = [0.0, 0.3, 0.4], taos = [1.0, 1.0, 1.0], t_end = 1000, alphas = [1.5, 1.5, 1.5], sigmas = [0.0, 0.0, 0.1], coupl = np.array([[0.0, 0.1, 0.1], [-0.1, 0.0, 0.2], [0.0, -0.1, 0.0]]), rng = None):

    x0 = np.array(x0, dtype="float").flatten()
    taos = np.array(taos, dtype="float").flatten()
    cs = np.array(cs, dtype="float").flatten()
    alphas = np.array(alphas, dtype="float").flatten()
    sigmas = np.array(sigmas, dtype="float").flatten()
    coupl = np.array(coupl, dtype="float")

    alphas, sigmas, dt_scaled, n = gen_levy_noise_preproc(alphas, sigmas, dt / (taos + 1e-6), n = len(x0))

    x = x0.copy()
    N = int(t_end // dt) + 1
    xs = np.zeros((N,n))
    xs[0,:] = x
    t = 0
    ts = np.zeros(N)

    L = np.zeros((n, N))
    for i in range(n):
        if sigmas[i] > 0:
            L[i,:] = sigmas[i] * (dt_scaled[i] ** (1/alphas[i])) * levy_stable.rvs(alphas[i], 0.0, size=N, random_state = rng)
    
    L[np.abs(L) > 1e12] = (np.sign(L) * 1e12)[np.abs(L) > 1e12]
    L[np.isinf(L)] = (np.sign(L) * 1e12)[np.isinf(L)]
    L[np.isnan(L)] = 0.0

    ts, xs = semi_impl_euler_maruyama_alphastable_sde_nb_loop(n, N, x, xs, t, ts, dt_scaled, coupl, cs, L, dt)
    
    return ts, xs, rng
    


def itoint(f, G, y0, tspan, noise = "normal", levy_alpha = 1.5):
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
    elif noise == "levy_stable":
        dW = (h ** (1/levy_alpha)) * levy_stable.rvs(levy_alpha, 0.0, (N-1, m))#+np.random.normal(0., np.sqrt(h), (N-1, m)) 
    elif noise == "cauchy":
        dW = cauchy.rvs(0., 1e-4, (N-1, m))
    else:
        dW = None
    chosenAlgorithm = sdeint.integrate.itoSRI2
    return chosenAlgorithm(f, G, y0, tspan, dW = dW)

def get_params_from_es_network(net):

    n_nodes = net.number_of_nodes()

    cs = np.zeros(n_nodes)
    taos = np.zeros(n_nodes)
    coupl = np.zeros((n_nodes, n_nodes))
    
    for i in range(n_nodes):

        node = net.nodes[i]
        pars = node["data"].get_par()
        taos[i] = 1 / pars["b"]
        cs[i] = pars["c"] * taos[i]

        in_idxs = [e[0] for e in list(net.in_edges(i))]
        for j in in_idxs:
            
            if hasattr(net.get_edge_data(j,i)["data"], "_x_0"):
                x0 = net.get_edge_data(j,i)["data"]._x_0
            else:
                x0 = 0.0
                
            d = taos[i] * net.get_edge_data(j,i)["data"]._strength

            coupl[i,j] = d

            cs[i] += -x0 * d
        

    return cs, taos, coupl


class evolve():
    def __init__( self, tipping_network, initial_state ):
        # Initialize solver

        self._all_cusp = all([n == "cusp" for n in tipping_network.get_node_types()])
        self._all_linear_coupl = all([tipping_network.get_edge_data(e[0], e[1])["data"].__class__.__name__ in ["linear_coupling_earth_system", "linear_coupling"]  for e in tipping_network.edges])

        if self._all_cusp and self._all_linear_coupl:
            # get c, taos, coupl
            self._cs, self._taos, self._coupl = get_params_from_es_network(tipping_network)


        self._net = tipping_network
        # Initialize state
        self._times = []
        self._states = []
        
        self._t = 0
        self._x = initial_state

        self.save_state( self._t, self._x ) 

        self._rng = None
        
    def save_state( self , t, x):
        """Save current state if save flag is set"""
        self._times.append( t )
        self._states.append( x )

    def get_timeseries( self ):
        times = np.array ( self._times )
        states = np.array ( self._states )
        return [times , states]
    
    def _integrate_sde( self, t_step, sigma=None, noise = "normal"):
        
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

    def _integrate_duffing_sde(self, dt, t_end, alphas, sigmas, rng = None):

        if any(alphas) < 0.1:
            warnings.warn("The CMS algorithm for generating levy-stable noise is not reliable for alphas < 0.1. The implementation provided here truncates large noise values above +-1e12 and sets any nans to 0.")


        x0 = self._x
        cs = self._cs
        taos = self._taos
        coupl = self._coupl
        
        ts, xs, rng = semi_impl_euler_maruyama_alphastable_sde(x0 = x0, dt = dt, cs = cs, taos = taos, t_end = t_end, alphas = alphas, sigmas = sigmas, coupl = coupl, rng = rng)

        self._times = ts.tolist()
        self._states = xs.tolist()
        self._t = self._times[-1]
        self._x = self._states[-1]
        self._rng = rng

        
    def integrate( self, t_step, t_end, sigmas = None , noise = "normal", alphas = None, seed = None):
        """Manually integrate to t_end"""
        
        if sigmas is None:
            while self._times[-1] < t_end:
                self._integrate_ode( t_step )
        elif self._all_cusp and self._all_linear_coupl:
            if (noise == "normal") and (alphas is None):
                alphas = [2.0 for _ in range(len(self._x))]
            elif alphas is None:
                raise NotImplementedError

            if self._rng is None:
                rng = np.random.RandomState(seed)
            else:
                rng = self._rng
            
            self._integrate_duffing_sde(t_step, t_end, alphas = alphas, sigmas = sigmas, rng = rng)
        else:
            while self._times[-1] < t_end:
                self._integrate_sde( t_step, sigmas, noise = noise)
    
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
