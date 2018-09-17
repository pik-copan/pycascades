from networkx import DiGraph

class tipping_network(DiGraph):
    
    def get_dxdt_vec(self):
        df = []
        for node in self.nodes():
            f_prime = [self.node[node]['data'].dxdt_diag()]
            df.append(f_prime)
            
        for edge in self.edges(data=True):
            to_node = edge[1]
            df[to_node].append((edge[2]['data'].dxdt_cpl(),edge[0]))
        return df

    def get_jac(self):
        jac_diag = []
        for idx in range(0,self.number_of_nodes()):
            jac_diag.append(self.node[idx]['data'].jac_diag())
        
        n = self.number_of_nodes()
        jac_cpl = [[lambda x1,x2: 0 for j in range(n)] for i in range(n)]
        for edge in self.edges():
            print(edge)
            jac_cpl[edge[1]][edge[0]] = self.get_edge_data(edge[0]
                                                    ,edge[1])['data'].jac_cpl()
        return { "diag" : jac_diag , "cpl" : jac_cpl }
            
    def get_adjusted_bif_par_vec( self , bif_par_eff_vec , initial_state ):
        """Adjust bifurcation parameter so that the sum of coupling and
        bifurcation parameter (effective bifurcation parameter) 
        equals bif_par_eff_vec"""
        bif_par_vec = []
        for to_id in range(0,self.number_of_nodes()):
            cpl_sum = bif_par_eff_vec[to_id]
            for from_id in range(0,self.number_of_nodes()):
                if not self.get_edge_data(from_id,to_id) == None:
                    cpl_sum += -self.get_edge_data(from_id,to_id)['data'].dxdt_cpl().__call__( initial_state[from_id] , initial_state[to_id] )
            
            bif_par_vec.append(cpl_sum)
        return bif_par_vec
    