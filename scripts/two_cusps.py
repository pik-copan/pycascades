# Add modules directory to path
import sys
sys.path.append('../modules')

# global imports
from scipy.integrate import odeint

# private imports
from core.coupling import linear_coupling
from core.tipping_element import cusp
from core.network import network

# create network
tc1 = cusp(0,0.5,1)
tc2 = cusp(1,0.5,1)
cpl = linear_coupling(0.1,tc1)
tc2.add_cpl(cpl)
net = network()
net.add_element(tc1)
net.add_element(tc2)

y0 = net.get_state()

print (y0)

t = [0,1,2,3,4,5,6,7,8,9,10]

print (t)

# solve ODE
y = odeint(net.system,y0,t)

print ([t,y])

