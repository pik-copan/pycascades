"""network module"""

class network:
    """network class
    Aggregates tipping_elements and provides methods to get system information.
    """
    def __init__(self):
        """Constructor"""
        self.tip_list = []
        
    def add_element(self,tip_element):
        """Add a tipping element to the network"""
        self.tip_list.append(tip_element)
        
    def system(self,x,t):
        """Interface that collects the dx/dt functions of the tipping elements
        in one vector for common ODE-Solvers.
        """
        df = []
        for tip_element in self.tip_list:
            df.append(tip_element.f_prime(x))
        return df
            
    def get_state(self):
        """Returns state vector of the network. Note that state denotes the
        vector of the continuous x variable in contrast to binary information 
        of the tipping status. The reason is that these binary information do
        not suffice to completely determine the dynamic of the system.
        """
        state_vec = []
        for tip_element in self.tip_list:
            state_vec.append(tip_element.x)
        return state_vec
        
    def get_structure(self):
        """Get some text information of the system structure.
        !!!Method currently not working correctly!!!
        """
        ret_string = ""
        for tip_element in self.tip_list:
            ret_string = ret_string + str(tip_element.id) + "\n"
        for cpl in tip_element.cpl_list:
            ret_string = (ret_string + str(cpl.out.id) 
                          + " --> " + str(tip_element.id)
				        + "\n")
        return ret_string
