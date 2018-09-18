"""coupling module

Provides classes for couplings.
Note that a coupling consists of two elements. The active element (called 
coupling element here) affects the passive element (called coupled 
element here).
"""


class coupling:
    """Abstract class for coupling of two tipping_elements
    Class should not be used but rather be inherited from by concrete coupling
    classes."""

    def __init__(self, origin, to):
        self._from = origin
        self._to = to

    def coupling(self, x_1, x_2):
        """Method computes the effect of x_1 on x_2, thus implements the
        coupling from x_1 to x_2.
        The method should be overwritten by concrete a tipping_element class
        to implement the respective coupling between two elements."""
        print('Warning: Either the abstract class is used which is not' +
              'recommented or the method coupling() has not been overwritten')
        return 0.0


class linear_coupling(coupling):
    """Class for linear coupling
    The coupling consists of a factor (strength) and a coupling element.
    """

    def __init__(self,strength):
        """Constructor"""
        self.strength = strength
        
    def dxdt_cpl(self):
        """Returns callable for the coupling term of dxdt."""
        return lambda x_from , x_to : self.strength*x_from
    
    def jac_cpl(self):
        """Returns callable for the jacobian coupling matrix element."""
        return lambda x_from , x_to : self.strength
		


class hopf_coupling(coupling):
    """Class for coupling of two (Hopf) tipping_elements according to
    Hopfbifurcation.
    The coupling consists of two terms -a*x_1^2*x_2 and b*x_1, x_1 being the
    originate node of the coupling effecting x_2"""

    def __init__(self, _from, _to, a, b):
        """Constructor"""
        self.a = a
        self.b = b
        self._to = _to
        self._from = _from

    def coupling(self, x_1, x_2, a, b):
        """Method returns coupling from Hopf tipping_element x_1 to Hopf
        tipping_element x_2: -a*x_1^2*x_2+b*x_1"""
        return -a*pow(x_1,2)*x_2+b*x_1

