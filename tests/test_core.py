from core.evolve.evolve import make_equilibrium_event, integrate
from core.system.system import network, double_fold
from core.system.coupling import linear_coupling

from scipy.integrate import odeint
import unittest
import numpy as np


class TestBasicFunctionality(unittest.TestCase):
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

    def test_equilibration(self):
        sys1 = double_fold(a = -4, b = 1, c = 0, x_0 = 0.5)
        sys2 = double_fold(a = -4, b = 1, c = 0, x_0 = 0.5)
        sys = (
            network()
            .add_element(sys1)
            .add_element(sys2)
            .add_coupling(0, 1, linear_coupling(strength=0.05))
            .add_coupling(1, 0, linear_coupling(strength=0.2))
        )
        event = make_equilibrium_event(sys, 0.001)
        sol = integrate(sys, [0.1, 0.9], [0, 10], 0.1, events=event)
        self.assertTrue(np.allclose(
            sol.y[:, -1],
            np.array([0.02790202, 1.00254695])
        ))

    def test_custom_strategy(self):
        def custom_strategy(f, x_init, t_span, opts):
            return odeint(f, x_init, t_span)

        sys1 = double_fold(a = -4, b = 1, c = 0, x_0 = 0.5)
        sys2 = double_fold(a = -4, b = 1, c = 0, x_0 = 0.5)
        sys = (
            network()
            .add_element(sys1)
            .add_element(sys2)
            .add_coupling(0, 1, linear_coupling(strength=0.05))
            .add_coupling(1, 0, linear_coupling(strength=0.2))
        )
        sol = integrate(sys, [0.1, 0.9], [0, 10], 0.1, strategy=custom_strategy)
        self.assertTrue(np.allclose(
            sol[-1, :],
            np.array([0.02567962, 1.06074957])
        ))
