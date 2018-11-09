#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 12:08:53 2018

@author: jonathan

helpers module
"""
import os
import csv
      
class csv_writer():
    def __init__( self, outfile):
        
        self.data = {}
        
        if os.path.exists ( outfile ):
            
            self._mode = 'a'
            
            file = open( outfile , 'r' )           
            csv_read = csv.reader(file)
            for line in csv_read:
                last = line[1]
            self.data["id"] = int(last)
            file.close()
            
        else:
            
            self._mode = 'w'
            self.data["id"] = 0
        
        self._file = open( outfile , self._mode )

        self._csv_writer = csv.writer( self._file, delimiter=',', quotechar='"'
                                     , quoting=csv.QUOTE_MINIMAL)
    
    def write_head( self ):
        self._csv_writer.writerow( [""] + list( self.data.keys()) )
        self._file.flush()
        
    def write_row( self ):
        self._csv_writer.writerow( [""] + list( self.data.values()) )
        self._file.flush()
        self.data["id"] += 1

def play_sound(path_to_file):
    try:
        import simpleaudio as sa
        wave_obj = sa.WaveObject.from_wave_file(path_to_file)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except:
        pass
