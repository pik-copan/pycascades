from scipy.integrate import solve_ivp
import numpy as np


def integrate(
    tipping_network,
    initial_state,
    t_span,
    t_step,
    strategy = None,
    **opts
):
    if strategy:
        sol = strategy(
            tipping_network.f,
            t_span,
            initial_state,
            opts,
        )
    else:
        sol = solve_ivp(
            lambda t, x : tipping_network.f(x, t),
            t_span,
            initial_state,
            t_eval=np.arange(t_span[0], t_span[1], step=t_step),
            events=opts.get("events", None)
        )
    return sol


def make_equilibrium_event(network, tol):
    def event(t, x):
        dxdt = network.f(x, t)
        res = np.any(np.abs(dxdt) > tol)
        return res
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
