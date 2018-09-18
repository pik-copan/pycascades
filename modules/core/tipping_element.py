"""tipping_element module

Provides classes for tipping_element objects
"""



class tipping_element:
    """Abstract tipping_element class
    This class provides the interface for tipping_element classes.
    It should not be used but rather inherited from by the concrete 
    tipping_element classes.
    """

    def __init__(self,id_number):
        """Constructor"""
        self.id = id_number

        """dx/dt and jacobian diagonal element of tipping element. 
        This method should be overwritten from the 
        concrete tipping_element classes to implement
        the special form of the tipping element.
        """
        
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

class cusp(tipping_element):
    """Concrete class for cusp-like tipping element"""
    def __init__(self, id_number, a, b ):
        """Constructor with additional parameters for cusp"""
        tipping_element.__init__(self,id_number)
        self.a = a
        self.b = b
        
    def dxdt_diag(self):
        """returns callable of dx/dt diagonal element of cusp"""
        return lambda par,x : self.a*pow(x,3) + self.b*x + par
    
    def jac_diag(self):
        """returns callable jacobian diagonal element of cusp."""
        return lambda par,x : 3*self.a*pow(x,2) + self.b


class hopf(tipping_element):
    """Concrete class for tipping_elements following the dynamics of a
    Hopfbifurcation"""
    def __init__(self, id_number, a, b, bif_par):
        self._id = id
        self._a = a
        self._b = b
        self._bif_par = bif_par

    def dxdt(self,x):
        """One half of a Hopfbifurcation"""
        return -self._a*pow(x,3)+self._a*self._bif_par*x

    def jac(self,x):
        """Method returns the derivative of dx/dt with respect to x evoluated
        at commited value x"""
        return -3*self._a*pow(x,2)+self._a*self._bif_par