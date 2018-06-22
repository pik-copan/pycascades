from core.tipping_element import cusp
from core.network import network

class net_factory():
    def __init__(self):
        pass
    def create_one_cusp(self,a,b,c,initial_state):
        tc0 = cusp(0,a,b,c)
        tc0.update_state(initial_state)
        net = network()
        net.add_element(tc0)
        return net		
