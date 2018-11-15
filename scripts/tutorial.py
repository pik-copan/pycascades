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
cusp_element_0 = cusp( a = -4, b = 1, c = 0, x_0 = 0.5 )
cusp_element_1 = cusp( a = -4, b = 1, c = 0, x_0 = 0.5 )

"""Create two linear couplings with strength 0.15 and 0.2"""
from core.coupling import linear_coupling
coupling_0 = linear_coupling( strength = 0.15 )
coupling_1 = linear_coupling( strength = 0.2 )


"""Create a tipping network and add the created elements"""
from core.tipping_network import tipping_network

net = tipping_network()

"""tipping_network is derived from networkx DiGraph class and all its methods
can be used, too."""
net.add_element( cusp_element_0 )
net.add_element( cusp_element_1 )
#net.add_coupling( 0, 1, coupling_0 )
#net.add_coupling( 1, 0, coupling_1 )

"""Plot the network with the plot_network function from utils module"""
from utils import plotter
plotter.network(net)

"""Create an evolve module to simulate the tipping network 
as dynamical system"""
from core.evolve import evolve
initial_state = [0.75,0.25]
ev = evolve( net, initial_state )

"""Manually integrate the system"""
import matplotlib.pyplot as plt
timestep = 0.01
t_end = 10
ev.integrate( timestep , t_end )

"""plot the temporal evolution"""
plt.plot ( ev.get_timeseries()[0], ev.get_timeseries()[1][:,0] )
plt.plot ( ev.get_timeseries()[0], ev.get_timeseries()[1][:,1] )
plt.show()

"""Use the equilibrate method to end integration when an 
equilibrium is reached"""
ev = evolve( net , initial_state )

tol = 0.005
breaktime = 100

ev.equilibrate( tol, timestep, breaktime )
plt.plot ( ev.get_timeseries()[0], ev.get_timeseries()[1][:,0] )
plt.plot ( ev.get_timeseries()[0], ev.get_timeseries()[1][:,1] )
plt.show()

"""Create a network with one cusp element and increase the control
until the tipping point is reached"""
initial_state = [0]

net = tipping_network()
net.add_element( cusp_element_0 )
ev = evolve( net, initial_state )

dc = 0.01
while not net.get_tip_states(ev.get_timeseries()[1][-1,:]).any():
    ev.equilibrate( tol, timestep, breaktime )
    c = net.node[0]['data'].get_par()['c']
    net.set_param( 0, 'c', c+dc )

plt.plot ( ev.get_timeseries()[0], ev.get_timeseries()[1][:,0] )
plt.show()
    
"""Create networks with the net_factory module"""
from gen import net_factory as nfac

"""Same two node network as above"""
net = nfac.pair( cusp_element_0, cusp_element_1, coupling_0)
plotter.network(net)

"""Chain, ring and shamrock structure"""
net = nfac.chain( 5, element_pool = [cusp_element_0]
                   , coupling_pool = [coupling_0] )
plotter.network(net)
net = nfac.ring( 5, element_pool = [cusp_element_0]
                   , coupling_pool = [coupling_0] )
plotter.network(net)
net = nfac.shamrock( 4, 3, element_pool = [cusp_element_0]
                   , coupling_pool = [coupling_0] )
plotter.network(net)

"""Use networkx graph generator"""
from networkx import erdos_renyi_graph
G = erdos_renyi_graph( 10, 0.25, directed = True, seed = None)
net = nfac.from_nxgraph( G, element_pool = [cusp_element_0]
                          , coupling_pool = [coupling_0])
plotter.network(net)
