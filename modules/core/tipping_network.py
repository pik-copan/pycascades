import networkx as nx
import numpy as np
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
            
    def get_tip_state(self):
        """Returns binary state vector of the network."""
        tip_vec = []
        for id in self.nodes():
            tip_vec.append(self.node[id]['data'].tipped)
        return tip_vec
    
    def f_prime(self,t,x):
        """Interface that collects the dx/dt functions of the tipping elements
        in one vector for common ODE-Solvers.
        """
        df = []
        cpl_vec = np.matrix(x)*nx.adjacency_matrix(self,nodelist=None
                                                   ,weight='weight').todense()
        for id in self.nodes():
            f_prime = self.node[id]['data'].dxdt(x[id]) + cpl_vec[0,id]
            df.append(f_prime)
        return df
    
    def jac(self,t,x):
        """Returns jacobian for iteration and 
        stability checkups of fixed points."""
        jac = nx.adjacency_matrix(self,nodelist=None
                                                   ,weight='weight').todense()
        for id in self.nodes():
            jac[id,id] = self.node[id]['data'].jac(x[id])
        return jac
    
    def adjust_normal_pars(self,c_eff):
        """Adjust normal parameter so that the sum of coupling and
        normal parameter (effective normal parameter) equals c_eff"""
        cpl_vec = np.matrix(self.get_state())*nx.adjacency_matrix(
                                                    self
                                                    ,nodelist=None
                                                    ,weight='weight').todense()
        for id in self.nodes():
            self.node[id]['data'].c = c_eff-cpl_vec[0,id]
            
    def is_stable(self):
        """Check stability of current system state by calculating the 
        eigenvalues of the jacobian (all eigenvalues < 0 => stable)."""
        val, vec = np.linalg.eig(self.jac(0,self.get_state()))
        stable = np.less(val,np.zeros((1,self.number_of_nodes())))
        if stable.all():
            return True
        else:
            return False
        
    def is_fixed_point(self,tolerance):
        """Check if the system is in an equilibrium state, e.g. if the 
        absolute value of all elements of f_prime is less than tolerance. 
        If True the state can be considered as close to a fixed point"""
        fix = np.less(np.abs(self.f_prime(0,self.get_state()))
                     ,tolerance*np.ones((1
                     ,self.number_of_nodes())))
        if fix.all():
            return True
        else:
            return False