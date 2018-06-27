from networkx import DiGraph


class tipping_network(DiGraph):
    def get_state(self):
        """Returns state vector of the network. Note that state denotes the
        vector of the continuous x variable in contrast to binary information 
        of the tipping status. The reason is that these binary information do
        not suffice to completely determine the dynamic of the system.
        """
        state_vec = []
        for id in self.nodes():
            state_vec.append(self.node[id]['data'].x)
        return state_vec
    
    def set_state(self,state_vec):
        """Update state by providing a new state vector"""
        for id in self.nodes():
            self.node[id]['data'].update_state(state_vec[id])
    
    def system(self,x,t):
        """Interface that collects the dx/dt functions of the tipping elements
        in one vector for common ODE-Solvers.
        """
        df = []
        for id in self.nodes():
            df.append(self.node[id]['data'].f_prime(x))
        return df