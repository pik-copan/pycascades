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
def trajectories(x_init:float = -1.0, alpha:float = 2.0, ele_idx:int = 0, gamma:float = 1.0, N: int = int(1e7), coupl = np.array([[0.0,-0.5,0.2,0.0],[0.3, 0.0, 0.1, 0.0],[0.25,0.1,0.0,0.0],[0.0,0.35,0.0,0.0]]), lamb: float = 1.0):
#alpha, tao, gamma, N = 2.0, 1700.0, 1.0, 1e6
#if True:
    taos = np.array([1865.4339212188884, 114.21024007462583, 913.6819205970066, 19.035040012437637])
    U = np.random.random_sample(size = N) * np.pi - np.pi/2
    W = -np.log(np.random.random_sample(size = N))#np.random.exponential(scale = 1.0, size = int(N))
    if alpha != 1.0:
        term1 = np.sin(alpha*U)/(np.cos(U)**(1/alpha))
        term2 = (np.cos(U - alpha*U)/W)**((1-alpha)/alpha)
        arr = gamma * term1 * term2
    else:
        arr = gamma * np.tan(U)
    #arr = levy_stable.rvs(alpha, 0.0, scale = 1/tao, size=int(1e7))#.cumsum()
    out_simple = np.zeros_like(arr)
    out_cusp = np.zeros_like(arr)
    out_simple[0] = x_init
    out_cusp[0] = x_init
    out_wunder = np.zeros((N, 4))
    out_wunder[0, :] = -1.0
    out_wunder[0,ele_idx] = x_init
    for i in range(1, N):
        tmp = out_cusp[i-1] + (arr[i] - out_cusp[i-1]**3 + out_cusp[i-1])/taos[ele_idx]
        if tmp <= -1.0:
            out_cusp[i] = -1.0
        elif tmp >= 1.0:
            out_cusp[i] = 1.0
        else:
            out_cusp[i] = tmp
        tmp = out_simple[i-1] + arr[i]/taos[ele_idx]
        if tmp <= -1.0:
            out_simple[i] = -1.0
        elif tmp >= 1.0:
            out_simple[i] = 1.0
        else:
            out_simple[i] = tmp

        for j in range(4):
            tmp = out_wunder[i-1, j] + (out_wunder[i-1, j]**3 + out_wunder[i-1, j])/taos[j]
            if j == ele_idx:
                tmp += arr[i] / taos[j]
            for k in range(4):
                tmp += lamb/taos[j] * coupl[j,k] * (out_wunder[i-1,k] + 1)
            if tmp <= -1.0:
                out_wunder[i, j] = -1.0
            elif tmp >= 1.0:
                out_wunder[i, j] = 1.0
            else:
                out_wunder[i, j] = tmp
            
        
    return out_simple, out_cusp, out_wunder



def main():
    df = pd.read_csv("first_passage_simple100.csv")

    for x_init in tqdm([-0.9, -0.6, -0.3, -0.1, 0.0, 0.1, 0.3, 0.6, 0.9]):
        for lamb in [0.1, 1.0, 10.0, 100.0]:
            for _, row in df.iterrows():
                tao = row["Tao"]
                ele = row["Element"]
                ele_idx = {"GIS": 0, "THC": 1, "WAIS": 2, "AMAZ": 3}[ele]
                alpha = row["Alpha"]
                gamma = row["Gamma"]
                N = min(2e5, max(1000, 20 * row["Mean"]))
                out_simple, out_cusp, out_wunder = trajectories(x_init = x_init, alpha = alpha, ele_idx = ele_idx, gamma = gamma, N = int(N), lamb = lamb)
                x = range(int(N))
                fig = plt.figure(dpi = 200)
                plt.plot(x, out_simple, label = "Simple Levy Noise")
                plt.plot(x, out_cusp, label = "Levy Noise with Cusp")
                plt.plot(x, out_wunder[:,ele_idx], label = "Levy Noise /w Cusp & Coupling")
                plt.ylim([-1.0, 1.0])
                plt.legend()
                fig.savefig(f"traj_wunderling_plots/{ele}_x={x_init}_a={alpha}_g={gamma}_l={lamb}.png", dpi = 200, facecolor='white', transparent=False, bbox_inches="tight")
                plt.close(fig)
                fig = plt.figure(dpi = 200)
                plt.plot(x, out_wunder)
                plt.ylim([-1.1, 1.1])
                plt.legend(["GIS", "THC", "WAIS", "AMAZ"])
                fig.savefig(f"traj_wunderling_plots/wunderlingnet_{ele}_x={x_init}_a={alpha}_g={gamma}_l={lamb}.png", dpi = 200, facecolor='white', transparent=False, bbox_inches="tight")
                plt.close(fig)

if __name__ == "__main__":
    main()