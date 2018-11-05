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

"""Create two cusp tipping elements"""
from core.tipping_element import cusp

cusp_element_0 = cusp(id_number=0, a=-1, b=1)
cusp_element_1 = cusp(id_number=1, a=-1, b=2)

"""Create two linear couplings with strength 0.15 and 0.2"""
from core.coupling import linear_coupling

coupling_0 = linear_coupling(0.15)
coupling_1 = linear_coupling(0.15)

"""Create a tipping network and add the created elements"""
from core.tipping_network import tipping_network

net = tipping_network()

"""tipping_network is derived from networkx DiGraph class and all its methods
can be used, too."""
net.add_node(0, data=cusp_element_0)
net.add_node(1, data=cusp_element_1)
net.add_edge(0, 1, data=coupling_0)

"""You can plot the network with the plot_network function from utils module"""
from core import utils

utils.plot_network(net)

"""Look up the gen.net_factory module for some predefined
network generation functions and the core.evolve and 
cascades.cascade_lab modules to see how to simulate the dynamics 
of the network.
TODO: Extend the tutorial"""
