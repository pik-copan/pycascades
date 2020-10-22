"""
Timing module: This module computes the conversion factor
between one year in the simulation and one "real" year depending on the tipping time scale of the Amazon rainforest
"""
import sys
sys.path.append('')
#sys.path.append('../../modules/core')
sys.path.append('../../modules/core')
sys.path.append('../../modules/gen')

import numpy as np
from tipping_element import cusp
from coupling import linear_coupling_earth_system
from evolve import evolve
from earth_sys.functions_earth_system import global_functions
from earth_sys.tipping_network_earth_system import tipping_network


class timing():

    def __init__(self):
        #Timescales
        self._gis_realtime = 4900.
        self._thc_realtime = 300.
        self._wais_realtime = 2400.
        self._amaz_realtime = 50.


        #Compute conversion factor
        self._real_timescale = self._gis_realtime                   					 #value normed to GIS
        self._timescale = self._gis_realtime/self._amaz_realtime    					 #value normed to GIS
        self._tip_point_gis = 1.8  # most probable tipping point (see Robinson, 2012)    #value normed to GIS
        self._c_krit = np.sqrt(4 / 27)
        self._GMT_cal = 4.0                                        						 #normed temperature
        self._epsilon_c = global_functions.CUSPc(0., self._tip_point_gis, self._GMT_cal) - self._c_krit
        self._initial_state = [-1.]
        self._threshold = 1.0


    """
    Time scale, normed to the shortest tipping scale, in years
    N.B.: Note that we can only insert a RELATIVE time scale, in principle the time scale is dependent on the GMT,
    Here we insert tipping time scales at a temperature around 4°C above pre-industrial, since time scales are shifting during simulation due to structure of CUSP-catastrophe
    """
    def timescales(self):
        gis_time = self._gis_realtime/self._amaz_realtime
        thc_time = self._thc_realtime/self._amaz_realtime
        wais_time = self._wais_realtime/self._amaz_realtime
        amaz_time = self._amaz_realtime/self._amaz_realtime
        return gis_time, thc_time, wais_time, amaz_time


    """
    Here we insert a conversion factor to get a translation from a.u. to "true" years
    """
    def conversion(self):
        cusp_deq = cusp(a=-1/self._timescale, b=1/self._timescale, c=self._c_krit/self._timescale, x_0=0.0)
        net = tipping_network()
        net.add_element(cusp_deq)
        cusp_deq._par['c'] = self._c_krit/self._timescale + self._epsilon_c/self._timescale

        timestep = 0.01
        t_end = 5000
        ev = evolve(net, self._initial_state)
        ev.integrate(timestep, t_end)

        t_arr = np.array(ev.get_timeseries()[0])
        cusp_deq = np.array(ev.get_timeseries()[1][:, 0])

        # find point where state crosses threshold
        th = cusp_deq > self._threshold
        th[1:][th[:-1] & th[1:]] = False

        # conversion factor from arbitrary units to years
        conv_fac = self._real_timescale / t_arr[np.nonzero(th)[0][0]]
        return conv_fac




