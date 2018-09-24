#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 16:48:10 2018

@author: jonathan
"""
import numpy as np

from core.evolve import evolve
from core.evolve import NoEquilibrium

def tip( net , initial_state , bif_par_arr , bif_par_func ):
    
    net_ev = evolve( net , initial_state , bif_par_arr , bif_par_func )
    
    tolerance = 0.005
    t_step = 0.1
    save = True
    realtime_break = 100
    
    if not net_ev.is_fixed_point(tolerance):
        print("Warning: Initial state is not a fixed point of the system")
    elif not net_ev.is_stable():
        print("Warning: Initial state is not a stable point of the system")
        
    while net_ev.number_tipped()<1:
        try:
            net_ev.equilibrate(tolerance,t_step,save,realtime_break)
        except NoEquilibrium:
            return np.nan
    
    return net_ev.number_tipped()
    
"""
TODO: Integrate get_critical_par method, that was initially in
evolve module, here!!!

from scipy.optimize import fsolve

    def get_critical_par(self,tip_id,res=0.001):
        self.net.adjust_normal_pars(0)
        if not self.net.is_stable():
            print("Initially unstable!")
        while self.net.is_stable():
            self.net.node[tip_id]['data'].c+=res
            x_new = fsolve(lambda x : self.net.f_prime(0,x)
                            ,-np.ones(len(self.net.get_state()))
                            ,fprime = lambda x : self.net.jac(0,x) )
            self.net.set_state(x_new)
        
        critical_par = self.net.node[tip_id]['data'].c
        x_crit = self.net.get_state()
        self.net.set_state(self.init_state)
        self.net.adjust_normal_pars(0)
        return critical_par,x_crit
"""