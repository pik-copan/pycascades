#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 16:48:10 2018

@author: jonathan
"""
import numpy as np

from core.evolve import evolve
from core.evolve import NoEquilibrium

import matplotlib.pyplot as plt

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
    
def basins( net , xrange , yrange , bif_par_arr , bif_par_func, number ):
    
    tolerance = 0.005
    t_step = 0.1
    save = True
    realtime_break = 100
    
    x_init = [[]]
    y_init = [[]]
    x_end = [[]]
    y_end = [[]]
    equilibria = []
    c = bif_par_arr
    
    for ind in range(0,number):
        x = np.random.uniform( xrange[0], xrange[1])
        y = np.random.uniform( yrange[0], yrange[1])
        
        net_ev = evolve( net , [x, y] , c , bif_par_func)
        net_ev.equilibrate(tolerance,t_step,save,realtime_break)
        
        if not net_ev.is_stable():
            continue
        
        equi_bool = [np.linalg.norm(net_ev.states[-1] - eq) > 0.5 for eq in equilibria]
        if all(equi_bool):
            basin_number = len(equilibria)
            x_end.append([])
            y_end.append([])         
            x_init.append([])
            y_init.append([])
            equilibria.append([])
        else:
            basin_number = [equi_bool.index(i) for i in equi_bool if i == False][0]
   
        x_end[basin_number].append(net_ev.states[-1][0])
        y_end[basin_number].append(net_ev.states[-1][1])         
        x_init[basin_number].append(x)
        y_init[basin_number].append(y)
        equilibria[basin_number] = [np.mean(x_end[basin_number]), np.mean(y_end[basin_number])]
    
    plt.xlim(xrange[0], xrange[1])
    plt.ylim(yrange[0], yrange[1])
    for basin in enumerate(equilibria):
        plt.scatter(x_init[basin[0]] , y_init[basin[0]])
        
    x_val = [x[0] for x in equilibria]
    y_val = [x[1] for x in equilibria]
    plt.scatter(x_val,y_val,c='black')
    plt.xlabel('$x_1$', fontsize=15)
    plt.ylabel('$x_2$', fontsize=15)
    plt.title('$d=2$', fontsize=15)
    plt.show()
    
    
    return equilibria
    
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