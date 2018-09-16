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

def tip( info , tipping_network , initial_state , bif_par_func , outfile ):
    
    net_ev = evolve( tipping_network , initial_state , bif_par_func )
    tolerance = 0.005
    t_step = 0.1
    save = True
    realtime_break = 30
    
    if not net_ev.is_fixed_point(tolerance):
        print("Warning: Initial state is not a fixed point of the system")
    elif not net_ev.is_stable():
        print("Warning: Initial state is not a stable point of the system")
        
    while net_ev.number_tipped()<1:
        print('while')
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

    c_data.add_cascade( info , net_ev.number_tipped() ,
                        net_ev.times , net_ev.pars , net_ev.states )
    
    file = open( outfile , 'wb' )
    pickle.dump( c_data , file )