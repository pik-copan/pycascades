#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 16:48:10 2018

@author: jonathan
"""

import pickle
import os

from core.evolve import evolve
from cascades.cascade_data import cascade_data

class NoEquilibrium(Exception):
    pass

def tip( info , tipping_network , initial_state , bif_par_arr , bif_par_func , outfile ):
    
    net_ev = evolve( tipping_network , initial_state , bif_par_arr , bif_par_func )
    tolerance = 0.005
    t_step = 0.1
    save = True
    realtime_break = 30
    
    if not net_ev.is_fixed_point(tolerance):
        print("Warning: Initial state is not a fixed point of the system")
    elif not net_ev.is_stable():
        print("Warning: Initial state is not a stable point of the system")
        
    while net_ev.number_tipped()<1:
        try:
            net_ev.equilibrate(tolerance,t_step,save,realtime_break)
        except NoEquilibrium:
            print("No equilibrium found " \
                  "in "+str(realtime_break)+" realtime seconds."\
                  " Increase tolerance or breaktime.")
            break
   
    if os.path.exists(outfile):
        file = open( outfile , 'rb' )
        c_data = pickle.load(file)
    else:
        c_data = cascade_data()

    c_data.add_cascade( info , tipping_network , net_ev.number_tipped() ,
                        net_ev.times , net_ev.pars , net_ev.states )
    
    file = open( outfile , 'wb' )
    pickle.dump( c_data , file )
    
    
"""
TODO: Integrate get_critical_par method, that was initially in
evolve module here!!!

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