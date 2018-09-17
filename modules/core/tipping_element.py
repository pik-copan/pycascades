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
        self.dxdt = lambda par,x : 0
        self.jac_diag = lambda par,x: 0

class cusp(tipping_element):
    """Concrete class for cusp-like tipping element"""
    def __init__(self, id_number, a, b ):
        """Constructor with additional parameters for cusp"""
        tipping_element.__init__(self,id_number)
        self.a = a
        self.b = b
        self.dxdt = lambda par,x : self.a*pow(x,3) + self.b*x + par
        self.jac_diag = lambda par,x : 3*self.a*pow(x,2) + self.b