from control.daq import sweep_parameter
from control.experiment_wrapper import set_freq_synth_frequency
import numpy as np

"""
Horns are 98.80mm apart.

Uses a time constant of 100ms, 12dB/oct, 0.2mV sensitivity, load time of 4s, lock in time of 0s. Sweeps from 225GHz to 275GHz (horn output frequencies) in 250MHz steps. Returns values in volts.
"""
for i in range(0, 3):
    sweep_parameter(set_freq_synth_frequency, np.linspace(225.0, 275.0, num=200, endpoint=True), time_constant=100,  sensitivity=0.2, load_time=4, lock_in_time=0, multiplier=18,
                    save_path='sweep_tuning_test4/high_time_const_sweep' + str(i))

"""
Horns are 98.80mm apart.

Uses a time constant of 30ms, 12dB/oct, 0.2mV sensitivity, load time of 4s, lock in time of 0s. Sweeps from 225GHz to 275GHz (horn output frequencies) in 250MHz steps. Returns values in volts.
"""
for i in range(0, 3):
    sweep_parameter(set_freq_synth_frequency, np.linspace(225.0, 275.0, num=200, endpoint=True), time_constant=30,  sensitivity=0.2, load_time=4, lock_in_time=0, multiplier=18,
                    save_path='sweep_tuning_test4/low_time_const_sweep' + str(i))