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

import sys
sys.path.insert(0, "../modules")

"""Create two cusp tipping elements"""
from core.tipping_element import cusp
cusp_element_0 = cusp( a = -4, b = 1, c = 0, x_0 = 0.5 )
cusp_element_1 = cusp( a = -4, b = 1, c = 0, x_0 = 0.5 )

"""Create two linear couplings with strength 0.15 and 0.2"""
from core.coupling import linear_coupling
coupling_0 = linear_coupling( strength = 0.05 )
coupling_1 = linear_coupling( strength = 0.2 )


"""Create a tipping network and add the created elements"""
from core.tipping_network import tipping_network

net = tipping_network()

"""tipping_network is derived from networkx DiGraph class and all its methods
can be used, too."""
net.add_element( cusp_element_0 )
net.add_element( cusp_element_1 )
net.add_coupling( 0, 1, coupling_1 )
net.add_coupling( 1, 0, coupling_0 )

"""Plot the network with the plot_network function from utils module"""
from utils import plotter
plotter.network(net).show()

"""Plot phaseflow and phase space of a two-element system"""
plotter.phase_flow(net, xrange = [-0.2,1.2], yrange = [-0.2,1.2]).show()
plotter.phase_space(net, xrange = [-0.2,1.2], yrange = [-0.2,1.2]).show()
plotter.stability(net, xrange = [-0.2,1.2], yrange = [-0.2,1.2]).show()

"""Create an evolve module to simulate the tipping network 
as dynamical system"""
from core.evolve import evolve
initial_state = [0.1,0.9]
ev = evolve( net, initial_state )

"""Manually integrate the system"""
timestep = 0.01
t_end = 10
ev.integrate( timestep , t_end )

"""plot the temporal evolution"""
from utils import plotter
plotter.series( ev.get_timeseries()[0], ev.get_timeseries()[1][:,:] ).show()

"""Use the equilibrate method to end integration when an 
equilibrium is reached"""
ev = evolve( net , initial_state )

tol = 0.005
breaktime = 100

ev.equilibrate( tol, timestep, breaktime )
plotter.series( ev.get_timeseries()[0], ev.get_timeseries()[1][:,:] ).show()

"""Create a network with one cusp element and increase the control
until the tipping point is reached"""
initial_state = [0,0]

net = tipping_network()
net.add_element( cusp_element_0 )
net.add_element( cusp_element_1 )
net.add_coupling(0,1,coupling_1)
ev = evolve( net, initial_state )

dc = 0.005
while not net.get_tip_states(ev.get_timeseries()[1][-1,:]).any():
    ev.equilibrate( tol, timestep, breaktime )
    c = net.nodes[0]['data'].get_par()['c']
    net.set_param( 0, 'c', c+dc )

p=plotter.series( ev.get_timeseries()[0], ev.get_timeseries()[1][:,:]
                , legend=True).show()

"""Import networks module"""
from gen import networks
"""Use networkx graph generator"""
from networkx import erdos_renyi_graph
G = erdos_renyi_graph(10, 0.25, directed = True, seed = None)
net = networks.from_nxgraph( G, element_pool = [cusp_element_0],
                             coupling_pool = (0,0.2), coupling = 'uniform')

"""Create spatial graph with the networks module"""

net = networks.spatial_graph(100,0.4,0.1, element_pool=[cusp_element_0], 
                         coupling_pool=[coupling_0])
plotter.network(net, spatial=True).show()