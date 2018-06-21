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

tc0 = cusp(0,-1,1,0)
tc0.update_state(-1)
tc0.tipped = False
net = network()
net.add_element(tc0)
print (net.get_structure())

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
    net.set_state(x[-1])
    x0 = net.get_state()
    
    t_cum.extend(t_arr)
    x_cum.extend(x)
    tc0.c = tc0.c + 0.005
    print (tc0.tipped)
    
plt.plot(t_cum,x_cum)
plt.show()