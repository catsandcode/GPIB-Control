from setup_control.snippets import sweep_parameter
from setup_control.experiment_wrapper import set_freq_synth_frequency
import numpy as np
import sys

"""
Uses a time constant of 1, 12dB/oct, 1mV sensitivity, load time of 4s, lock in time of 0s. Sweeps from 225GHz to 275GHz in 250MHz steps. Returns values in volts.

Takes four sweeps, one without filter, then two with filter and finally one without.
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

# Settings
freq_start = 225
freq_end = 275
num_steps = 200
time_const = 100.0
chop_freq = 1.0
sens = 1.0
load_time = 4
lock_time = 0
multiplier = 18

# Start tests
wait_for_user_confirmation('please ensure that no filter is between the two antenna horns')

sweep_parameter(set_freq_synth_frequency, np.linspace(freq_start, freq_end, num=num_steps, endpoint=True), time_constant=time_const, chopper_frequency=chop_freq, sensitivity=sens, load_time=load_time, lock_in_time=lock_time, multiplier=multiplier,
                    save_path='hdpe_test1/no_filter0')

wait_for_user_confirmation('please place the filter between the two antenna horns')

sweep_parameter(set_freq_synth_frequency, np.linspace(freq_start, freq_end, num=num_steps, endpoint=True), time_constant=time_const, chopper_frequency=chop_freq, sensitivity=sens, load_time=load_time, lock_in_time=lock_time, multiplier=multiplier,
                    save_path='hdpe_test1/with_filter0')

sweep_parameter(set_freq_synth_frequency, np.linspace(freq_start, freq_end, num=num_steps, endpoint=True), time_constant=time_const, chopper_frequency=chop_freq, sensitivity=sens, load_time=load_time, lock_in_time=lock_time, multiplier=multiplier,
                    save_path='hdpe_test1/with_filter1')

wait_for_user_confirmation('please remove the filter between the two antenna horns')

sweep_parameter(set_freq_synth_frequency, np.linspace(freq_start, freq_end, num=num_steps, endpoint=True), time_constant=time_const, chopper_frequency=chop_freq, sensitivity=sens, load_time=load_time, lock_in_time=lock_time, multiplier=multiplier,
                    save_path='hdpe_test1/no_filter1')
