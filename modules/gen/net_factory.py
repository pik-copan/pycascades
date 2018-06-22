from core.tipping_element import cusp
from core.network import network
from core.coupling import linear_coupling

class net_factory():
    def __init__(self):
        pass
    def create_one_cusp(self,a,b,c,initial_state):
        tc0 = cusp(0,a,b,c)
        tc0.update_state(initial_state)
        net = network()
        net.add_element(tc0)
        return net

    def create_cusp_chain(self,number,a,b,c,initial_state,cpl_strength
                          ,opt='uniform'):
        if opt == 'uniform':
            pass
        else:
            raise ValueError( 'Unrecognized option ' + opt )
        
        net = network()
        for id in range(0,number):
            tc = cusp(id,a,b,c)
            tc.update_state(initial_state)
            net.add_element(tc)

        for id in range(1,number):
            cpl = linear_coupling(cpl_strength,net.tip_list[id-1])
            net.tip_list[id].add_cpl(cpl)
            
        return net