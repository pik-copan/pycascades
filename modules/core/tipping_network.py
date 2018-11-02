from networkx import DiGraph

class tipping_network(DiGraph):

    def __init__(self, incoming_graph_data=None, **attr):
        DiGraph.__init__(self, incoming_graph_data=None, **attr)
        self._node_types = {}
        self._hopf_dict = {}

    def add_node(self, node_for_adding, **attr):

        super().add_node(node_for_adding, **attr)
        self._node_types.update({node_for_adding : attr['data'].get_type()})

        if attr['data'].get_type() == 'hopf':
            self._hopf_dict.update({attr['data'].get_id() : attr['data'].get_b()})

    
    def get_dxdt(self):
        dxdt_diag = []
        dxdt_cpl = []
        for idx in range(0,self.number_of_nodes()):
            dxdt_diag.append(self.node[idx]['data'].dxdt_diag())
            dxdt_row = []
            for in_edge in self.in_edges(nbunch=[idx],data=True):
                dxdt_row.append(
                        [in_edge[0],in_edge[1],in_edge[2]['data'].dxdt_cpl()])
            dxdt_cpl.append(dxdt_row)

        return { "diag" : dxdt_diag , "cpl" : dxdt_cpl }

    def get_jac(self):
        jac_diag = []
        n = self.number_of_nodes()           
        for idx in range(0,n):
            jac_diag.append(self.node[idx]['data'].jac_diag())
        
        jac_cpl = [[lambda t,x1,x2: 0 for j in range(n)] for i in range(n)]
        jac_diag_add = [[lambda t,x1,x2: 0 for j in range(n)] for i in range(n)]
        for edge in self.edges():
            jac_diag_add[edge[1]][edge[0]] = self.get_edge_data(edge[0],
                                                    edge[1])['data'].jac_diag()
            jac_cpl[edge[1]][edge[0]] = self.get_edge_data(edge[0]
                                                ,edge[1])['data'].jac_cpl()
        return { "diag" : jac_diag , "cpl" : jac_cpl , "diag_add" : jac_diag_add}
            
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
