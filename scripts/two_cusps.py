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
net = net_factory.create_two_cusps(-1,1,0,-1.0,2,False)
net.adjust_normal_pars(0)
pos=nx.spring_layout(net)
nx.draw_networkx(net,pos)
nx.draw_networkx_edge_labels(net,pos,edge_labels=nx.get_edge_attributes(net,'weight'))
plt.show()

net_evolve = net_evolve(net)

net_evolve.tip([0],0.005,0.1,30,save=True)

plt.figure(1)
plt.subplot(211)
plt.plot(net_evolve.times,net_evolve.states)

plt.subplot(212)
plt.plot(net_evolve.pars,net_evolve.states)
plt.show()