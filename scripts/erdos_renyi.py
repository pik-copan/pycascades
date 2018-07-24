# Add modules directory to path
import sys
sys.path.append('../modules')

# global imports
#import numpy as np
import time
import matplotlib.pyplot as plt

# private imports
from gen.net_factory import net_factory
from core.evolve import net_evolve

net_factory = net_factory()
net = net_factory.create_erdos_renyi(100,3,-1,1,0,-1,2,67)
net_ev = net_evolve(net)

t0 = time.process_time()
print(net_ev.tip([0],0.005,0.1,500,save=True))
t_iteration = time.process_time() - t0
print("Elapsed Time:")
print(t_iteration)

plt.figure(1)
plt.plot(net_ev.times,net_ev.states)
plt.show()

