# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 16:50:20 2017

@author: root
"""

import time

import control.experiment_wrapper as ew

ew.initialize()
ew.set_freq_multiplier(1)
ew.set_freq_synth_frequency(13.5)
ew.set_freq_synth_power(15)
ew.set_freq_synth_enable(True)
ew.set_chopper_amplitude(5)
ew.set_chopper_frequency(5)
ew.set_chopper_on(True)
print 'initialized, setting sensitivity'
ew.set_sensitivity(500)
print 'getting sensitivity'
print ew.get_sensitivity()
time.sleep(10)
print 'snapping data'
print ew.snap_data()
time.sleep(10)

print ew.snap_data()
    
ew.close()