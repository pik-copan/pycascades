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
import sdeint

import seaborn as sns
sns.set(font_scale=1.5)
sns.set_style("whitegrid")


import sys
sys.path.append('../modules/gen')
sys.path.append('../modules/core')
sys.path.append('../modules/utils')
sys.path.insert(0,"../modules")



"""Create two cusp tipping elements"""
from tipping_element import cusp
cusp_element_0 = cusp( a = -4, b = 1, c = 0.0, x_0 = 0.5 )


"""Create a tipping network and add the created elements"""
from tipping_network import tipping_network
from evolve_sde import evolve


#Network of two coupled cusp catastrophes
net = tipping_network()
net.add_element( cusp_element_0 )

initial_state = [0.0]
ev = evolve( net, initial_state )

"""Manually integrate the system"""
timestep = 0.01
t_end = 200

#define sigma for random processes
noise = 0.25						#noise level
n = 1							#number of investigated tipping elements
sigma = np.diag([1]*n)*noise	#diagonal uncorrelated noise
ev.integrate( timestep, t_end, initial_state, sigma=sigma)

time = ev.get_timeseries()[0]
cusp0 = ev.get_timeseries()[1][:,:].T[0]



fig, (ax0) = plt.subplots(1, 1, figsize=(5, 4)) #(default: 8, 6)


ax0.plot(time, cusp0, color="#1ABC9C", linewidth=2.0, label="Noise")
ax0.set_xlabel("Time [a.u.]")
ax0.set_ylabel("State [a.u.]")
ax0.set_ylim([-1.0, 2.0])
ax0.set_xticks(np.arange(0, 250, 50))
ax0.set_yticks(np.arange(-1.0, 2.5, 0.5))
ax0.legend(loc="lower left")

fig.tight_layout()
#fig.savefig('figures/levy.png')
#fig.savefig('figures/levy.pdf')
fig.show()
fig.clf()
plt.close()


print("Finish")
