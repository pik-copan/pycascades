
import numpy as np 
import xarray as xr 
import pandas as pd
import pycascades as pc 


# TODO:

# 1) Get network config from pandas csv
# 2) Simulate for given random seed
# 3) Save to xarray dataset
# 4) Write merging tools for runs
# 5) Parallelize runs
# 6) possibly even run this on multiple cluster nodes
# 7) Load xarray dataset zarr..
# 8) Make 3d plots of multiple runs, put into large PDF <- bzw interactive widget
# 9) Compute statistics:
#    -> First passage time andere quadranten
#    -> Probability density in phase space
# 10) Focus again on basins...
#    -> get basin algorithm running
#    -> First passage time andere basins

# Saving structure - xarray dataset
# -> variables GIS, THC, WAIS (, AMAZ)
# -> coords time, Network config number, GMT, strength, seed


# Heute Abend noch:
# 1. Compute First passage time per Run + record to which quadrant
# 2. Make average plots of these...
# 3. Add First passage times into interactive widget as text
# 4. Make simulation functions for varying sigmas & start the simulations.
# 5. Fix simulations for fixed sigma: compute the sigma at GMT/strength == 0???


def simulate_network_config(network_config, seed, GMT, strength, timestep = 10., t_end = 100000, sigma_as_coord = True):

        # network_config = get_network_config(config_id)

        config_id = network_config["config_id"] #if 'Unnamed: 0' not in network_config else network_config['Unnamed: 0']

        limits_gis, limits_thc, limits_wais, limits_amaz = network_config["limits"]

        pf_wais_to_gis, pf_thc_to_gis, pf_gis_to_thc, pf_wais_to_thc, pf_thc_to_wais, pf_gis_to_wais, pf_thc_to_amaz = network_config["couplings"]

        kk = network_config["kk"]

        conv_fac_gis = 19.035040012437637

        gis_time, thc_time, wais_time, amaz_time = 98.0*conv_fac_gis, 6.0*conv_fac_gis, 48.0*conv_fac_gis, 1.0*conv_fac_gis

        sigma = network_config["sigma"]
        alpha = network_config["alpha"]

        sigmas = np.array(4*[sigma])
        alphas = np.array(4*[alpha])

        earth_system = pc.earth_system.Earth_System(gis_time, thc_time, wais_time, amaz_time,
                limits_gis, limits_thc, limits_wais, limits_amaz,
                pf_wais_to_gis, pf_thc_to_gis, pf_gis_to_thc,
                pf_wais_to_thc, pf_gis_to_wais, pf_thc_to_wais, pf_thc_to_amaz)

        net = earth_system.earth_network(GMT, strength, kk[0], kk[1])

        ev = pc.evolve_sde( net, [-1.,-1.,-1.,-1.])
        ev.integrate(timestep , t_end, sigmas = sigmas, alphas = alphas)
        ts = ev.get_timeseries()[0]
        xs = ev.get_timeseries()[1]

        GIS, THC, WAIS, AMAZ = xs[:,0], xs[:,1], xs[:,2], xs[:,3]

        if sigma_as_coord:
                dims = ("time", "config_id", "GMT", "strength", "alpha", "sigma", "seed")
                return xr.Dataset({"GIS": (dims, GIS[:,None,None,None,None,None,None]), "THC": (dims, THC[:,None,None,None,None,None,None]), "WAIS": (dims, WAIS[:,None,None,None,None,None,None]), "AMAZ": (dims, AMAZ[:,None,None,None,None,None,None])}, coords = {"time": ts, "config_id": [config_id], "GMT": [GMT], "strength": [strength], "alpha": [alpha], "sigma": [sigma], "seed": [seed]})
        else:
                dims = ("time", "config_id", "GMT", "strength", "alpha", "seed")
                return xr.Dataset({"GIS": (dims, GIS[:,None,None,None,None,None]), "THC": (dims, THC[:,None,None,None,None,None]), "WAIS": (dims, WAIS[:,None,None,None,None,None]), "AMAZ": (dims, AMAZ[:,None,None,None,None,None])}, coords = {"time": ts, "config_id": [config_id], "GMT": [GMT], "strength": [strength], "alpha": [alpha], "seed": [seed]})


