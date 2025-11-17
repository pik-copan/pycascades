from pycascades.core.coupling import linear_coupling
from pycascades.core.evolve.evolve import make_equilibrium_event, integrate
from pycascades.core.system.system import network, double_fold

import unittest
import numpy as np


class TestBasicFunctionality(unittest.TestCase):
    def test_equilibration(self):
        sys1 = double_fold(a = -4, b = 1, c = 0, x_0 = 0.5)
        sys2 = double_fold(a = -4, b = 1, c = 0, x_0 = 0.5)
        net = (
            network()
            .add_element(sys1)
            .add_element(sys2)
            .add_coupling(0, 1, linear_coupling(strength=0.05))
            .add_coupling(1, 0, linear_coupling(strength=0.2))
        )
        initial_state = [0.1, 0.9]
        t_end = 10
        event = make_equilibrium_event(net, 0.001)
        sol = integrate(net, initial_state, [0, t_end], 0.1, events=event)
        self.assertTrue(np.allclose(
            sol.y[:, -1],
            np.array([0.02790202, 1.00254695])
        ))

    def test_system(self):
        sys1 = double_fold(a = -4, b = 1, c = 0, x_0 = 0.5)
        sys2 = double_fold(a = -4, b = 1, c = 0, x_0 = 0.5)
        sys = (
            network()
            .add_element(sys1)
            .add_element(sys2)
            .add_coupling(0, 1, linear_coupling(strength=0.05))
            .add_coupling(1, 0, linear_coupling(strength=0.2))
        )
        initial_state = [0.1, 0.9]
        sol = integrate(sys, initial_state, [0, 10], 0.1)
        self.assertTrue(np.allclose(
            sol.y[:, -1],
            np.array([0.02726913, 1.00262741])
        ))
