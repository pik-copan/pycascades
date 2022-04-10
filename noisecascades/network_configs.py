
import ast
import numpy as np
import pandas as pd
import pycascades as pc
import xarray as xr
from tqdm import tqdm
from numba import jit
from copy import deepcopy


from noisecascades.trajectory_simulations import simulate_network_config

@jit(nopython=True)
def find_first_pos(vec):
    """return the index of the first occurence of item in vec"""
    for i in range(len(vec)):
        if vec[i] >= 0:
            return i
    return 0 #2*len(vec)


NETWORK_CONFIGS = [
    {
        "name": "classic", 
        "config_id": 0,
        #"GMT": 3.0, 
        "limits": [1.5, 4.0, 1.5, 4.0], 
        "couplings": [0.1, -0.5, 0.5, 0.12, 0.05, 0.5, 0.3], 
        "kk": [-1.0, -1.0],
        # "alpha": 1.5,
        # "sigma": 1.0
        }, 
    {
        "name": "oscillating",
        "config_id": 1,
        #"GMT": 2.0, 
        "limits": [2.715278762405562318e+00, 5.591667511790497258e+00, 2.006511324102656868e+00, 3.871773585368268655e+00], 
        "couplings": [1.079841584751979472e-01, 4.672455575473318801e-01, 5.305103830254412900e-01, 2.662379125466165508e-01, 1.070763107753331944e-01, 6.701966126655601874e-01, 3.068899226037242745e-01], 
        "kk": [-1.0, -1.0],
        # "alpha": 1.5,
        # "sigma": 1.0
        }
]



def get_sigma_for_Pt(config, Pt = 1000, rel_tol = 0.1, max_iter = 6):
    tmp_config = deepcopy(config)
    done = False

    iter = 0
    best_sigma = tmp_config["sigma"]
    dist_best_sigma = Pt

    fac = 10
    mode = "start"

    while not done:
        dss = []
        for seed in range(20):
            dss.append(simulate_network_config(tmp_config, seed, tmp_config["GMT"], tmp_config["strength"], timestep = 10., t_end = 10*Pt))

        ds = xr.merge(dss)
        first_idx = xr.apply_ufunc(find_first_pos, ds, input_core_dims=[["time"]],vectorize = True)
        mPt = 10*float(first_idx.to_array("vars").min("vars").mean().values)
        
        #print(mPt, tmp_config["sigma"])

        dist = abs(mPt - Pt)
        if (mPt - Pt) > rel_tol*Pt:
            if mode == "decr":
                fac /= 2
            tmp_config["sigma"] *= fac
            mode = "incr"
        elif (Pt - mPt) > rel_tol*Pt:
            if mode == "incr":
                fac /= 2
            tmp_config["sigma"] /= fac
            mode = "decr"
        else:
            done = True

        if dist < dist_best_sigma:
            best_sigma = tmp_config["sigma"]

        if iter >= max_iter:
            tmp_config["sigma"] = best_sigma
            done = True

        iter += 1

    return tmp_config


def generate_network_configs(base_configs, GMTs, strengths, alphas, sigmas = None):

    configs_list = []

    for base_config in base_configs:
        print(base_config)
        for GMT in GMTs:
            print(f"GMT = {GMT}")
            for strength in tqdm(strengths):

                for alpha in alphas:
                    
                    if alpha == 0.0:
                        configs_list.append({**base_config, **{"GMT": GMT, "strength": strength, "sigma": 0.0, "alpha": 2.0}})
                    else:
                        if sigmas is None:
                            configs_list.append(get_sigma_for_Pt({**base_config, **{"GMT": GMT, "strength": strength, "sigma": 0.1, "alpha": alpha}}, Pt = 1000))
                        else:
                            for sigma in sigmas:
                                if sigma is None:
                                    configs_list.append(get_sigma_for_Pt({**base_config, **{"GMT": GMT, "strength": strength, "sigma": 0.1, "alpha": alpha}}, Pt = 1000))
                                else:
                                    configs_list.append({**base_config, **{"GMT": GMT, "strength": strength, "sigma": sigma, "alpha": alpha}})

    df = pd.DataFrame.from_records(configs_list)

    df.to_csv("network_configs.csv")

    return df


def get_network_config(config_id = 0, strength = 0.0, GMT = 0.0, alpha = 2.0, sigma = None, row_id = None, configs_file = "network_configs.csv"):

    df = pd.read_csv(configs_file)

    if row_id is not None:
        row = df.iloc[row_id]
    elif sigma is None:
        row = df[(df.config_id == config_id) & (df.alpha == alpha) & (df.strength == strength) & (df.GMT == GMT)].iloc[0 if alpha != 2.0 else 1]
    else:
        row = df[(df.config_id == config_id) & (df.alpha == alpha) & (df.sigma == sigma) & (df.strength == strength) & (df.GMT == GMT)].iloc[0]

    network_config = {k: ast.literal_eval(v) if k in ["limits", "couplings", "kk"] else v for k,v in row.to_dict().items()} #NETWORK_CONFIGS[config_id]

    return network_config



if __name__ == "__main__":

    #generate_network_configs(NETWORK_CONFIGS, GMTs = [0.0, 1.5, 3.0], strengths = [0.0, 0.5, 1.0], alphas = np.array([0.0, 0.5, 1.0, 1.5, 2.0]), sigmas = [None, 0.01, 0.1, 1.0, 10.0])

    #generate_network_configs(NETWORK_CONFIGS, GMTs = np.linspace(0.0, 4.0, 41), strengths = np.linspace(0.0, 1.0, 21), alphas = np.array([0.0, 0.5, 1.0, 1.5, 2.0]), sigmas = [None, 0.01, 0.1, 1.0, 10.0])

    generate_network_configs(NETWORK_CONFIGS, GMTs = np.linspace(0.0, 4.0, 41), strengths = np.linspace(0.0, 1.0, 21), alphas = np.array([0.0, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]), sigmas = [0.1, 0.25])