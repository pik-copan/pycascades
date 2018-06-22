# Add modules directory to path
import sys
sys.path.append('../modules')

# global imports
import matplotlib.pyplot as plt

# private imports
from gen.net_factory import net_factory
from core.integrate import solver

net_factory = net_factory()
net = net_factory.create_one_cusp(-1,1,0,-1)

print (net.get_structure())

solver = solver(net)

# initialize time
solver.iterate(net.tip_list[0],1000,0.01,0.001)

plt.figure(1)
plt.subplot(211)
plt.plot(solver.times,solver.states)

plt.subplot(212)
plt.plot(solver.pars,solver.states)
plt.show()