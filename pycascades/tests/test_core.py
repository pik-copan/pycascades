from pycascades import cusp, linear_coupling, tipping_network
from pycascades.core.evolve.evolve import make_equilibrium_event, integrate

import unittest
import numpy as np


class TestBasicFunctionality(unittest.TestCase):
    def test_evolve(self):
        cusp_element_0 = cusp(a = -4, b = 1, c = 0, x_0 = 0.5)
        cusp_element_1 = cusp(a = -4, b = 1, c = 0, x_0 = 0.5)
        coupling_0 = linear_coupling(strength = 0.05)
        coupling_1 = linear_coupling(strength = 0.2)
        net = tipping_network()
        net.add_element(cusp_element_0)
        net.add_element(cusp_element_1)
        net.add_coupling(0, 1, coupling_1)
        net.add_coupling(1, 0, coupling_0)
        initial_state = [0.1, 0.9]
        t_end = 10
        sol = integrate(net, initial_state, [0, t_end], 0.1)
        self.assertTrue(np.allclose(
            sol.y[:, -1],
            np.array([0.02726913, 1.00262741])
        ))

    def test_equilibration(self):
        cusp_element_0 = cusp(a = -4, b = 1, c = 0, x_0 = 0.5)
        cusp_element_1 = cusp(a = -4, b = 1, c = 0, x_0 = 0.5)
        coupling_0 = linear_coupling(strength = 0.05)
        coupling_1 = linear_coupling(strength = 0.2)
        net = tipping_network()
        net.add_element(cusp_element_0)
        net.add_element(cusp_element_1)
        net.add_coupling(0, 1, coupling_1)
        net.add_coupling(1, 0, coupling_0)
        initial_state = [0.1, 0.9]
        t_end = 10
        event = make_equilibrium_event(net, 0.001)
        sol = integrate(net, initial_state, [0, t_end], 0.1, events=event)
        print(sol.y[:, -1])
        self.assertTrue(np.allclose(
            sol.y[:, -1],
            np.array([0.02790202, 1.00254695])
        ))
