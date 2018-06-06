# Add modules directory to path
import sys
sys.path.append('../modules')

from core.tipping_element import tipping_element
from core.coupling import linear_coupling

# Test linear coupling
te = tipping_element()
cpl = linear_coupling(0.1,te)
print cpl.coupling()


