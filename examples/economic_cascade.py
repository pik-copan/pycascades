"""
Tipping cascade on the normalised international trade network with economic tipping elements. 

The network is read from a csv file which contains the normalised weight matrix. 
The start node is given as a command line argument; the network is initialised 
with all nodes in the untipped state x=1 except for the start node, which is 
tipped and set to x=0. The system is then evolved for a specific time or until 
it reaches equilibrium (under a given tolerance).

1) Economic cascades can be started with the file "economic_cascade.py"
2) The underlying data for the EORA network must, however, be requested from the Acclimate group at the Potsdam-Institute for Climate Impact Research
"""

import copy
import csv
from datetime import timedelta
import numpy as np
import numpy.ma as ma
from netCDF4 import Dataset
import networkx as nx
import os
import sys
import time

sys.path.append('../modules/')

from core.tipping_element_economic import economic_logistic
from core.coupling_economic import linear_coupling
from core.tipping_network_economic import tipping_network_economic
from core.evolve_economic import evolve

start_time = time.time()

w_log = 0.2 # weight of the logistic term
startnode =  int(sys.argv[1]) # start node for the cascade
timestep =  0.5 # time interval after which the system is saved. 
    # not the actual integration timestep, which is determined by the 
    # scipy.integrate.odeint solver
breaktime = 10 # time after which the integration is ended
tol = 0.0001 # tolerance for determining whether the system is in equilibrium

### load normalised weight matrix
n_s = 27 # number of sectors
n_c = 188 # number of countries
flows_2d = []
with open('EORA_2012_normalised.csv') as f:
    rd = csv.reader(f)
    for row in rd:
        flows_2d.append( [ float(element) for element in row ] )


### set up network
element = economic_logistic(a=4,b=0.5,c=10,w=w_log)
net = tipping_network_economic()
for i_s in range(n_s * n_c):
    net.add_element( element, n_s=n_s )
for j_s in range(n_s):
    for j_c in range(n_c):
        for i_s in range(n_s):
            for i_c in range(n_c):
                if flows_2d[i_s + i_c*n_s][j_s + j_c*n_s]:
                        net.add_coupling( i_c * n_s + i_s,  j_c * n_s + j_s, i_s, 
                            linear_coupling(strength = flows_2d[i_s + i_c*n_s][j_s + j_c*n_s]) )

### set up initial state, fix dynamic of start node (otherwise it might tip back immediately)
initial_state = [1] * (n_s * n_c)
initial_state[startnode] = 0
net.set_param( startnode, 'r_0', -1 )
net.node[startnode]['sectorlist'] = [ [] for i in range(n_s)]

### evolve network upt to breaktime
ev = evolve( net, initial_state )
while ev._t < breaktime:
    ev._integrate_economic( timestep, timeseries=False, mxstep=1000 )
    tipped = net.get_tip_states( ev._x )
    
    ### save the tipstates of every node every timestep in an individual file
    np.savetxt("tipped_n%i_t%.1f.csv"%(startnode,ev._t),tipped, delimiter=",")
    
    # ### save the average state and the number of tipped nodes every timestep in a single file
    # avstate = np.mean(ev._x)
    # n_tipped = net.get_number_tipped( ev._x )
    # with open("output/time_avstate_tipped_w" + str(w_log) + "_c" + str(startcountry) + "_s" + str(startsector) + ".csv", 'a') as f:
        # wr = csv.writer(f)
        # wr.writerow( [ev._t, avstate, tipped] )
    
    # ### stop integration once equilibrium is reached
    # if ev.is_equilibrium_sec(tol):
        # break

print(str(timedelta(seconds=time.time()-start_time)))
