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
        self.x = 0.0
        self.cpl_list = []
        self.tipped = False
        
    def dxdt(self,x):
        """Calculate dx/dt of tipping element. This method should be
        overwritten from the concrete tipping_element classes to implement
        the special form of the tipping element.
        """
        print ("Warning: Either using abstract tipping_element class which"
                 + "is not suggested or forgot to override dxdt() function")
        return 0.0
    
    def jac(self,x):
        """Calculate jacobian diagonal element of tipping element. 
        This method should be overwritten from the concrete tipping_element
        classes to implement the special form of the tipping element.
        """
        print ("Warning: Either using abstract tipping_element class which"
                 + "is not suggested or forgot to override jac() function")
        return 0.0
    
    def update_state(self,x):
        """Change state of the tipping element. Override this method to 
        include tipping status updates"""
        self.x = x

class cusp(tipping_element):
    """Concrete class for cusp-like tipping element"""
    def __init__(self, id_number, a, b, c):
        """Constructor with additional parameters for cusp"""
        tipping_element.__init__(self,id_number)
        self.a = a
        self.b = b
        self.c = c
        
    def dxdt(self,x):
        """Normal form of cusp"""
        return ( self.a*pow(x,3) + self.b*x + self.c )
    
    def jac(self,x):
        """Diagonal element for jacobian matrix"""
        return ( 3*self.a*pow(x,2) + self.b )
    
    def update_state(self,x):
        """Change state of the tipping element and check wether element 
        is tipped. For a cusp-like tipping element that means the 
        state variable has passed zero which ultimately divides 
        the stable solutions for every point in parameter space."""
        if (self.x > 0 and x <= 0) or (self.x <= 0 and x > 0):
            self.tipped = not self.tipped
        self.x = x