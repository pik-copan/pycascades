#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 12:08:53 2018

@author: jonathan

helpers module
"""

def play_sound(path_to_file):
    try:
        import simpleaudio as sa
        wave_obj = sa.WaveObject.from_wave_file(path_to_file)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except:
        pass