"""tipping_element module

Provides classes for tipping_element objects
"""
import numpy as np
from math import exp
from scipy.optimize import fsolve

class tipping_element:
    """Version of  tipping_element for economic model with min-sector coupling.
    
    Due to the nonlinear min-sector coupling the jacobian cannot be defined 
    in a straightforward way and is left out of all class definitions for the 
    economic tipping cascades. In general, this makes the ODE-solver less 
    flexible but for the equations used in the economic model that is not a 
    problem.
    """

    def __init__(self):
        """Constructor"""
        self._type = None
        self._par = {}

    def get_type(self):
        return self._type

    def get_par(self):
        return self._par
    
    def set_par(self, key, val):
        self._par[key] = val
    
    def dxdt_diag(self):
        """dx/dt diagonal element of tipping element. 
        This method should be overwritten from the 
        concrete tipping_element classes to implement
        the special form of the tipping element.
        """
        return lambda t, x : 0
    
    def tip_state(self):
        return lambda x : 0

class economic_logistic(tipping_element):
    """Economic tipping element with logistic growth term.
    
    Written in LaTex code, the differential equation is defined as 
        x_i' = -x_i-4\sqrt{x}\exp (-10x_i) + 0.2 x_i(1-x_i)+r_i
    with the coupling term r_i. Unfortunately, this equation is not
    defined for x<0, but the numerical solver will occasionally arrive 
    at negative values. To solve this problem, we replace the economic 
    equation for small x by a polynomial equation with similar behaviour.
    The equations are "stitched" together in the lower tipping point 
    (x_0,x'(x_0)) so that the expression remains continuously 
    differentiable. In La'Tex code:
        x' = \begin{cases} -x-4x^{0.5}\exp (-10x)+r & x > x_0 \\
            -\frac{x'_0}{x_0^4} (x-x_0)^4+x'_0 +r & x \leq x_0 \end{cases}
    """
    
    def __init__(self, a = 4, b = 0.5, c = 6, w = 1, r_0 = 0, epsilon = 0.01 ):
        """Constructor"""
        super().__init__()
        self._type = 'economic'
        self._par['a'] = a
        self._par['b'] = b
        self._par['c'] = c
        self._par['w'] = w
        self._par['r_0'] = r_0
        
        ### calculate parameters for the polynomial replacement
            ### epsilon has to be chaosen so that the solver finds the 
            ### lower and not the upper tipping point
        self._par['x_0'] = fsolve( self._xprimeprime, epsilon )[0] 
        self._par['xprime_0'] = self._xprime( self._par['x_0'] )
        
    def _xprime(self, x):
        return - x - self._par['a'] * pow(x, self._par['b']) * exp(- self._par['c'] * x) + self._par['w'] * x * ( 1 - x )
    
    def _xprimeprime(self, x):
        return (self._par['w'] - 1) - 2 * self._par['w'] * x \
            - self._par['a'] * self._par['b'] * pow(x, self._par['b']-1) * exp( - self._par['c'] * x ) \
            + self._par['a'] * self._par['c'] * pow(x, self._par['b']) * exp( - self._par['c'] * x )
    
    def dxdt_diag(self):
        """returns callable of dx/dt diagonal element of cusp"""
        return lambda t, x : - x - self._par['a'] * pow(x, self._par['b']) \
                           * exp(- self._par['c'] * x) + self._par['w'] * x * ( 1 - x ) \
                           + self._par['r_0'] \
                           if x > self._par['x_0'] else \
                           - self._par['xprime_0']/pow(self._par['x_0'],4) * \
                           pow((x - self._par['x_0']), 4) + self._par['xprime_0'] \
                           + self._par['r_0'] 
    
    def tip_state(self):
        return lambda x : x < self._par['x_0']
