from control.daq import sweep_parameter
from control.experiment_wrapper import set_freq_synth_frequency
import numpy as np

"""
Horns are 98.67mm apart.

Uses a time constant of 100ms, 12dB/oct, 0.2mV sensitivity, load time of 4s, lock in time of 0s. Sweeps from 225GHz to 300GHz in 500MHz steps. Returns values in volts.

Takes two sweeps at 5kHz, two at 2kHz, and two at 1kHz
"""

for i in range(0, 2):
    sweep_parameter(set_freq_synth_frequency, np.linspace(225, 300, num=150, endpoint=True), time_constant=100, chopper_frequency=5, sensitivity=0.2, load_time=4, lock_in_time=0, multiplier=18,
                    save_path='sweep_tuning_test3/5kHz_sweep_num_' + str(i))

for i in range(0, 2):
    sweep_parameter(set_freq_synth_frequency, np.linspace(225, 300, num=150, endpoint=True), time_constant=100, chopper_frequency=2, sensitivity=0.2, load_time=4, lock_in_time=0, multiplier=18,
                    save_path='sweep_tuning_test3/2kHz_sweep_num_' + str(i))

for i in range(0, 2):
    sweep_parameter(set_freq_synth_frequency, np.linspace(225, 300, num=150, endpoint=True), time_constant=100, chopper_frequency=1, sensitivity=0.2, load_time=4, lock_in_time=0, multiplier=18,
                    save_path='sweep_tuning_test3/1kHz_sweep_num_' + str(i))