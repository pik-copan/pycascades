import sdeint
import numpy as np
from scipy.stats import levy, cauchy, levy_stable


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
    (d, m, f, G, y0, tspan, __, __) = sdeint.integrate._check_args(
        f,
        G,
        y0,
        tspan,
        None,
        None
    )
    N = len(tspan)
    h = (tspan[N - 1] - tspan[0]) / (N - 1)  # assuming equal time steps
    if noise == "levy":
        dW = (
            levy.rvs(0., 1e-11, (N - 1, m))
            + np.random.normal(0., np.sqrt(h), (N - 1, m))
        )
    elif noise == "levy_stable":
        dW = (
            (h ** (1 / levy_alpha))
            * levy_stable.rvs(levy_alpha, 0.0, (N - 1, m))
        )
    elif noise == "cauchy":
        dW = cauchy.rvs(0., 1e-4, (N - 1, m))
    else:
        dW = None
    chosenAlgorithm = sdeint.integrate.itoSRI2
    return chosenAlgorithm(f, G, y0, tspan, dW = dW)
