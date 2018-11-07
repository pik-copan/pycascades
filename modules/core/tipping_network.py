from networkx import DiGraph
import numpy as np
       
class tipping_network(DiGraph):

    def __init__( self, incoming_graph_data=None, **attr):
        DiGraph.__init__( self, incoming_graph_data=None, **attr)
        self.dxdt = { "diag" : [] , "cpl" : [] }
        self.jac_dict  = { "diag" : [] , "diag_add" : [] , "cpl" : [] }

    def add_element( self, tipping_element ):
        ind = self.number_of_nodes()
        super().add_node( ind, data = tipping_element )
        self.dxdt['diag'].append( tipping_element.dxdt_diag() )
        self.jac_dict['diag'].append( tipping_element.jac_diag() )
        self.dxdt['cpl'].append( [] )
        
    def add_coupling( self, from_id, to_id, coupling):
        super().add_edge( from_id, to_id, data = coupling)
        self.dxdt['cpl'][to_id].append( ( from_id, to_id, coupling.dxdt_cpl() ) )
        self.jac_dict['cpl'].append( (from_id, to_id, coupling.jac_cpl()) )
        self.jac_dict['diag_add'].append ( ( from_id, to_id, coupling.jac_diag() ) )

    def set_param( self, node_id, key, val ):
        element = self.node[node_id]['data']
        element.set_par( key, val)
        self.dxdt['diag'][node_id] = element.dxdt_diag()
        self.jac_dict['diag'][node_id] = element.jac_diag()
        """Update couplings to be faster"""
        
    def get_tip_states( self, x):
        tip_state = [self.node[node_id]['data'].tip_state()(x[node_id]) for node_id in self.nodes()]
        return np.array( tip_state )
    
    def get_number_tipped( self, x):
        return np.count_nonzero( self.get_tip_states( x ) )
        
    def f( self, x, t):
        f = np.zeros( self.number_of_nodes() )
        for idx in range( 0, self.number_of_nodes() ):
            f[idx] = self.dxdt["diag"][idx].__call__( t, x[idx] )
            for cpl in self.dxdt["cpl"][idx]:
                f[idx] += cpl[2].__call__(t, x[cpl[0]], x[idx])
        return f

    def jac(self, x, t):
        jac = np.zeros((self.number_of_nodes(), self.number_of_nodes()))

        for cpl in self.jac_dict["cpl"]:
            jac[cpl[1], cpl[0]] += cpl[2].__call__( t, x[cpl[0]], x[cpl[1]])

        for idx in range(0, len(x)):
            jac[idx, idx] = self.jac_dict["diag"][idx].__call__(t, x[idx])
            for add in self.jac_dict["diag_add"]:
                jac[idx, idx] += add[2].__call__( t, x[add[0]], x[add[1]])
        return jac
            
    def get_adjusted_control( self , x ):
        """Adjust bifurcation parameter so that the sum of coupling and
        bifurcation parameter (effective bifurcation parameter) 
        equals bif_par_eff_vec"""
        effective_control = np.zeros(len(x))
        control = []
        for to_id in range(0,self.number_of_nodes()):
            cpl_sum = effective_control[to_id]
            for from_id in range(0,self.number_of_nodes()):
                if not self.get_edge_data(from_id,to_id) == None:
                    cpl_val = self.get_edge_data(
                                        from_id,to_id)['data'].dxdt_cpl()
                    cpl_sum += -cpl_val.__call__( 0, x[from_id], x[to_id] )
            
            control.append(cpl_sum)
        return control

    def compute_impact_matrix(self):
        n = self.number_of_nodes()
        impact_matrix = [[lambda t, x1, x2: 0 for j in range(n)] for i in range(n)]
        for edge in self.edges.data():
            print(edge[2]['data'].bif_impact())
            impact_matrix[edge[1]][edge[0]]=edge[2]['data'].bif_impact()
            # if self.get_node_types()[edge[1]]=='cusp':
            #     impact_matrix[edge[1]][edge[0]]=edge['data'].dxdt_cpl()
            # elif self.get_node_types()[edge[1]]=='hopf':
            #     impact_matrix[edge[1]][edge[0]]=edge['data']
        return impact_matrix
