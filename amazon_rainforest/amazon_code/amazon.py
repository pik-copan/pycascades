import sys
sys.path.append('../../modules/gen')
sys.path.append('../../modules/core')
sys.path.append('')


from tipping_network import tipping_network
from tipping_element import cusp
from coupling import linear_coupling

#NW - my functions
from functions_amazon import global_functions


from netCDF4 import Dataset



import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=1.)
sns.set_style("whitegrid")


def generate_network(rain_crit, data_eval, no_cpl_dummy): 
    net = tipping_network()

    #get longitude and latitude values, for that use first network
    net_data = Dataset(data_eval[0])
    lon_x = net_data.variables["lon"][:]
    lat_y = net_data.variables["lat"][:]

    #rainfall value
    rain = global_functions.Rain(data_eval)
    rain_mean = np.nanmean(rain)

    for idx, val in enumerate(lon_x):
        #constants that are necessary to set up the tipping network
        rain_current = rain[idx] #rainfall in a certain cell
        rain_critical = rain_crit #critical rainfall of a certain cell

        a = 1
        b = 1
        element = cusp( a = -1, b = 1, c = global_functions.Amazon_CUSPc(a, b, rain_current, rain_critical, rain_mean), x_0 = 0)
        net.add_element(element)
        net.node[idx]['pos'] = (val, lat_y[idx])


    flows_xy_total = []
    for data in data_eval:
        data_file = Dataset(data)
        flows_xy_total.append(data_file.variables["network"][:, :])
    flows_xy_total = np.array(flows_xy_total)

    #compute total moisture recycling within a year
    flows_xy = Dataset(data_eval[0]).variables["network"][:, :]
    it = np.nditer(flows_xy, flags=['multi_index'])


    couplings = []
    while not it.finished:
        if not it.multi_index[0] == it.multi_index[1]:
            ###########
            #need to get value for each month
            monthly = []
            for i in range(0, len(flows_xy_total)):
                monthly.append(flows_xy_total[i, it.multi_index[0], it.multi_index[1]])

            appender = [it.multi_index[1], it.multi_index[0], np.sum(monthly)]
            for i in monthly:
                appender.append(i)
            couplings.append([i for i in appender])
        it.iternext()

    couplings = np.array(couplings)
    couplings = np.array(sorted(couplings, key=lambda x: x[2]))


    #sort out zero values in array
    cpl_hist = np.array(couplings).T[2]
    start_idx = len(couplings) - np.count_nonzero(cpl_hist)#count length of zeros
    couplings = np.array(couplings[start_idx:]) # sort out where couplings are zero



    #Resolution dependent coupling limit: Setting where couplings below cpl_limit mm/year are neglected; default value 1.0 mm
    cpl_limit = 1.0 # time to compute the new network sensitively depends on the coupling limit; 

    for cpl in couplings:
        if cpl[2] > cpl_limit:
            if no_cpl_dummy == True:
                coupling_object = linear_coupling(strength = 0.0)
            else:
                #get the difference between rainfall in the respective cell after[rain_new] and before[rain_old] tipping
                delta_rain = global_functions.Rain_moisture_delta_only([cpl[i] for i in range(3, len(cpl))]) #delta_rain is a negative number
                #current and critical values are required for the rainfall and mcwd
                rain_current = rain[int(cpl[1])]
                rain_critical = rain_crit

                #Amount of change of MCWD is the coupling strength
                coupling_object = linear_coupling(strength = global_functions.Amazon_cpl(a, b, rain_critical, rain_current, rain_mean, delta_rain))
            net.add_coupling( int(cpl[0]), int(cpl[1]), coupling_object ) #needs to be saved as integer here

    print("Amazon rainforest network generated! Restriction: Only moisture recycling links above {} mm/yr are considered".format(cpl_limit))
    d = net.number_of_edges() / net.number_of_nodes()
    average_clustering = nx.average_clustering(net)
    #print("Average degree: ", d)
    #print("Average clustering: ", average_clustering)
    return net