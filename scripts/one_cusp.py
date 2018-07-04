# Add modules directory to path
import sys
sys.path.append('../modules')

# global imports
import matplotlib.pyplot as plt
import networkx as nx

# private imports
from gen.net_factory import net_factory
from core.integrate import solver

net_factory = net_factory()
net = net_factory.create_one_cusp(-1,1,0,-1)
nx.draw(net)

solver = solver(net)

# initialize time
solver.tip([0],0.005,0.1,30)

plt.figure(1)
plt.subplot(211)
plt.plot(solver.times,solver.states)

plt.subplot(212)
plt.plot(solver.pars,solver.states)
plt.show()