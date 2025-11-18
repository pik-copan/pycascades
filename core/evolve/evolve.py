from . import semi_impl_euler_maruyama_alphastable_sde
from . import itoint

from scipy.integrate import solve_ivp
import numpy as np


class NoEquilibrium(Exception):
    pass


def integrate(
    tipping_network,
    initial_state,
    t_span,
    t_step,
    backend = "solve_ivp",
    **opts
):
    match backend:
        case "solve_ivp":
            sol = solve_ivp(
                lambda t, x : tipping_network.f(x, t),
                t_span,
                initial_state,
                t_eval=np.arange(t_span[0], t_span[1], step=t_step),
                events=opts.get("events", None)
            )
        case "itoint":
            for opt in ["sigma", "noise"]:
                if opt not in opts:
                    raise Exception(f'Keyword Argument {opt} missing')

            sol = itoint(
                tipping_network.f,
                lambda x, t: opts["sigma"],
                initial_state,
                t_span,
                noise = opts["noise"]
            )
        case "duffing":
            for opt in ["cs", "taos", "alphas", "sigmas", "coupl"]:
                if opt not in opts:
                    raise Exception(f'Keyword Argument {opt} missing')

            sol = semi_impl_euler_maruyama_alphastable_sde(
                x0 = t_span[0],
                dt = t_step,
                cs = opts["cs"],
                taos = opts["taos"],
                t_end = t_span[1],
                alphas = opts["alphas"],
                sigmas = opts["sigmas"],
                coupl = opts["coupl"],
                rng = opts.get("rng", None)
            )
    return sol


def make_equilibrium_event(network, tol):
    def event(t, x):
        dxdt = network.f(x, t)
        return np.linalg.norm(dxdt) - tol
    event.terminal = True
    event.direction = 0
    return event


def is_equilibrium(f, t, x, tol):
    """Check if the system is in an equilibrium state, e.g. if the
    absolute value of all elements of f (f is dxdt) is less than tolerance.
    If True the state can be considered as close to a fixed point"""
    dxdt = f(x, t)
    n = len(dxdt)
    fix = np.less(np.abs(dxdt), tol * np.ones(n))

    if fix.all():
        return True
    else:
        return False


def is_stable(jacobian, t, x):
    """Check stability of current system state by calculating the
    eigenvalues of the jacobian (all eigenvalues < 0 => stable)."""
    jac_values = jacobian(x, t)
    n = len(jac_values)
    val, vec = np.linalg.eig(jac_values)
    stable = np.less(val, np.zeros(n))

    if stable.all():
        return True
    else:
        return False
