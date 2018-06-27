# Add modules directory to path
import sys
sys.path.append('../modules')

# global imports
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# private imports
from core.coupling import linear_coupling
from core.tipping_element import cusp
from core.network import network

# create network
tc0 = cusp(0,-1,1,0)
tc0.update_state(-1)
tc1 = cusp(1,-1,1,0)
tc1.update_state(-1)
#c1 = linear_coupling(-0.37,tc0)
c2 = linear_coupling(0.4,tc1)
tc0.add_cpl(c2)
#tc1.add_cpl(c1)
net = network()
net.add_element(tc0)
net.add_element(tc1)
print (net.get_structure())

# initialize state
x0 = net.get_state()

# initialize time
iter_tstep = 0.01
param_tstep = 10
t_init = 0
t_max = 2000

t_cum = []
x_cum = []

for t in range(t_init,t_max,param_tstep):
    t_begin = t
    t_end = t + param_tstep
    t_arr = np.linspace(t_begin, t_end
                        , num=round( ( t_end-t_begin ) / iter_tstep + 1 ) )
    x = odeint(net.system,x0,t_arr)
    x0 = x[-1]
    t_cum.extend(t_arr)
    x_cum.extend(x)
    tc0.c = tc0.c + 0.005
    
plt.plot(t_cum,x_cum)
plt.show()

