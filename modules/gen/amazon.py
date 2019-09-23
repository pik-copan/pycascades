#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 14:09:40 2019

Create network from amazon data from Staal 2018 paper.

@author: kroenke
"""

from core.tipping_network import tipping_network
from core.tipping_element import cusp
from core.coupling import linear_coupling

import networkx as nx
import numpy as np

def generate_network(net_data, average_degree, coupling=1, cpl_mode='read'):
    net = tipping_network()
    element = cusp( a = -4, b = 1, c = 0, x_0 = 0.5 )
    
    lon_x = net_data.variables["lon"][:]
    lat_y = net_data.variables["lat"][:]
    for idx, val in enumerate(lon_x):
        net.add_element( element )
        net.node[idx]['pos'] = (val, lat_y[idx])
    
    rain = net_data.variables["rain"][:]
    """
    rain_mean = np.nanmean(rain)
    inds = np.where(np.isnan(rain))
    rain[inds]= rain_mean
    """
    flows_xy = net_data.variables["network"][:,:]
    it = np.nditer(flows_xy, flags=['multi_index'])
    couplings = []
    while not it.finished:
        if not it.multi_index[0] == it.multi_index[1]:
            couplings.append((it.multi_index[1],
                              it.multi_index[0],
                              coupling * it[0] / rain[it.multi_index[0]],
                              it[0], rain[it.multi_index[0]], rain[it.multi_index[1]]))
        it.iternext()

    desired_edge_number = round(average_degree * net.number_of_nodes())
    start_idx = len(couplings) - desired_edge_number

    couplings = sorted(couplings, key=lambda x: x[2])
    couplings = couplings[start_idx:]   
    for cpl in couplings:
        if cpl_mode == 'homogenous':
            cpl_val = coupling
        else:
            cpl_val = cpl[2]
        coupling_object = linear_coupling(cpl_val)
        net.add_coupling( cpl[0], cpl[1], coupling_object )

    print("Amazon rain forest network generated!")
    d = net.number_of_edges() / net.number_of_nodes()
    average_clustering = nx.average_clustering(net)
    print("Average degree: ", d )
    print("Average clustering: ", average_clustering )
    return net