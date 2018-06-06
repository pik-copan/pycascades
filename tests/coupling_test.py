# Add modules directory to path
import sys
sys.path.append('../modules')

from core.tipping_element import cusp
from core.coupling import linear_coupling

# Test linear coupling
tc1 = cusp(0.5,1)
tc2 = cusp(0.5,1)
cpl = linear_coupling(0.1,tc1)
print cpl.coupling()
tc2.add_cpl(cpl)
tc2.iterate(1.5)
print tc2.x
