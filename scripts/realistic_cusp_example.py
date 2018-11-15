#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 13:21:50 2018

@author: jonathan
"""
from core.tipping_element import realistic_cusp
from core.tipping_network import tipping_network
from core.evolve import evolve

import matplotlib.pyplot as plt
# Parameter for GIS
t_scale = 300          # timescale in years
x = (0,7)              # Sea levels for untipped and tipped states
c = (0.8,3.2)          # bistable range

cusp1 = realistic_cusp( t_scale, x, c, rho_init = 2)

initial_state = [0]

net = tipping_network()
net.add_element( cusp1 )
ev = evolve( net, initial_state )

tol = 0.005 / t_scale
timestep = 0.1 * t_scale
breaktime = 100

delta_rho = 0.005

while not net.get_tip_states(ev.get_timeseries()[1][-1,:]).any():
    rho = net.node[0]['data'].get_par()['rho']
    net.set_param( 0, 'rho', rho + delta_rho )
    t0 = ev._t
    ev.equilibrate( tol, timestep, breaktime )
    eq_time = ev._t - t0

print(eq_time)
plt.plot(ev.get_timeseries()[0][:], ev.get_timeseries()[1][:,0])
plt.show()
