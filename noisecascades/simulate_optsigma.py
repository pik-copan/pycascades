import pandas as pd
import numpy as np
import xarray as xr
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import zarr
from numcodecs import Blosc

from noisecascades.trajectory_simulations import simulate_network_config
from noisecascades.network_configs import get_network_config

def simulate_network_config_from_vars(vars):
    config, GMT, strength, alpha_idx, config_idx, GMT_idx, strength_idx, n_runs = vars
    dss = []
    for seed in range(n_runs):
        dss.append(simulate_network_config(config, seed, GMT, strength, sigma_as_coord=False))
    ds = xr.merge(dss)
    zarrpath = "optsigma_simulations.zarr"
    zarrgroup = zarr.open_group(str(zarrpath))
    for var in ["GIS", "THC", "WAIS", "AMAZ"]:
        zarrgroup[var][:, config_idx, GMT_idx, strength_idx, alpha_idx, :] = ds[var].values[:,0,0,0,0,:]
    
def simulate_all_for_optsigma(n_runs = 20, configs_file = "network_configs.csv", timestep = 10., t_end = 100000):

    df = pd.read_csv(configs_file)


    coords = {
        "time": np.linspace(0, t_end, int(t_end // timestep) + 1),
        "config_id": sorted(df.config_id.unique()),
        "seed": range(n_runs),
        "GMT": sorted(df.GMT.unique()),
        "strength": sorted(df.strength.unique()),
        "alpha": sorted(df.alpha.unique())
    }
    
    print("Loading configs")
    vars = []
    for alpha in tqdm(df.alpha.unique()):
        for config_id in df.config_id.unique():
            for strength in df.strength.unique():
                for GMT in df.GMT.unique():
                    config = get_network_config(config_id = config_id, strength = strength, GMT = GMT, alpha = alpha, sigma = None, row_id = None, configs_file = configs_file)
                    alpha_idx = np.where(coords["alpha"] == alpha)[0][0]
                    config_idx = np.where(coords["config_id"] == config_id)[0][0]
                    GMT_idx = np.where(coords["GMT"] == GMT)[0][0]
                    strength_idx = np.where(coords["strength"] == strength)[0][0]
                    vars.append((config, GMT, strength, alpha_idx, config_idx, GMT_idx, strength_idx, n_runs))

    print("building dummy")
    ds = xr.Dataset(coords = coords)
    
    ds = ds.chunk(chunks={"time": -1, "config_id": 1, "seed": -1, "GMT": 1, "strength": 1, "alpha": 1})

    zarrpath = "optsigma_simulations.zarr"

    ds.to_zarr(zarrpath)

    zarrgroup = zarr.open_group(str(zarrpath))

    compressor = Blosc(cname='lz4', clevel=1)

    for var in ["GIS", "THC", "WAIS", "AMAZ"]:
        newds = zarrgroup.create_dataset(var, shape = (int(t_end // timestep) + 1, len(df.config_id.unique()), len(df.GMT.unique()), len(df.strength.unique()), len(df.alpha.unique()), n_runs), chunks = (int(t_end // timestep) + 1, 1, 1, 1, 1, n_runs), dtype = 'float32', fillvalue = np.nan, compressor = compressor)
        newds.attrs['_ARRAY_DIMENSIONS'] = ("time", "config_id", "GMT", "strength", "alpha", "seed")

    print("starting simulations")
    with ProcessPoolExecutor() as pool:
        _ = list(tqdm(pool.map(simulate_network_config_from_vars, vars), total = len(vars)))



# import zarr
# from numcodecs import Blosc
# import xarray as xr
# import rioxarray
# import numpy as np
# from pathlib import Path
# import rasterio
# from rasterio.enums import Resampling
# from rasterio.vrt import WarpedVRT
# from tqdm import tqdm
# import xml.etree.ElementTree as ET
# from concurrent.futures import ThreadPoolExecutor



# class Sen2DatacubeCreator:


#     SOILGRID_VARS = ["bdod", "cec", "cfvo", "clay", "nitrogen", "phh2o", "ocd", "sand", "silt", "soc"]

#     SOILGRID_DEPTH = ["0-5cm", "5-15cm", "15-30cm", "30-60cm", "60-100cm", "100-200cm"]

#     SOILGRID_VALS = ["mean", "uncertainty", "Q0.05", "Q0.5", "Q0.95"]


#     def __init__(self, basepath, outpath, silent = False):



#         self.basepath = Path(basepath)/"Sentinel/FullEurope/tiles"
#         self.basepath_static = Path(basepath)
#         self.outpath = Path(outpath)
#         self.outpath.mkdir(parents = True, exist_ok = True)

#         self.bands = {"blue": "B02", "green": "B03", "red": "B04", "nir": "B8A", "scl": "SCL"}
#         self.static = {"dem": ('float32', np.nan), "lc": ('uint8', 255), "geom": ('uint8', 0)}
#         self.layers = [f"{var}_{depth}_{val}" for var in self.SOILGRID_VARS for depth in self.SOILGRID_DEPTH for val in self.SOILGRID_VALS]
#         self.static_sg = {f"sg_{layer}": ('int16', -32768) for layer in self.layers}

#         self.silent = silent

#     @property
#     def possible_dates(self):
#         try:
#             return self._possible_dates
#         except AttributeError:
#             dates = np.arange('2017-03-01', '2021-03-01', 1, dtype='datetime64[D]')
#             quarters = np.arange('2017-03', '2021-06', 3, dtype='datetime64[M]')
#             i = 0
#             j = 0
#             k = 0
#             out = {}
#             for d in dates:
#                 if d >= quarters[i+1]:
#                     i+=1
#                     j = 0
#                     k = 0
#                 quarter = quarters[i]
#                 if d < quarter + np.timedelta64((j+1)*5):
#                     out[d] = [i, j]
#                 if k%5 == 4:
#                     j += 1
#                 k+=1
#             self._possible_dates = out
#             return out

#     def create_dummy(self, tile):

#         blueprint = rioxarray.open_rasterio(sorted(list((self.basepath/tile).glob("**/R20m_B02_0.jp2")))[-1])
#         blueprint = blueprint.isel({"x": slice(57,5433), "y": slice(57,5433)}) # Take center crop
#         # Fix geotrafo
#         geotransform = blueprint["spatial_ref"].attrs["GeoTransform"]
#         geotrafo = [float(g) for g in geotransform.split(" ")]
#         geotrafo[0] = geotrafo[0] + geotrafo[1] * 57
#         geotrafo[3] = geotrafo[3] + geotrafo[5] * 57
#         blueprint["spatial_ref"].attrs["GeoTransform"] = (" ").join([str(g) for g in geotrafo])

#         coords = {
#             "quarter": np.arange('2017-03', '2021-03', 3, dtype='datetime64[M]'),
#             "pentad": np.arange(0, 19*5, 5, dtype = 'timedelta64[D]'),
#             "y": blueprint.coords["y"].values,
#             "x": blueprint.coords["x"].values,
#             "spatial_ref": blueprint.coords["spatial_ref"].values
#         }

#         ds = xr.Dataset(coords = coords)
#         ds["x"].attrs = blueprint["y"].attrs
#         ds["y"].attrs = blueprint["y"].attrs
#         ds["spatial_ref"].attrs = blueprint["spatial_ref"].attrs
#         ds.attrs = blueprint.attrs
#         ds = ds.chunk(chunks=dict(quarter = 4, pentad=19, y=256, x=256))

#         zarrpath = self.outpath/f"{tile}.zarr"

#         ds.to_zarr(zarrpath)

#         zarrgroup = zarr.open_group(str(zarrpath))

#         compressor = Blosc(cname='lz4', clevel=1)

#         if not self.silent:
#             print("Building Dummy bands...")
#         for band in self.bands:
#             newds = zarrgroup.create_dataset(band, shape = (16,19,5376,5376), chunks = (4,19,256,256), dtype = 'float32', fillvalue = np.nan, compressor = compressor)
#             newds.attrs['_ARRAY_DIMENSIONS'] = ('quarter','pentad','x','y')
        
#         if not self.silent:
#             print("Building static dummies...")
#         for static in self.static:
#             dtype, fillvalue = self.static[static]
#             newds = zarrgroup.create_dataset(static, shape = (5376,5376), chunks = (1024,1024), dtype = dtype, fillvalue = fillvalue, compressor = compressor)
#             newds.attrs['_ARRAY_DIMENSIONS'] = ('x','y')

#         for static in self.static_sg:
#             dtype, fillvalue = self.static_sg[static]
#             newds = zarrgroup.require_dataset(static, shape = (5376,5376), chunks = (1024,1024), dtype = dtype, fillvalue = fillvalue, compressor = compressor)
#             newds.attrs['_ARRAY_DIMENSIONS'] = ('x','y')

#         newds = zarrgroup.create_dataset("date", shape = (16,19), chunks = (16,19), dtype = 'datetime64[D]', fillvalue = np.datetime64('nat'), compressor = compressor)
#         newds.attrs['_ARRAY_DIMENSIONS'] = ('quarter','pentad')

#         days = [np.datetime64(d.name) for d in (self.basepath/tile).iterdir()]

#         days_arr = np.full((16,19), np.datetime64('nat'), dtype = 'datetime64[D]')

#         for d in days:
#             if d in self.possible_dates:
#                 q, p = self.possible_dates[d]
#                 days_arr[q,p] = d
        
#         zarrgroup["date"][:,:] = days_arr
#         if not self.silent:
#             print("Done building dummy!")


#     def write_static(self, tile):

#         dem_path = self.basepath_static/"DEM"/"eudem_dem_3035_europe.tif"
#         lc_path = self.basepath_static/"S2GLC"/"S2GLC_Europe_2017_v1.2.tif"
#         geom_path = self.basepath_static/"Geomorphons"/"geom"/"geom_90M_full.tif"

#         zarrpath = self.outpath/f"{tile}.zarr"
#         zarrgroup = zarr.open_group(str(zarrpath))

#         blueprint = rasterio.open(sorted(list((self.basepath/tile).glob("**/R20m_B02_0.jp2")))[-1])
#         # Fix geotrafo
#         x1, x2, x0, y1, y2, y0, _, _, _ = list(blueprint.transform)
#         x0 = x0 + x1 * 57
#         y0 = y0 + y2 * 57

#         if not self.silent:
#             print("Writing DEM...")
#         with rasterio.open(dem_path) as src:
#             with WarpedVRT(src, crs=blueprint.crs, resampling=Resampling.bilinear) as vrt:
#                 dst_window = vrt.window(x0, y0 + 5376 * y2,x0 + 5376 * x1, y0)
#                 data = vrt.read(window=dst_window, out_shape=(1, 5376, 5376)).astype(np.float32)

#             zarrgroup["dem"][:,:] = data[0,...]

#         if not self.silent:
#             print("Writing LC...")
#         with rasterio.open(lc_path) as src:
#             with WarpedVRT(src, crs=blueprint.crs, resampling=Resampling.nearest) as vrt:
#                 dst_window = vrt.window(x0, y0 + 5376 * y2,x0 + 5376 * x1, y0)
#                 data = vrt.read(window=dst_window, out_shape=(1, 5376, 5376)).astype(np.uint8)

#             zarrgroup["lc"][:,:] = data[0,...]
        
#         if not self.silent:
#             print("Writing GEOM...")
#         with rasterio.open(geom_path) as src:
#             with WarpedVRT(src, crs=blueprint.crs, resampling=Resampling.nearest) as vrt:
#                 dst_window = vrt.window(x0, y0 + 5376 * y2,x0 + 5376 * x1, y0)
#                 data = vrt.read(window=dst_window, out_shape=(1, 5376, 5376)).astype(np.uint8)

#             zarrgroup["geom"][:,:] = data[0,...]
        
#         soilgrids_path = self.basepath_static/"soilgrids"/tile

#         if not self.silent:
#             print("Writing SOILGRIDS...")

#         for layer in self.layers:
#             sg_path = soilgrids_path/f"{layer}.tif"
            
#             with rasterio.open(sg_path) as src:
#                 zarrgroup[f"sg_{layer}"][:,:] = src.read(1)


#         if not self.silent:
#             print("Static vars Done!")

#     def write_sen2(self, tile):
        
#         dates = [np.datetime64(d.name) for d in (self.basepath/tile).iterdir()]

#         dates_per_chunk = [[d for d in dates if (d in self.possible_dates) and self.possible_dates[d][0]//4 == q] for q in (tqdm(range(4)) if not self.silent else range(4))]

#         # scores = {}
#         # for date in dates:
#         #     if date in self.possible_dates:
#         #         xml = ET.parse(self.basepath/tile/str(date)/"metadata0.xml")
#         #         qi = xml.find("{https://psd-14.sentinel2.eo.esa.int/PSD/S2_PDI_Level-2A_Tile_Metadata.xsd}Quality_Indicators_Info").find("Image_Content_QI")
#         #         metadata = {q.tag: q.text for q in list(qi)}

#         #         scores[date] = metadata['CLOUDY_PIXEL_PERCENTAGE'] + metadata['DEGRADED_MSI_DATA_PERCENTAGE'] + metadata['NODATA_PIXEL_PERCENTAGE'] + metadata['CLOUD_SHADOW_PERCENTAGE'] + metadata['DARK_FEATURES_PERCENTAGE'] + metadata['WATER_PERCENTAGE']

#         # best_date = min(scores, key = scores.get)

#         if not self.silent:
#             print("Loading Zarr...")
        
#         zarrpath = self.outpath/f"{tile}.zarr"
#         zarrgroup = zarr.open_group(str(zarrpath))

#         #quarters = np.arange('2017-03', '2021-03', 3, dtype='datetime64[M]')
#         #pentads = np.arange(0, 19*5, 5, dtype = 'timedelta64[D]')
        
#         for band in self.bands:
#             if not self.silent:
#                 print(f"Writing {band}...")
#             for chunk in (tqdm(dates_per_chunk) if not self.silent else dates_per_chunk):
#                 chunk_arr = np.full((4,19,5376,5376), np.nan, dtype = np.float32)
#                 for date in chunk:
#                     q, p = self.possible_dates[date]
#                     filepath = self.basepath/tile/str(date)/f"R20m_{self.bands[band]}_0.jp2"
#                     if filepath.is_file():
#                         with rasterio.open(filepath) as src:
#                             data = src.read().astype(np.float32)
#                             data[data == -9999.] = np.nan
#                             data = data / 10000
#                             data[data < 0] = 0
#                             data[data > 1] = 1
#                             chunk_arr[q%4,p,:,:] = data[0,57:5433,57:5433]
#                 zarrgroup[band][((q//4)*4):((q//4 + 1)*4),:,:,:] = chunk_arr
            


if __name__ == "__main__":

        simulate_all_for_optsigma()