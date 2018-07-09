# Add modules directory to path
import sys
sys.path.append('../modules')

# global imports
import matplotlib.pyplot as plt
import networkx as nx
#import numpy as np

# private imports
from gen.net_factory import net_factory
from core.evolve import net_evolve

net_factory = net_factory()
net = net_factory.create_oscillator(-1,1,0,1.0,-1)
pos=nx.spring_layout(net)
nx.draw_networkx(net,pos)
nx.draw_networkx_edge_labels(net,pos,edge_labels=nx.get_edge_attributes(net,'weight'))
plt.show()

net_evolve = net_evolve(net)

# initialize time
#net_evolve.tip([0],0.005,0.1,30)
net_evolve.equilibrate(0.005,0.1,30)

plt.figure(1)
plt.plot(net_evolve.times,net_evolve.states)

