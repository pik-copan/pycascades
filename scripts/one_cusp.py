# Add modules directory to path
import sys
sys.path.append('../modules')

# global imports
import matplotlib.pyplot as plt

# private imports
from core.tipping_element import cusp
from core.network import network
from core.integrate import solver

tc0 = cusp(0,-1,1,0)
tc0.update_state(-1)
net = network()
net.add_element(tc0)
print (net.get_structure())

solver = solver(net)

# initialize time
solver.iterate(tc0,1000,0.01,0.001)

plt.figure(1)
plt.subplot(211)
plt.plot(solver.times,solver.states)

plt.subplot(212)
plt.plot(solver.pars,solver.states)
plt.show()