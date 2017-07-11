from control.daq import sweep_parameter
from control.experiment_wrapper import set_freq_synth_frequency
import numpy as np
import sys

"""
Horns are 98.67mm apart.

Uses a time constant of 100ms, 12dB/oct, 0.2mV sensitivity, load time of 4s, lock in time of 0s. Sweeps from 225GHz to 300GHz in 500MHz steps. Returns values in volts.

Takes two sweeps, one with filter and one without
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

sweep_parameter(set_freq_synth_frequency, np.linspace(225, 300, num=150, endpoint=True), time_constant=100, chopper_frequency=1, sensitivity=0.2, load_time=4, lock_in_time=0, multiplier=18,
                    save_path='sweep_tuning_test3/no_filter')

wait_for_user_confirmation('please place the filter between the two antenna horns')

sweep_parameter(set_freq_synth_frequency, np.linspace(225, 300, num=150, endpoint=True), time_constant=100, chopper_frequency=1, sensitivity=0.2, load_time=4, lock_in_time=0, multiplier=18,
                    save_path='sweep_tuning_test3/with_filter')
