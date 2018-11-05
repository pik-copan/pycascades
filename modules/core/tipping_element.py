"""tipping_element module

Provides classes for tipping_element objects
"""


class tipping_element:
    """Abstract tipping_element class
    This class provides the interface for tipping_element classes.
    It should not be used but rather inherited from by the concrete 
    tipping_element classes.
    """

    def __init__(self):
        """Constructor"""
        self._type = None

        """dx/dt and jacobian diagonal element of tipping element. 
        This method should be overwritten from the 
        concrete tipping_element classes to implement
        the special form of the tipping element.
        """
    
    
    def get_type(self):
        return self._type
  
    
    def dxdt_diag(self):
        """dx/dt diagonal element of tipping element. 
        This method should be overwritten from the 
        concrete tipping_element classes to implement
        the special form of the tipping element.
        """
        return lambda par,x : 0
    
    def jac_diag(self):
        """jacobian diagonal element of tipping element. 
        This method should be overwritten from the 
        concrete tipping_element classes to implement
        the special form of the tipping element.
        """
        return lambda par,x: 0
    
    def get_tip_state(self):
        return lambda x : 0


class cusp(tipping_element):
    """Concrete class for cusp-like tipping element"""
    def __init__(self, a, b ):
        """Constructor with additional parameters for cusp"""
        super().__init__()
        self._type = 'cusp'
        self._a = a
        self._b = b
        
    def dxdt_diag(self):
        """returns callable of dx/dt diagonal element of cusp"""
        return lambda t, par, x : self.a*pow(x,3) + self.b*x + par
    
    def jac_diag(self):
        """returns callable jacobian diagonal element of cusp."""
        return lambda t, par, x : 3*self.a*pow(x,2) + self.b
    
    def get_tip_state(self):
        return lambda x : 0

class hopf(tipping_element):
    """Concrete class for tipping_elements following the dynamics of a
    Hopfbifurcation.
    Implementation using a representation with polar coordinates:
    dr/dt=(bif_par-r^2)*r*a, dphi/dt=b (time-dependence of angle)"""

    def __init__(self, a, b):
        """Constructor with additional parameters for (half a) Hopf
        element"""
        super().__init__()
        self._type = 'hopf'
        self._a = a
        self._b = b

    def dxdt_diag(self):
        """returns callable of dx/dt diagonal element of Hopf element"""
        return lambda t, bif_par, r: (bif_par-pow(r,2))*r*self._a

    def jac_diag(self):
        """returns callable jacobian diagonal element of Hopf"""
        return lambda t, bif_par, r: self._a*bif_par-self._a*3*pow(r,2)

    def get_b(self):
        """ODE of angle (polar coordinates): domega/dt=b Hence, angle=t*b"""
        return self._b
