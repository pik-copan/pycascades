#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tutorial on how to use the PyCascades Python 
package for complex tipping networks.
The core of PyCascades consists of the basic classes for 
tipping elements, couplings between them and a 
tipping_network class that contains information about
the network structure between these basic elements as well as
an evolve class, which is able to simulate the dynamics of a
tipping network.
"""

import networkx as nx
import matplotlib.pyplot as plt


"""Create two cusp tipping elements"""
from core.tipping_element import cusp
cusp_element_0 = cusp( a = -4, b = 1, c = 0, x_0 = 0.5 )
cusp_element_1 = cusp( a = -4, b = 1, c = 0, x_0 = 0.5 )

"""Create two linear couplings with strength 0.15 and 0.2"""
from core.coupling import linear_coupling
coupling_0 = linear_coupling( strength = 0.05 )
coupling_1 = linear_coupling( strength = 0.2 )


"""Create a tipping network and add the created elements and couplings"""
from core.tipping_network import tipping_network

net = tipping_network()
net.add_element( cusp_element_0 )
net.add_element( cusp_element_1 )
net.add_coupling( 0, 1, coupling_1 )
net.add_coupling( 1, 0, coupling_0 )

"""tipping network is derived from the DiGraph class of networkx.
Therefore, networkx functions can be applied to tipping_network objects.
Here, the created network is plotted with the function draw_networkx."""
nx.draw_networkx(net, with_labels=True)
plt.show()

"""Create an evolve module to simulate the tipping network 
as dynamical system"""
from core.evolve import evolve
initial_state = [0.2,0.8]
ev = evolve( net, initial_state )

"""Manually integrate the system"""
timestep = 0.01
t_end = 10
ev.integrate( timestep , t_end )

plt.plot( ev.get_timeseries()[0], ev.get_timeseries()[1][:,0] )
plt.plot( ev.get_timeseries()[0], ev.get_timeseries()[1][:,1] )
plt.xlabel('t')
plt.ylabel('x')
plt.show()

"""Use the equilibrate method to end integration when an 
equilibrium is reached"""
ev = evolve( net , initial_state )

tol = 0.005
breaktime = 100

ev.equilibrate( tol, timestep, breaktime )

plt.plot( ev.get_timeseries()[0], ev.get_timeseries()[1][:,0] )
plt.plot( ev.get_timeseries()[0], ev.get_timeseries()[1][:,1] )
plt.xlabel('t')
plt.ylabel('x')
plt.show()

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
    c = net.node[0]['data'].get_par()['c']
    net.set_param( 0, 'c', c+dc )

plt.plot( ev.get_timeseries()[0], ev.get_timeseries()[1][:,0] )
plt.plot( ev.get_timeseries()[0], ev.get_timeseries()[1][:,1] )
plt.xlabel('t')
plt.ylabel('x')
plt.show()
    
"""Create random Erdos-Renyi network with net_factory"""
from gen import net_factory

node_number = 50
link_probability = 0.05
er_graph = net_factory.erdos_renyi_graph(element_pool = [cusp_element_0],
                                         coupling_pool = [coupling_0],
                                         seed = None)
net = er_graph.create(node_number, link_probability)

nx.draw_circular(net, with_labels=False)
plt.show()