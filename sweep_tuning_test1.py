from control.snippets import sweep_parameter
from control.experiment_wrapper import set_freq_synth_frequency
import numpy as np

"""
Horns are 98.67mm apart.

Uses a time constant of 100ms, 12dB/oct, 0.2mV sensitivity, load time of 4s, lock in time of 1.5s. Sweeps from 12.5GHz to 16.5GHz in 25MHz steps. Returns values in volts.
"""

for i in range(0, 3):
    sweep_parameter(set_freq_synth_frequency, np.linspace(12.5, 16.5, num=160, endpoint=True), time_constant=100,  sensitivity=0.2, load_time=4, lock_in_time=1.5, multiplier=1,
                    save_path='sweep_tuning_test1/long_lock_in_time_sweep_num_' + str(i))


"""
Horns are 98.67mm apart.

Uses a time constant of 100ms, 12dB/oct, 0.2mV sensitivity, load time of 4s, lock in time of 0.2s. Sweeps from 12.5GHz to 16.5GHz in 25MHz steps. Returns values in volts.
"""

for i in range(0, 3):
    sweep_parameter(set_freq_synth_frequency, np.linspace(12.5, 16.5, num=160, endpoint=True), time_constant=100,  sensitivity=0.2, load_time=4, lock_in_time=0.2, multiplier=1,
                    save_path='sweep_tuning_test1/short_lock_in_time_sweep_num_' + str(i))