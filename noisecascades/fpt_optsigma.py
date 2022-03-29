


import xarray as xr

from numba import jit
import numpy as np

import zarr
from numcodecs import Blosc

@jit(nopython=True)
def first_passage_index(vec):
    """return the index of the first occurence of item in vec"""
    for i in range(len(vec)):
        if vec[i] >= 0:
            return i
    return 0 #2*len(vec)


def add_FPT_to_cube(zarrpath = "optsigma_simulations.zarr"):


    cube = xr.open_zarr( zarrpath, consolidated = False)

    first_idx = xr.apply_ufunc(first_passage_index, cube, input_core_dims=[["time"]],vectorize = True, dask = 'parallelized').compute()

    FPT = cube.time.isel(time = (first_idx.to_array("vars").min("vars"))).drop(["time"]).rename("FPT").to_dataset()

    FPOktant = (((first_idx[["GIS", "THC", "WAIS"]].to_array("var") - first_idx[["GIS", "THC", "WAIS"]].to_array("var").min("var")) <= 0)*1).astype(str).str.join("var", "").to_dataset(name = "Oktant")

    zarrgroup = zarr.open_group(str(zarrpath))
 
    compressor = Blosc(cname='lz4', clevel=1)

    newds = zarrgroup.create_dataset("FPT", shape = (len(cube.config_id), len(cube.GMT), len(cube.strength), len(cube.alpha), len(cube.seed)), chunks = (1, 1, 1, 1, len(cube.seed)), dtype = 'float32', fillvalue = np.nan, compressor = compressor)
    newds.attrs['_ARRAY_DIMENSIONS'] = ("config_id", "GMT", "strength", "alpha", "seed")

    zarrgroup["FPT"][:] = FPT.FPT.values

    newds = zarrgroup.create_dataset("Oktant", shape = (len(cube.config_id), len(cube.GMT), len(cube.strength), len(cube.alpha), len(cube.seed)), chunks = (1, 1, 1, 1, len(cube.seed)), dtype = '<U3', fillvalue = '000', compressor = compressor)
    newds.attrs['_ARRAY_DIMENSIONS'] = ("config_id", "GMT", "strength", "alpha", "seed")

    zarrgroup["Oktant"][:] = FPOktant.Oktant.values


if __name__ == "__main__":

    add_FPT_to_cube()