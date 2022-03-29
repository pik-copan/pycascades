
import pandas as pd
import numpy as np
import xarray as xr
from scipy.stats import wasserstein_distance
from tqdm import tqdm



def df_emd_over_n(zarrpath = "cfgs16_simulations.zarr"):

    cube = xr.open_zarr( zarrpath, consolidated = False)

    all_emds = []

    for n in tqdm([10, 20, 50, 100, 200, 500, 1000]):
        for config_id in cube.config_id.values:
            for alpha in cube.alpha.values:
                for sigma in cube.sigma.values:
                    for GMT in cube.GMT.values:
                        for strength in cube.strength.values:
                            n_slices = 10000//n
                            emds = []
                            for i_slice in range(n_slices):
                                run = cube.FPT.sel(config_id = config_id, alpha = alpha, sigma = sigma, GMT = GMT, strength = strength)
                                emd = wasserstein_distance(run.values, run.sel(seed = slice(i_slice*n, (i_slice+1)*n)).values)
                                emds.append(emd)
                            mean_emd = np.array(emds).mean()
                            all_emds.append(dict(n=n, config_id = config_id, alpha = alpha, sigma = sigma, GMT = GMT, strength = strength, emd = mean_emd))

    df = pd.DataFrame.from_records(all_emds)
    df.to_csv("emds_cfgs16.csv")


if __name__ == "__main__":

    df_emd_over_n()