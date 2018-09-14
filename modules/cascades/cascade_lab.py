#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 16:48:10 2018

@author: jonathan
"""
import pickle
import os

from core.evolve import net_evolve
from cascades.cascade_data import cascade_data

def tip( tipping_network , tip_id_list , outfile ):
    
    net_ev = net_evolve(tipping_network)
    cascade_size = net_ev.tip(tip_id_list,0.005,0.1,500,save=True)
    if os.path.exists(outfile):
        file = open( outfile , 'rb' )
        c_data = pickle.load(file)
    else:
        c_data = cascade_data()
        
    c_data.add_cascade( "test" , tipping_network , cascade_size )
    file = open( outfile , 'wb' )
    pickle.dump( c_data , file )