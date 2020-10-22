import networkx as nx
import numpy as np
       
class tipping_network(nx.DiGraph):

    def __init__( self, incoming_graph_data=None, **attr):
        nx.DiGraph.__init__( self, incoming_graph_data=None, **attr)
        
    def add_element( self, tipping_element ):
        ind = self.number_of_nodes()
        super().add_node( ind, data = tipping_element )
        self.nodes[ind]['lambda_f'] = tipping_element.dxdt_diag()
        self.nodes[ind]['lambda_jac'] = tipping_element.jac_diag()
        
    def add_coupling( self, from_id, to_id, coupling):
        super().add_edge( from_id, to_id, data = coupling)
        self[from_id][to_id]['lambda_f'] = coupling.dxdt_cpl()
        self[from_id][to_id]['lambda_jac'] = coupling.jac_cpl()
        self[from_id][to_id]['lambda_jac_diag'] = coupling.jac_diag()

    def set_param( self, node_id, key, val ):
        element = self.nodes[node_id]['data']
        element.set_par( key, val)
        self.nodes[node_id]['lambda_f'] = self.nodes[node_id]['data'].dxdt_diag()
        self.nodes[node_id]['lambda_jac'] = self.nodes[node_id]['data'].jac_diag()

    def get_tip_states( self, x):
        tipped = [self.nodes[i]['data'].tip_state()(x[i]) for i in self.nodes()]
        return np.array( tipped )

    def get_node_types( self ):
        type_list = [self.nodes[i]['data'].get_type() for i in self.nodes()]
        return type_list
        
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
    
    def set_vulnerability(self, node_id, bool_val):
        self.nodes[node_id]["vulnerable"] = bool_val

    def get_vulnerability_network(self):
        G = nx.Graph()
        for node in self.nodes():
            G.add_node(node)
            G.nodes[node]["vulnerable"] = self.nodes[node]["vulnerable"]
        for edge in self.edges():
                if self.nodes[edge[0]]["vulnerable"] and self.nodes[edge[1]]["vulnerable"]:
                    G.add_edge(edge[0],edge[1])
        return G
        
    def get_out_component_size(self, from_id):
        out_component_size = -1
        for node in self.nodes():
            if nx.has_path(self, from_id, node):
                out_component_size += 1
        return out_component_size
    
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
