#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tutorial on how to use the PyCascades Python 
framework for simulating tipping cascades on complex networks.
The core of PyCascades consists of the basic classes for 
tipping elements, couplings between them and a 
tipping_network class that contains information about
the network structure between these basic elements as well as
an evolve class, which is able to simulate the dynamics of a
tipping network.
"""
#self programmed code imports
import os
import sys
import re
import glob
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns
sns.set(font_scale=1.5)
sns.set_style("white")

import sys
sys.path.append('../modules/gen')
sys.path.append('../modules/core')
sys.path.append('../modules/utils')
sys.path.insert(0,"../modules")


import networkx as nx
import networks as nfac
import plotter
from tipping_element import cusp
from coupling import linear_coupling


cusp_element_0 = cusp( a = -4, b = 1, c = 0, x_0 = 0.5 )
coupling_0 = linear_coupling( strength = 0.05 )




#Erdös-Rényi
size = 15
degree = 3
rewiring_ws = 0.15

G = nx.erdos_renyi_graph(size, degree/size, directed = True, seed = None)
net = nfac.from_nxgraph( G, element_pool = [cusp_element_0], coupling_pool = [coupling_0])
print(net.number_of_edges() / net.number_of_nodes())
while net.number_of_edges() / net.number_of_nodes() < 2.9 or net.number_of_edges() / net.number_of_nodes() > 3.1:
	G = nx.erdos_renyi_graph(size, degree/size, directed = True, seed = None)
	net = nfac.from_nxgraph( G, element_pool = [cusp_element_0], coupling_pool = [coupling_0])


#Matplotlib Specifications
plt.xticks([])
plt.yticks([])
#plotter.network(net).savefig('figures/er.png')
#plotter.network(net).savefig('figures/er.pdf')
plotter.network(net).show()
#Average Degree
av_degree = net.number_of_edges() / net.number_of_nodes()
print(av_degree)



net = nfac.directed_watts_strogatz_graph(size, degree, rewiring_ws, element_pool = [cusp_element_0], coupling_pool = [coupling_0] )
#Matplotlib Specifications
plt.xticks([])
plt.yticks([])
#plotter.network(net).savefig('figures/ws.png')
#plotter.network(net).savefig('figures/ws.pdf')
plotter.network(net).show()
#Average Degree
av_degree = net.number_of_edges() / net.number_of_nodes()
print(av_degree)



net = nfac.directed_barabasi_albert_graph(size, degree, element_pool = [cusp_element_0], coupling_pool = [coupling_0] )
#Matplotlib Specifications
plt.xticks([])
plt.yticks([])
#plotter.network(net).savefig('figures/ba.png')
#plotter.network(net).savefig('figures/ba.pdf')
plotter.network(net).show()
#Average degree
av_degree = net.number_of_edges() / net.number_of_nodes()
print(av_degree)


print("Finish")
