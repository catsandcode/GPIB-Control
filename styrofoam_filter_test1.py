from control.daq import sweep_parameter
from control.experiment_wrapper import set_freq_synth_frequency
import numpy as np
import sys

"""
Horns are 92.85mm apart.

Uses a time constant of 1000ms, 12dB/oct, 0.2mV sensitivity, load time of 4s, lock in time of 4s. Sweeps from 12.5GHz to 16.5GHz in 25MHz steps. Returns values in volts.
"""


def wait_for_user_confirmation(instruction):
    print instruction
    while True:
        s = raw_input('continue? y/[n]\n')
        if s.lower() == 'y':
            print 'continuing...'
            break
        elif s.lower() == 'n':
            print 'exiting...'
            sys.exit(0)

wait_for_user_confirmation('please ensure that no filter is between the two antenna horns')

sweep_parameter(set_freq_synth_frequency, np.linspace(12.5, 16.5, num=160, endpoint=True), time_constant=1000,  sensitivity=0.2, load_time=4, lock_in_time=4, multiplier=1,
                save_path='styrofoam_filter_test1/no_filter')

wait_for_user_confirmation('please place the filter between the two antenna horns')

sweep_parameter(set_freq_synth_frequency, np.linspace(12.5, 16.5, num=160, endpoint=True), time_constant=1000,  sensitivity=0.2, load_time=4, lock_in_time=4, multiplier=1,
                save_path='styrofoam_filter_test1/with_filter')
