"""coupling module

Provides classes for couplings.
Note that a coupling consists of two elements. The active element (called 
coupling element here) affects the passive element (called coupled 
element here).
"""
import math

class coupling:
    """Abstract class for coupling of two tipping_elements
    Class should not be used but rather be inherited from by concrete coupling
    classes."""

    def __init__(self):
        pass

    def dxdt_cpl(self):
        """Returns callable for the coupling term of dxdt."""
        return lambda t, x_from , x_to : 0
    
    def jac_cpl(self):
        """Returns callable for the jacobian coupling matrix element."""
        return lambda t, x_from , x_to : 0
    
    def jac_diag(self):
        return lambda t, x_from , x_to : 0

    def projection(self):
        return lambda t : 1


class linear_coupling(coupling):
    """Class for linear coupling
    The coupling consists of a factor (strength) and a coupling element.
    """

    def __init__(self, strength):
        """Constructor"""
        coupling.__init__(self)
        self._strength = strength
        
    def dxdt_cpl(self):
        """Returns callable for the coupling term of dxdt."""
        return lambda t, x_from , x_to : self._strength * x_from
    
    def jac_cpl(self):
        """Returns callable for the jacobian coupling matrix element."""
        return lambda t, x_from , x_to : self._strength
    
    def jac_diag(self):
        return lambda t, x_from , x_to : 0

    def bif_impact(self):
        return lambda t, x_from , x_to : self._strength * x_from
		


class cusp_to_hopf(coupling):
    """Class for coupling """

    def __init__(self, _from, _to, a_hopf, strength):
        coupling.__init__(self, _from, _to)
        self._strength = strength
        self._a = a_hopf

    def dxdt_cpl(self):
        """coupling"""
        return lambda t, x_from, r_to : self._a*r_to*self._strength*x_from

    def jac_cpl(self):
        """partial derivative of dxdt with respect to x_from"""
        return lambda t, x_from, r_to : self._a*r_to*self._strength

    def jac_diag(self):
        """partial derivative with respect to r_to"""
        return lambda t, x_from, r_to : self._a*self._strength*x_from

    def bif_impact(self):
        return lambda t, x_from, r_to : self._strength*x_from


class hopf_x_to_cusp(coupling):
    """Class for coupling """

    def __init__(self, _from, _to, b_hopf, strength):
        """Constructor"""
        coupling.__init__(self, _from, _to)
        self._b = b_hopf
        self._strength = strength

    def dxdt_cpl(self):
        """coupling"""
        return lambda t, r_from, x_to : self._strength*r_from*math.cos(self._b
                                                                       *t)

    def jac_cpl(self):
        """partial derivative of dxdt with respect to r_from"""
        return lambda t, r_from, x_to : self._strength*math.cos(self._b*t)

    def jac_diag(self):
        """partial derivative with respect to x_to"""
        return lambda t, r_from, x_to : 0

    def projection(self):
        return lambda t : math.cos(self._b*t)

    def bif_impact(self):
        return lambda t, r_from, x_to : self._strength*r_from*math.cos(self._b
                                                                       *t)

class hopf_y_to_cusp(coupling):
    """Class for coupling """

    def __init__(self, _from, _to, b_hopf, strength):
        """Constructor"""
        self._b = b_hopf
        self._strength = strength

    def dxdt_cpl(self):
        """coupling"""
        return lambda t, r_from, x_to : self._strength*r_from*math.sin(self._b
                                                                       *t)

    def jac_cpl(self):
        """partial derivative of dxdt with respect to r_from"""
        return lambda t, r_from, x_to : self._strength*math.sin(self._b*t)

    def jac_diag(self):
        """partial derivative with respect to x_to"""
        return lambda t, r_from, x_to : 0

    def projection(self):
        return lambda t : math.sin(self._b*t)

    def bif_impact(self):
        return lambda t, r_from, x_to : self._strength*r_from*math.sin(self._b
                                                                       *t)

class hopf_x_to_hopf(coupling):
    """Class for coupling """
    def __init__(self, _from, _to, a_to, b_from, strength):
        coupling.__init__(self, _from, _to)
        self._a_to = a_to
        self._b_from = b_from
        self._strength = strength

    def dxdt_cpl(self):
        return lambda t, r_from, r_to : self._a_to*r_to*self._strength*r_from*\
                                        math.cos(self._b_from*t)

    def jac_cpl(self):
        return lambda t, r_from, r_to : self._a_to*r_to*self._strength*\
                                      math.cos(self._b_from*t)

    def jac_diag(self):
        return lambda t, r_from, r_to : self._a_to*self._strength*r_from*\
                                        math.cos(self._b_from*t)

    def projection(self):
        return lambda t : math.cos(self._b_from*t)

    def bif_impact(self):
        return lambda t, r_from, r_to : self._strength*r_from*\
                                        math.cos(self._b_from*t)

class hopf_y_to_hopf(coupling):
    """Class for coupling """

    def __init__(self, _from, _to, a_to, b_from, strength):
        coupling.__init__(self, _from, _to)
        self._a_to = a_to
        self._b_from = b_from
        self._strength = strength

    def dxdt_cpl(self):
        return lambda t, r_from, r_to: self._a_to*r_to*self._strength*r_from*\
                                       math.sin(self._b_from * t)

    def jac_cpl(self):
        return lambda t, r_from, r_to: self._a_to*r_to*self._strength*\
                                     math.sin(self._b_from * t)

    def jac_diag(self):
        return lambda t, r_from, r_to: self._a_to*self._strength*r_from*\
                                       math.sin(self._b_from * t)

    def projection(self):
        return lambda t : math.sin(self._b_from * t)

    def bif_impact(self):
        return lambda t, r_from, r_to : self._strength*r_from*\
                                        math.sin(self._b_from*t)

class linear_coupling_earth_system(coupling):

    def __init__(self, strength, x_0):
        coupling.__init__(self)
        self._strength = strength
        self._x_0 = x_0

    def dxdt_cpl(self):
        return lambda t, x_from, x_to: self._strength * (x_from - self._x_0)

    def jac_cpl(self):
        return lambda t, x_from, x_to: self._strength

    def jac_diag(self):
        return lambda t, x_from, x_to: 0

    def bif_impact(self):
        return lambda t, x_from, x_to: self._strength * (x_from - self._x_0)
