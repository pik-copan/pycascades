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
    def __init__(self,strength,out):
        """Constructor"""
        self.strength = strength
        self.out = out
        
    def coupling(self,x):
        """Returns the value for the coupling term depending on the strength 
        and the state x of the coupling element.
        """
        return self.strength*x
		
