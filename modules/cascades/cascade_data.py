#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 16:21:28 2018

@author: jonathan
"""

class cascade_data():
    def __init__(self):
        self._casc_list = []
    
    def add_cascade( self , info , tipping_network , t_array 
                   , par_array , time_series , size ):
        casc_dict = { "info" : info
                    , "net" : tipping_network
                    , "t_array" : t_array
                    , "par_array" : par_array
                    , "time_series" : time_series
                    , "size" : size }
        self.casc_list.append(casc_dict)