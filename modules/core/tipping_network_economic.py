import networkx as nx
import numpy as np
from copy import deepcopy
       
class tipping_network_economic(nx.DiGraph):
    """Version of  tipping_network for economic model with min-sector coupling.
    
    Due to the nonlinear min-sector coupling the jacobian cannot be defined 
    in a straightforward way and is left out of all class definitions for the 
    economic tipping cascades. In general, this makes the ODE-solver less 
    flexible but for the equations used in the economic model that is not a 
    problem.
    
    Economic model and min-sector coupling: 
    In the economic model each node belongs to one of n_s sectors. 
    Written in LaTex-code, the coupling term r_i for node i is defined as
        r_i =  \min_{s in sectors} \left\lbrace \sum_{c in countries} 
            w_{c,s\rightarrow i} x_{c,s} \right\rbrace
    x_{c,s} is the state of sector s in country c, and w_{c,s\rightarrow i} 
    is the entry of the normalised weight matrix for the link from sector s 
    in country c to node i. This is implemented by adding 'sectorlist', a 
    list of lists, to each node, where the i'th list contains those nodes from 
    the i'th sector which have a link to the respective node.
    """

    def __init__( self, incoming_graph_data=None, **attr):
        nx.DiGraph.__init__( self, incoming_graph_data=None, **attr)
        self._weight_mat = np.zeros((self.number_of_nodes(), self.number_of_nodes()))
        
    def add_element( self, tipping_element, n_s ):
        tipping_element = deepcopy(tipping_element)
        ind = self.number_of_nodes()
        super().add_node( ind, data = tipping_element )
        self.node[ind]['lambda_f'] = tipping_element.dxdt_diag()
        self.node[ind]['sectorlist'] = [ [] for i in range(n_s)]
        
    def add_coupling( self, from_id, to_id, from_sector_id, coupling):
        coupling = deepcopy(coupling)
        super().add_edge( from_id, to_id, data = coupling)
        self[from_id][to_id]['lambda_f'] = coupling.dxdt_cpl()
        self.node[to_id]['sectorlist'][from_sector_id].append(from_id)

    def set_param( self, node_id, key, val ):
        element = self.node[node_id]['data']
        element.set_par( key, val)
        self.node[node_id]['lambda_f'] = self.node[node_id]['data'].dxdt_diag()

    def get_tip_states( self, x):
        tipped = [self.node[i]['data'].tip_state()(x[i]) for i in self.nodes()]
        return np.array( tipped )

    def get_node_types( self ):
        type_list = [self.node[i]['data'].get_type() for i in self.nodes()]
        return type_list
        
    def get_number_tipped( self, x):
        return np.count_nonzero( self.get_tip_states( x ) )

    def f_economic( self, x, t):
        f = np.zeros( self.number_of_nodes() )
        for node in self.nodes(data=True):
            ind = node[0]
            x_comp = x[ind]
            f[ind] = node[1]['lambda_f'].__call__( t, x_comp)
            f[ind] += min( [sum( [self[from_id][ind]['lambda_f'].__call__( t, x[from_id], x_comp) \
                    for from_id in sector] ) if sector != [] else 1 \
                    for sector in node[1]['sectorlist']] ) 
        return f
    
    
