from networkx import DiGraph
import numpy as np
       
class tipping_network(DiGraph):

    def __init__( self, incoming_graph_data=None, **attr):
        DiGraph.__init__( self, incoming_graph_data=None, **attr)
        
    def add_element( self, tipping_element ):
        ind = self.number_of_nodes()
        super().add_node( ind, data = tipping_element )
        self.node[ind]['lambda_f'] = tipping_element.dxdt_diag()
        self.node[ind]['lambda_jac'] = tipping_element.jac_diag()
        
    def add_coupling( self, from_id, to_id, coupling):
        super().add_edge( from_id, to_id, data = coupling)
        self[from_id][to_id]['lambda_f'] = coupling.dxdt_cpl()
        self[from_id][to_id]['lambda_jac'] = coupling.jac_cpl()
        self[from_id][to_id]['lambda_jac_diag'] = coupling.jac_diag()

    def set_param( self, node_id, key, val ):
        element = self.node[node_id]['data']
        element.set_par( key, val)
        self.node[node_id]['lambda_f'] = self.node[node_id]['data'].dxdt_diag()
        self.node[node_id]['lambda_jac'] = self.node[node_id]['data'].jac_diag()

    def get_tip_states( self, x):
        tipped = [self.node[i]['data'].tip_state()(x[i]) for i in self.nodes()]
        return np.array( tipped )
    
    def get_number_tipped( self, x):
        return np.count_nonzero( self.get_tip_states( x ) )
        
    def f( self, x, t):
        f = np.zeros( self.number_of_nodes() )
        for node in self.nodes(data=True):
            ind = node[0]
            x_comp = x[ind]
            f[ind] = node[1]['lambda_f'].__call__( t, x_comp)
        for edge in self.edges(data=True):
            from_id = edge[0]
            to_id = edge[1]
            lmd = edge[2]['lambda_f']
            f[to_id] += lmd.__call__( t, x[from_id], x[to_id])
        return f

    def jac(self, x, t):
        jac = np.zeros((self.number_of_nodes(), self.number_of_nodes()))
        for node in self.nodes(data=True):
            ind = node[0]
            x_comp = x[ind]
            jac[ind,ind] = node[1]['lambda_jac'].__call__( t, x_comp)
        for edge in self.edges(data=True):
            from_id = edge[0]
            to_id = edge[1]
            lmd = edge[2]['lambda_jac']
            jac[to_id, from_id] = lmd.__call__( t, x[from_id], x[to_id] )
            lmd_diag = edge[2]['lambda_jac_diag']
            jac[to_id, to_id] += lmd_diag.__call__( t, x[from_id], x[to_id] )
        return jac
            
    def get_adjusted_control( self , x ):
        """Adjust bifurcation parameter so that the sum of coupling and
        bifurcation parameter (effective bifurcation parameter) 
        equals bif_par_eff_vec"""
        effective_control = np.zeros(len(x))
        control = []
        for to_id in range( self.number_of_nodes() ):
            cpl_sum = effective_control[to_id]
            for from_id in range( self.number_of_nodes() ):
                if not self.get_edge_data(from_id,to_id) == None:
                    cpl_lmd = self[from_id][to_id]['data'].dxdt_cpl()
                    cpl_sum += -cpl_lmd.__call__( 0, x[from_id], x[to_id] )
            
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
