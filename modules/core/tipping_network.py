from networkx import DiGraph
from scipy.sparse import coo_matrix
import numpy as np
       
class tipping_network(DiGraph):

    def __init__( self, incoming_graph_data=None, **attr):
        DiGraph.__init__( self, incoming_graph_data=None, **attr)
        self.dxdt = coo_matrix((0,0))
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

    def f( self, t, x):
        f = np.zeros( self.number_of_nodes() )
        for idx in range( 0, self.number_of_nodes() ):
            f[idx] = self.dxdt["diag"][idx].__call__( t, x[idx] )
            for cpl in self.dxdt["cpl"][idx]:
                f[idx] += cpl[2].__call__(t, x[cpl[0]], x[idx])
        return f

    def jac(self, t, x):
        jac = np.zeros((self.number_of_nodes(), self.number_of_nodes()))

        for cpl in self.jac_dict["cpl"]:
            jac[cpl[1], cpl[0]] += cpl[2].__call__( t, x[cpl[0]], x[cpl[1]])

        for idx in range(0, len(x)):
            jac[idx, idx] = self.jac_dict["diag"][idx].__call__(t, x[idx])
            for add in self.jac_dict["diag_add"]:
                jac[idx, idx] += add[2].__call__( t, x[add[0]], x[add[1]])
        return jac
            
    def get_adjusted_bif_par_vec( self , bif_par_eff_vec , initial_state ):
        """Adjust bifurcation parameter so that the sum of coupling and
        bifurcation parameter (effective bifurcation parameter) 
        equals bif_par_eff_vec"""
        bif_par_vec = []
        for to_id in range(0,self.number_of_nodes()):
            cpl_sum = bif_par_eff_vec[to_id]
            for from_id in range(0,self.number_of_nodes()):
                if not self.get_edge_data(from_id,to_id) == None:
                    cpl_val = self.get_edge_data(
                                        from_id,to_id)['data'].dxdt_cpl()
                    cpl_sum += -cpl_val.__call__( 0 , initial_state[from_id] 
                                                , initial_state[to_id] )
            
            bif_par_vec.append(cpl_sum)
        return bif_par_vec

    def get_hopf_dict(self):
        return self._hopf_dict

    def get_node_types(self):
        return self._node_types

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
