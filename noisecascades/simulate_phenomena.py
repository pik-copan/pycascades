import pandas as pd
import numpy as np
import xarray as xr
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import zarr
from numcodecs import Blosc
import os
from numba import jit
import argparse

from noisecascades.trajectory_simulations import simulate_network_config
from noisecascades.network_configs import get_network_config


@jit(nopython=True)
def first_passage_index(vec):
    """return the index of the first occurence of item in vec"""
    for i in range(len(vec)):
        if vec[i] >= 0:
            return i
    return -1 #2*len(vec)


def simulate_network_config_from_vars(invars, verbose = False):
    configs, GMTs, strength, alpha_idx, config_idx, strength_idx, sigma_idx, n_runs = invars
    for GMT_idx, GMT in enumerate(GMTs):
        config = configs[GMT_idx]
        n_batches = n_runs // 50
        for batch in range(n_batches):
            dss = []
            for seed in range(50):#n_runs):
                dss.append(simulate_network_config(config, batch*50 + seed, GMT, strength, sigma_as_coord=True))
            ds = xr.merge(dss)

            cube = ds.sel(config_id = config["config_id"], GMT = GMT, strength = strength, alpha = config["alpha"], sigma = config["sigma"])

            first_idx = xr.apply_ufunc(first_passage_index, cube[["GIS", "THC", "WAIS"]], input_core_dims=[["time"]],vectorize = True)

            first_idx_sel = xr.where(first_idx == -1, len(cube.time)-1, first_idx)

            FPT = cube.time.isel(time = (first_idx_sel.to_array("vars").min("vars"))).drop(["time"])#.rename("FPT").to_dataset()

            FPT = xr.where(first_idx.to_array("vars").max("vars") == -1, np.nan, FPT).to_dataset(name = "FPT")

            FPOktant = (((first_idx_sel[["GIS", "THC", "WAIS"]].to_array("var") - first_idx_sel[["GIS", "THC", "WAIS"]].to_array("var").min("var")) <= 0)*1).astype(str).str.join("var", "")#.to_dataset(name = "Oktant")

            FPOktant = xr.where(first_idx.to_array("vars").max("vars") == -1, '000', FPOktant).to_dataset(name = "Oktant")

            zarrpath = os.environ["PTMP"]+"/noisecascades/phenomena_simulations.zarr"
            zarrgroup = zarr.open_group(str(zarrpath))
            zarrgroup["FPT"][config_idx, GMT_idx, strength_idx, alpha_idx, sigma_idx, batch*50:(batch+1)*50] = FPT.FPT.values
            zarrgroup["Oktant"][config_idx, GMT_idx, strength_idx, alpha_idx, sigma_idx, batch*50:(batch+1)*50] = FPOktant.Oktant.values

        if verbose:
            print(f"Done with GMT={GMT}, strength={strength}, alpha={config['alpha']}, sigma={config['sigma']}, config_id={config['config_id']}") 



def build_dummy(zarrpath = os.environ["PTMP"]+"/noisecascades/phenomena_simulations.zarr", sigmas = [0.1, 0.25], n_runs = 500, configs_file = "network_configs.csv", timestep = 10., t_end = 100000):

    df = pd.read_csv(configs_file)


    coords = {
        #"time": np.linspace(0, t_end, int(t_end // timestep) + 1),
        "config_id": sorted(df.config_id.unique()),
        "seed": range(n_runs),
        "GMT": sorted(df.GMT.unique()),
        "strength": sorted(df.strength.unique()),
        "alpha": sorted(df.alpha.unique()),
        "sigma": np.array(sigmas)
    }
    
    print("building dummy")
    ds = xr.Dataset(coords = coords)
    
    ds = ds.chunk(chunks={"config_id": 1, "seed": -1, "GMT": -1, "strength": 1, "alpha": 1, "sigma": 1})

    ds.to_zarr(zarrpath)

    zarrgroup = zarr.open_group(str(zarrpath))

    compressor = Blosc(cname='lz4', clevel=1)

    for var in ["FPT", "Oktant"]:
        newds = zarrgroup.create_dataset(var, shape = (len(df.config_id.unique()), len(df.GMT.unique()), len(df.strength.unique()), len(df.alpha.unique()), len(sigmas), n_runs), chunks = (1, len(df.GMT.unique()), 1, 1, 1, n_runs), dtype = 'float32', fillvalue = np.nan, compressor = compressor)
        newds.attrs['_ARRAY_DIMENSIONS'] = ("config_id", "GMT", "strength", "alpha", "sigma", "seed")

def simulate_all(node_idx = 0, zarrpath = "/p/tmp/vitusben/noisecascades/phenomena_simulations.zarr", sigmas = [0.1, 0.25], n_runs = 500, configs_file = "network_configs.csv", timestep = 10., t_end = 100000):

    df = pd.read_csv(configs_file)


    coords = {
        #"time": np.linspace(0, t_end, int(t_end // timestep) + 1),
        "config_id": sorted(df.config_id.unique()),
        "seed": range(n_runs),
        "GMT": sorted(df.GMT.unique()),
        "strength": sorted(df.strength.unique()),
        "alpha": sorted(df.alpha.unique()),
        "sigma": np.array(sigmas)
    }
    
    print("Loading configs")
    all_vars = []
    sim_idx = 0
    for alpha in tqdm(coords["alpha"]):
        for sigma in coords["sigma"]:
            for config_id in coords["config_id"]:
                if sim_idx == node_idx:
                    for strength in coords["strength"]:
                        configs = [get_network_config(config_id = config_id, strength = strength, GMT = GMT, alpha = alpha, sigma = None, row_id = None, configs_file = configs_file) for GMT in coords["GMT"]]
                        for config in configs:
                            config["sigma"] = sigma
                        alpha_idx = np.where(coords["alpha"] == alpha)[0][0]
                        config_idx = np.where(coords["config_id"] == config_id)[0][0]
                        strength_idx = np.where(coords["strength"] == strength)[0][0]
                        sigma_idx = np.where(coords["sigma"] == sigma)[0][0]
                        all_vars.append((configs, coords["GMT"], strength, alpha_idx, config_idx, strength_idx, sigma_idx, n_runs))
                sim_idx += 1


    # for invars in all_vars:
    #     simulate_network_config_from_vars(invars, verbose = True)

    print("starting simulations")
    with ProcessPoolExecutor(max_workers = 4) as pool:
        _ = list(tqdm(pool.map(simulate_network_config_from_vars, all_vars), total = len(all_vars)))




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='simulate some stuff..')

    parser.add_argument('node_idx', type=int, help='the node idx')

    args = parser.parse_args()

    if args.node_idx == -1:
        build_dummy()
    else:
        simulate_all(node_idx = args.node_idx)