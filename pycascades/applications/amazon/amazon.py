from core.system.system import double_fold
from core.system.coupling import linear_coupling

import numpy as np


class amazon_double_well(double_fold):
    def __init__(self, map, mcwd, map_crit, mcwd_crit, map_mean, mcwd_mean):
        """Constructor with additional parameters for cusp"""
        super().__init__()
        self.mcwd = mcwd
        self.map = map
        self.map_crit = map_crit
        self.map_mean = map_mean
        self.mcwd_mean = mcwd_mean
        self.mcwd_crit = mcwd_crit

        self._control = self._calculate_control()

    def _calculate_control(self):
        c_rain = (
            np.sqrt(4 / 27) * (self.map - self.map_mean)
            / (self.map_crit - self.map_mean)
        )
        c_mcwd = (
            np.sqrt(4 / 27)
            * (self.mcwd - self.mcwd_mean)
            / (self.mcwd_crit - self.mcwd_mean)
            if self.mcwd_crit > 0.0
            else 0.0
        )

        if c_mcwd < 0.0:
            c_mcwd = 0.0

        c = c_mcwd + c_rain
        return c

    def f(self, x, t):
        return -1.0 * pow(x, 3) + 1.0 * x + self._control


class amazon_coupling(linear_coupling):
    def __init__(
        self,
        delta_map,
        delta_mcwd,
        map,
        mcwd,
        map_crit,
        mcwd_crit,
        map_mean,
        mcwd_mean,
        x_0
    ):
        self._strength = self._calculate_strength(
            delta_map,
            delta_mcwd,
            map,
            mcwd,
            map_crit,
            mcwd_crit,
            map_mean,
            mcwd_mean
        )
        self._x_0 = x_0

    def _calculate_strength(
        self,
        delta_map,
        delta_mcwd,
        map,
        mcwd,
        map_crit,
        mcwd_crit,
        map_mean,
        mcwd_mean
    ):
        cpl_rain = np.sqrt(4 / 27) * (1 / 2) * delta_map / (map_mean - map_crit)
        cpl_mcwd = (
            np.sqrt(4 / 27) * (1 / 2) * delta_mcwd
            / (mcwd_crit - mcwd_mean)
            if mcwd_crit > 0.0 else 0.0
        )
        cpl  = cpl_mcwd + cpl_rain
        return cpl
