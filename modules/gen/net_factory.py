from core.tipping_element import cusp
from core.coupling import linear_coupling
from core.tipping_network import tipping_network

class net_factory():
    def __init__(self):
        pass
    def create_one_cusp(self,a,b,c,initial_state):
        tc0 = cusp(0,a,b,c)
        tc0.update_state(initial_state)
        net = tipping_network()
        net.add_node(0,data=tc0)
        return net

    def create_cusp_chain(self,number,a,b,c,initial_state,cpl_strength
                          ,opt='uniform'):
        if opt == 'uniform':
            pass
        else:
            raise ValueError( 'Unrecognized option ' + opt )
        
        net = tipping_network()
        for id in range(0,number):
            tc = cusp(id,a,b,c)
            tc.update_state(initial_state)
            net.add_node(id,data=tc)

        for id in range(1,number):
            cpl = linear_coupling(cpl_strength,net.nodes[id-1]['data'])
            net.node[id]['data'].add_cpl(cpl)
            net.add_edge(id-1,id,weigth=cpl_strength)
            
            
        return net