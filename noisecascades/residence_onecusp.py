import numpy as np
from numba import jit
from scipy.stats import levy_stable
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import seaborn as sb
from matplotlib.colors import LogNorm
import matplotlib as mpl
#from concurrent.futures import ThreadPoolExecutor
#from functools import partial

@jit(nopython = True)
def residence(x_init:float = 0.0, alpha:float = 2.0, tao:float = 1700.0, gamma:float = 1.0, N: int = int(1e7)):
#alpha, tao, gamma, N = 2.0, 1700.0, 1.0, 1e6
#if True:
    U = np.random.random_sample(size = N) * np.pi - np.pi/2
    W = -np.log(np.random.random_sample(size = N))#np.random.exponential(scale = 1.0, size = int(N))
    if alpha != 1.0:
        term1 = np.sin(alpha*U)/(np.cos(U)**(1/alpha))
        term2 = (np.cos(U - alpha*U)/W)**((1-alpha)/alpha)
        arr = gamma * term1 * term2
    else:
        arr = gamma * np.tan(U)
    #arr = levy_stable.rvs(alpha, 0.0, scale = 1/tao, size=int(1e7))#.cumsum()
    arr[0] = x_init
    for i in range(1, N):
        tmp = arr[i-1] + (arr[i] - arr[i-1]**3 + arr[i-1])/tao
        if tmp <= -1.0:
            arr[i] = -1.0
        elif tmp >= 1.0:
            arr[i] = 1.0
        else:
            arr[i] = tmp
    return np.mean(arr>0.0)

def est_residence(x_init:float = 0.0, alpha:float = 2.0, tao:float = 1700.0, gamma:float = 1.0, N: int = int(1e7), M: int = 100):
    idxs = np.zeros(M)
    for i in tqdm(range(M)):
        idxs[i] = residence(x_init = x_init, alpha = alpha, tao = tao, gamma = gamma, N = N)
    #curr_first_passage = lambda x: first_passage(alpha = alpha, tao = tao, gamma = gamma, N = N)
    #with ThreadPoolExecutor(max_workers=4) as pool:
        #idxs = list(tqdm(pool.map(curr_first_passage, range(M)),total = M))
    return np.mean(idxs)


def main():
    N = int(1e7)
    M = 100
    outdict = {"Element": [], "X0": [], "Tao": [], "Alpha": [], "Gamma": [], "Residence time": []}
    for x_init in [-0.9, -0.6, -0.3, -0.1, 0.0, 0.1, 0.3, 0.6, 0.9]:
        for j, tao in enumerate([1865.4339212188884, 114.21024007462583, 913.6819205970066, 19.035040012437637]):
            ele = ["GIS", "THC", "WAIS", "AMAZ"][j]
            for alpha in [0.5, 1.0, 1.5, 2.0]:#np.linspace(0.25, 2.0, 8):#np.linspace(0.1, 2.0, 20):#
                for gamma in [0.1, 1.0, 10.0]:#[0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0]:#
                    print(f"Tipping proba for x0 = {x_init}, tao = {tao}, alpha = {alpha}, gamma = {gamma}")
                    fraction = est_residence(x_init = x_init, alpha = alpha, tao = tao, gamma = gamma, N = N, M = M)
                    outdict["Element"].append(ele)
                    outdict["X0"].append(x_init)
                    outdict["Tao"].append(tao)
                    outdict["Alpha"].append(alpha)
                    outdict["Gamma"].append(gamma)
                    outdict["Residence time"].append(fraction)

    df = pd.DataFrame.from_dict(outdict)

    df.to_csv(f"residence_onecusp{M}.csv")

    #df = pd.read_csv(f"residence_onecusp{M}.csv")

    g = sb.FacetGrid(df, row="Element",  col = "X0")
    g.map_dataframe(lambda data, color: sb.heatmap(data.pivot("Alpha", "Gamma", "Residence time"), square=True, vmin = 0.0, vmax = 1.0, cbar = False))
    cbar_ax = g.fig.add_axes([1.015,0.13, 0.015, 0.8])
    plt.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=0.0, vmax=1.0), cmap = sb.color_palette("rocket", as_cmap=True)),cax=cbar_ax, label = "Residence time in tipped state")
    g.fig.savefig(f"residence_onecusp_TipTime.png", dpi = 200, facecolor='white', transparent=False, bbox_inches="tight")
    plt.clf()

if __name__ == "__main__":
    main()