# Add modules directory to path
import sys
sys.path.append('../modules')

# global imports
import matplotlib.pyplot as plt
import networkx as nx

# private imports
from gen.net_factory import net_factory
from core.evolve import net_evolve

net_factory = net_factory()
net = net_factory.create_one_cusp(-1,1,0,-1)
nx.draw(net)

net_evolve = net_evolve(net)

# initialize time
net_evolve.tip([0],0.005,0.1,30)

plt.figure(1)
plt.subplot(211)
plt.plot(net_evolve.times,net_evolve.states)

plt.subplot(212)
plt.plot(net_evolve.pars,net_evolve.states)
plt.show()