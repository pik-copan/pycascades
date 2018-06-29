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
net = net_factory.create_cusp_chain(5,-1,1,0,-0.003,0.35)

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
#solver.equilibrate(0.005,0.1,30)
solver.tip([0],0.005,0.1,30)
#solver.integrate(0.1,200)
t_iteration = time.process_time() - t0
print(t_iteration)

plt.figure(1)
plt.plot(solver.times,solver.states)
