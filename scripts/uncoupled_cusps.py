# Small script that integrates a few uncoupled cusps with different initial
# conditions showing the dynamical structure of the cusp-dgl

# Add modules directory to path
import sys
sys.path.append('../modules')

# global imports
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# private imports
from core.tipping_element import cusp
from core.network import network

# create network
tc0 = cusp(0,-1,1,0)
tc1 = cusp(1,-1,1,0)
tc2 = cusp(2,-1,1,0)
tc3 = cusp(3,-1,1,0)
tc4 = cusp(4,-1,1,0)
tc0.update_state(0)
tc1.update_state(0.1)
tc2.update_state(-0.1)
tc3.update_state(2)
tc4.update_state(-2)
net = network()
net.add_element(tc0)
net.add_element(tc1)
net.add_element(tc2)
net.add_element(tc3)
net.add_element(tc4)
print (net.get_structure())

# initialize state
x0 = net.get_state()

# initialize time
timestep = 0.01
t_begin = 0.0
t_end = 5.0
t = np.linspace(t_begin, t_end, num=round( ( t_end-t_begin ) /timestep + 1 ) )

# solve ODE
x = odeint(net.system,x0,t)

plt.plot(t,x)
plt.show()

