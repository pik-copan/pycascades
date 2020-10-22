import time
import numpy as np
import networkx as nx
import glob
import re
import os

import csv
from netCDF4 import Dataset

#plotting imports
import matplotlib
matplotlib.use("Agg")


import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import seaborn as sns
sns.set(font_scale=2.5)
sns.set_style("whitegrid")


#self programmed code imports
import sys
sys.path.append('../modules/gen')
sys.path.append('../modules/core')
sys.path.append('amazon_code')
sys.path.insert(0,"../modules")

from networks import from_nxgraph
#from gen.net_factory import from_nxgraph
from amazon import generate_network
from evolve import evolve, NoEquilibrium
from tipping_element import cusp
from coupling import linear_coupling




#Tipping function
def tip( net , initial_state ):
    ev = evolve( net , initial_state )

    tolerance = 0.01
    t_step = 1
    #dc = 0.01
    realtime_break = 300000
    
    if not ev.is_equilibrium(tolerance):
        #This network is not in equilibrium since it[0] (= moisture transport) is not effectless at the current state of the network,
        print("Warning: Initial state is not a fixed point of the system")
    elif not ev.is_stable():
        print("Warning: Initial state is not a stable point of the system")

    ev.equilibrate(tolerance, t_step, realtime_break)

    conv_time = ev.get_timeseries()[0][-1] - ev.get_timeseries()[0][0]
    return conv_time, net.get_number_tipped(ev.get_timeseries()[1][-1,:]), net.get_tip_states(ev.get_timeseries()[1][-1])[:]




################################GLOBAL VARIABLES################################
no_cpl_dummy = False #no_cpl_dummy can be used to shut on or off the coupling; If True then there is no coupling, False with normal coupling
#################################################


sys_var = np.array(sys.argv[2:])
year = sys_var[0]



#GLOBAL VARIABLES
#critical value of mm/year before a state change occurs (Arie suggested: 800-1700mm/yr)
r_critical = np.arange(1700, 1800, 100)


data_eval = np.sort(np.array(glob.glob("data/*{}*.nc".format(year)))) #tree transpiration and interception evaporation

print(data_eval)



###MAIN###
for r_crit in r_critical:
    print("r_crit: ", r_crit)
    net = generate_network(r_crit, data_eval, no_cpl_dummy)

    output = []

    init_state = np.zeros(net.number_of_nodes())
    init_state.fill(-1) #initial state should be -1 instead of 0 everywhere

    #Without the source node tipped
    info = tip(net, init_state)
    conv_time = info[0]
    casc_size = info[1] 
    unstable_amaz = info[2]

    if no_cpl_dummy == True:
        np.savetxt("results/no_coupling/unstable_amaz_{}_rcrit{}_field.txt".format(year, r_crit), unstable_amaz)
        np.savetxt("results/no_coupling/unstable_amaz_{}_rcrit{}_total.txt".format(year, r_crit), [conv_time, casc_size])
    else:
        np.savetxt("results/unstable_amaz_{}_rcrit{}_field.txt".format(year, r_crit), unstable_amaz)
        np.savetxt("results/unstable_amaz_{}_rcrit{}_total.txt".format(year, r_crit), [conv_time, casc_size])


    #plotting procedure
    print("Plotting sequence")
    dataset = data_eval[0]
    net_data = Dataset(dataset)
    #latlon values
    lat = net_data.variables["lat"][:]
    lon = net_data.variables["lon"][:]


    tuples = [(lat[idx],lon[idx]) for idx in range(lat.size)]

    lat = np.unique(lat)
    lon = np.unique(lon)
    lat = np.append(lat, lat[-1]+lat[-1]-lat[-2]) #why do need to append lat[-1]+lat[-1]-lat[-2]???
    lon = np.append(lon, lon[-1]+lon[-1]-lon[-2])
    vals = np.empty((lat.size,lon.size))
    vals[:,:] = np.nan

    for idx,x in enumerate(lat):
        for idy,y in enumerate(lon):
            if (x,y) in tuples:
                p = unstable_amaz[tuples.index((x,y))]
                vals[idx,idy] = p


    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=25)

    plt.figure(figsize=(15,10))

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([275, 320, -22, 15], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE, linewidth=1)
    ax.coastlines('50m')
    cmap = plt.get_cmap('rainbow')

    plt.pcolor(lon-(lon[-1]-lon[-2]) / 2, lat-(lat[-1]-lat[-2]) / 2, vals, cmap=cmap)
    #nx.draw_networkx(net,pos, edge_color='black', node_size=0, with_labels=False)
    cbar = plt.colorbar(label='Unstable Amazon')


    if no_cpl_dummy == True:
        plt.savefig("results/no_coupling/unstable_amaz_{}_rcrit{}.png".format(year, r_crit), bbox_inches='tight')
        plt.savefig("results/no_coupling/unstable_amaz_{}_rcrit{}.pdf".format(year, r_crit), bbox_inches='tight')
    else:
        plt.savefig("results/unstable_amaz_{}_rcrit{}.png".format(year, r_crit), bbox_inches='tight')
        plt.savefig("results/unstable_amaz_{}_rcrit{}.pdf".format(year, r_crit), bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.close()


print("Finish")
