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

def generate_network(net_data, average_degree, coupling_factor=0.01):
    net = tipping_network()
    element = cusp( a = -4, b = 1, c = 0, x_0 = 0.5 )
    
    lon_x = net_data.variables["lon"][:]
    lat_y = net_data.variables["lat"][:]
    for idx, val in enumerate(lon_x):
        net.add_element( element )
        net.node[idx]['pos'] = (val, lat_y[idx])
    
    flows_xy = net_data.variables["network"][:,:]
    it = np.nditer(flows_xy, flags=['multi_index'])
    couplings = []
    while not it.finished:
        couplings.append((it.multi_index[0], 
                          it.multi_index[1], 
                          coupling_factor * it[0]))
        it.iternext()

    desired_edge_number = round(average_degree * net.number_of_nodes())
    start_idx = len(couplings) - desired_edge_number

    couplings = sorted(couplings, key=lambda x: x[2])
    couplings = couplings[start_idx:]
    
    for cpl in couplings:
        coupling = linear_coupling(cpl[2])
        net.add_coupling( cpl[0], cpl[1], coupling )

    print("Amazon rain forest network generated!")
    d = net.number_of_edges() / net.number_of_nodes()
    average_clustering = nx.average_clustering(net)
    print("Average degree: ", d )
    print("Average clustering: ", average_clustering )
    return net
