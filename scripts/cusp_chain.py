# Add modules directory to path
import sys
sys.path.append('../modules')

# global imports
import matplotlib.pyplot as plt
import networkx as nx
import time

# private imports
from gen.net_factory import net_factory
from core.integrate import solver

net_factory = net_factory()
net = net_factory.create_cusp_chain(5,-1,1,0,-1,0.34)

t0 = time.process_time()
pos=nx.spring_layout(net)
nx.draw(net,pos)
nx.draw_networkx_edge_labels(net,pos,edge_labels=nx.get_edge_attributes(net,'weight'))
plt.show()

t_graph_draw = time.process_time() - t0
print(t_graph_draw)

solver = solver(net)

# initialize time
t0 = time.process_time()
solver.equilibrate(0.001,0.01,0.3)
t_iteration = time.process_time() - t0
print(t_iteration)

print(solver.times)
print(solver.states)

plt.figure(1)
plt.plot(solver.times,solver.states)
