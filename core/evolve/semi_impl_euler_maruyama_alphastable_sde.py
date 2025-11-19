from numba import jit
from scipy.stats import levy_stable
import numpy as np
import warnings


def gen_levy_noise_preproc(alpha, sigma, dt, n = 1):
    if not isinstance(alpha, np.ndarray):
        if not isinstance(alpha, list):
            alpha = [alpha]
        alpha = np.array(alpha)
    if len(alpha) < n:
        alpha = np.repeat(alpha, n // len(alpha) + 1)[:n]
    if not isinstance(sigma, np.ndarray):
        if not isinstance(sigma, list):
            sigma = [sigma]
        sigma = np.array(sigma)
    if len(sigma) < n:
        sigma = np.repeat(sigma, n // len(sigma) + 1)[:n]
    return alpha, sigma, dt, n


@jit(nopython = True)
def semi_impl_euler_maruyama_alphastable_sde_nb_loop(
    n, N, x, xs, t, ts, dt_scaled, coupl, c, L, dt
):
    for i in range(1, N):
        x_new = x.copy()

        transp = (coupl @ x)
        for j in range(n):
            if (not np.isnan(x[j])) and (not np.isinf(x[j])):
                candidates = np.roots(np.array(
                    [
                        dt_scaled[j],
                        0.0,
                        1.0 - dt_scaled[j],
                        - x[j] - (c[j] + transp[j]) * dt_scaled[j]
                    ]
                ).astype(np.complex128))
                if (np.abs(candidates.imag) < 1e-5).sum() == 1:
                    drift = (
                        candidates[np.abs(candidates.imag) < 1e-5][0]
                    ).real
                else:
                    best_idx = np.argmin(np.abs(candidates - x[j]))
                    drift = (candidates[best_idx]).real
            else:
                drift = x[j]

            x_new[j] = drift + L[j, i]

            # x2 = x1 + (-x2^3 + x2 + c)*dt/taos

        t += dt
        ts[i] = t
        x = x_new   # .copy()
        xs[i, :] = x
    return ts, xs


def semi_impl_euler_maruyama_alphastable_sde(
    x0 = [-1.0, -1.0, -1.0],
    dt = 0.1,
    cs = [0.0, 0.3, 0.4],
    taos = [1.0, 1.0, 1.0],
    t_end = 1000,
    alphas = [1.5, 1.5, 1.5],
    sigmas = [0.0, 0.0, 0.1],
    coupl = np.array([[0.0, 0.1, 0.1], [-0.1, 0.0, 0.2], [0.0, -0.1, 0.0]]),
    rng = None
):
    if any(alphas) < 0.1:
        warnings.warn(
            """The CMS algorithm for generating levy-stable noise is not
            reliable for alphas < 0.1. The implementation provided here
            truncates large noise values above +-1e12 and sets any
            nans to 0."""
        )

    x0 = np.array(x0, dtype="float").flatten()
    taos = np.array(taos, dtype="float").flatten()
    cs = np.array(cs, dtype="float").flatten()
    alphas = np.array(alphas, dtype="float").flatten()
    sigmas = np.array(sigmas, dtype="float").flatten()
    coupl = np.array(coupl, dtype="float")

    alphas, sigmas, dt_scaled, n = gen_levy_noise_preproc(
        alphas, sigmas, dt / (taos + 1e-6), n = len(x0)
    )

    x = x0.copy()
    N = int(t_end // dt) + 1
    xs = np.zeros((N, n))
    xs[0, :] = x
    t = 0
    ts = np.zeros(N)

    L = np.zeros((n, N))
    for i in range(n):
        if sigmas[i] > 0:
            L[i, :] = (
                sigmas[i]
                * (dt_scaled[i] ** (1 / alphas[i]))
                * levy_stable.rvs(alphas[i], 0.0, size=N, random_state = rng)
            )
    L[np.abs(L) > 1e12] = (np.sign(L) * 1e12)[np.abs(L) > 1e12]
    L[np.isinf(L)] = (np.sign(L) * 1e12)[np.isinf(L)]
    L[np.isnan(L)] = 0.0

    ts, xs = semi_impl_euler_maruyama_alphastable_sde_nb_loop(
        n, N, x, xs, t, ts, dt_scaled, coupl, cs, L, dt
    )
    return ts, xs, rng


def get_params_from_es_network(net):

    n_nodes = net.number_of_nodes()

    cs = np.zeros(n_nodes)
    taos = np.zeros(n_nodes)
    coupl = np.zeros((n_nodes, n_nodes))

    for i in range(n_nodes):

        node = net.nodes[i]
        pars = node["data"].get_par()
        taos[i] = 1 / pars["b"]
        cs[i] = pars["c"] * taos[i]

        in_idxs = [e[0] for e in list(net.in_edges(i))]
        for j in in_idxs:
            if hasattr(net.get_edge_data(j, i)["data"], "_x_0"):
                x0 = net.get_edge_data(j, i)["data"]._x_0
            else:
                x0 = 0.0

            d = taos[i] * net.get_edge_data(j, i)["data"]._strength

            coupl[i, j] = d

            cs[i] += -x0 * d

    return cs, taos, coupl
