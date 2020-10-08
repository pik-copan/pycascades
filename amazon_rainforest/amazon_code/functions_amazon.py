import numpy as np
from netCDF4 import Dataset
import warnings


class global_functions():
    def Rain(datasets):
        """
        Computation of rainfall values; all datasets are necessary and a potential rain factor
        """
        rain = []
        for data in datasets:
            net_data = Dataset(data)
            #get mean value for rainfall
            rain_dataset = net_data.variables["rain"][:]
            if len(rain) == 0:
                rain = rain_dataset
            else:
                rain = np.add(rain, rain_dataset)
        rain = np.array(rain)
        return rain



    def Amazon_CUSPc(a, b, rain_current, rain_critical, rain_mean):
        """
        c = c(rainfall) where tipping occurs at sqrt((4*b**3)/(27*a))
        """
        c = np.sqrt((4*np.abs(b)**3) / (27*np.abs(a)))/(rain_critical - rain_mean)*(rain_current - rain_mean)
        return c



    def Amazon_cpl(a, b, rain_critical, rain_current, rain_mean, delta_rain):
        """
        Factor of (1/2) is necessary since delta(state)=2 from -1 to +1
        Factor (-1) is necessary since delta_rain < 0, but the coupling must be positive
        """

        #rain [c, cpl]-values
        c = np.sqrt((4*np.abs(b)**3) / (27*np.abs(a)))/(rain_critical - rain_mean)*(rain_current - rain_mean)
        cpl = np.sqrt((4*np.abs(b)**3) / (27*np.abs(a)))/(rain_mean - rain_critical)*(1/2)*(-1)*delta_rain


        if cpl < 0.0:
            print("Coupling strengths below 0.0 are not allowed")
            die
    
        return cpl



    def Rain_moisture_delta_only(moist_rec_val):
        """
        Computation of moisture recycling value for a year
        """
        rain_moist = - np.sum(moist_rec_val)
        return rain_moist