import sys
import unittest
import numpy as np
from pycascades import cusp, linear_coupling, tipping_network, evolve

class TestBasicFunctionality(unittest.TestCase):
    def test_simple_system(self):
        cusp_element_0 = cusp( a = -4, b = 1, c = 0, x_0 = 0.5 )
        cusp_element_1 = cusp( a = -4, b = 1, c = 0, x_0 = 0.5 )
        coupling_0 = linear_coupling( strength = 0.05 )
        coupling_1 = linear_coupling( strength = 0.2 )
        net = tipping_network()
        net.add_element( cusp_element_0 )
        net.add_element( cusp_element_1 )
        net.add_coupling( 0, 1, coupling_1 )
        net.add_coupling( 1, 0, coupling_0 )
        initial_state = [0.1,0.9]
        ev = evolve( net, initial_state )
        timestep = 0.01
        t_end = 10
        ev.integrate( timestep , t_end )
        np.set_printoptions(threshold=sys.maxsize)

        self.assertTrue(np.allclose(ev.get_timeseries()[1][-1,:], np.array([0.02725572, 1.00270361])))

