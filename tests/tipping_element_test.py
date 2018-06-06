# Add modules directory to path
import sys
sys.path.append('../modules')

from core.tipping_element import tipping_element,cusp

# Test tipping_element class
te = tipping_element()
print te.x
print te.cpl_sum()
te.iterate(1.5)
print te.x

# Test cusp class
tc = cusp(1,0.5)
print tc.x
print tc.a
tc.iterate(1.5)
print tc.x
