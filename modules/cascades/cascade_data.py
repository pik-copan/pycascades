#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 16:21:28 2018

@author: jonathan
"""

class cascade_data(list):
    def __init__(self):
        pass
    
    def add_cascade( self , info , size , t_array=None
                   , par_series=None , time_series=None , tipping_network = None):
        
        casc_dict = { "info" : info
                    , "net" : tipping_network
                    , "size" : size
                    , "t_array" : t_array
                    , "par_array" : par_series
                    , "time_series" : time_series }
        
        self.append(casc_dict)