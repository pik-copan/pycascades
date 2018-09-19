"""coupling module

Provides classes for couplings.
Note that a coupling consists of two elements. The active element (called 
coupling element here) affects the passive element (called coupled 
element here).
"""
class linear_coupling:
    """Class for linear coupling
    The coupling consists of a factor (strength) and a coupling element.
    """
    def __init__(self,strength):
        """Constructor"""
        self.strength = strength
        
    def dxdt_cpl(self):
        """Returns callable for the coupling term of dxdt."""
        return lambda t, x_from , x_to : self.strength*x_from
    
    def jac_cpl(self):
        """Returns callable for the jacobian coupling matrix element."""
        return lambda t, x_from , x_to : self.strength
    
    def jac_diag(self):
        return lambda t, x_from , x_to : 0
		
