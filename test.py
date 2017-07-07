# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 16:50:20 2017

@author: root
"""

import time
import numpy as np
import control.experiment_wrapper as ew

ew.initialize()
ew.set_freq_multiplier(1)
ew.set_freq_synth_frequency(13.5)
ew.set_freq_synth_power(15)
ew.set_freq_synth_enable(True)
ew.set_chopper_amplitude(5)
ew.set_chopper_frequency(5)
ew.set_chopper_on(True)
time.sleep(5)

ew.set_sensitivity(500)
for freq in np.linspace(12.5, 16.5, num=10, endpoint=True):
    ew.set_freq_synth_frequency(freq)
    print ew.snap_data()

while True:
    s = ew.lock_in.read()
    if s == '':
        break
    else:
        print s
    
ew.close()