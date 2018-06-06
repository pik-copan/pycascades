# Add modules directory to path
import sys
sys.path.append('../modules')

from core.coupling import linear_coupling
from core.tipping_element import cusp
from core.network import network

tc1 = cusp(0,0.5,1)
tc2 = cusp(1,0.5,1)
cpl = linear_coupling(0.1,tc1)
tc2.add_cpl(cpl)
net = network()
net.add_element(tc1)
net.add_element(tc2)
print net.plot_net()
print net.get_state()
net.iterate(0.5)
print net.get_state()
