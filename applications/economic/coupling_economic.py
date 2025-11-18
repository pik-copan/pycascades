"""coupling module

Provides classes for couplings.
Note that a coupling consists of two elements. The active element (called 
coupling element here) affects the passive element (called coupled 
element here).
"""
import math

class coupling:
    """Version of  coupling for economic model with min-sector coupling.
    
    Due to the nonlinear min-sector coupling the jacobian cannot be defined 
    in a straightforward way and is left out of all class definitions for the 
    economic tipping cascades. In general, this makes the ODE-solver less 
    flexible but for the equations used in the economic model that is not a 
    problem.
    """

    def __init__(self):
        pass

    def dxdt_cpl(self):
        """Returns callable for the coupling term of dxdt."""
        return lambda t, x_from , x_to : 0
    
    def projection(self):
        return lambda t : 1


class linear_coupling(coupling):
    """Version of  linear_coupling for economic model with min-sector coupling.
    
    Due to the nonlinear min-sector coupling the jacobian cannot be defined 
    in a straightforward way and is left out of all class definitions for the 
    economic tipping cascades. In general, this makes the ODE-solver less 
    flexible but for the equations used in the economic model that is not a 
    problem.
    """
    def __init__(self, strength):
        """Constructor"""
        coupling.__init__(self)
        self._strength = strength
        
    def dxdt_cpl(self):
        """Returns callable for the coupling term of dxdt."""
        return lambda t, x_from , x_to : self._strength * x_from
    
