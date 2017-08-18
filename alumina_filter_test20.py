from setup_control.snippets import sweep_parameter
from setup_control.experiment_wrapper import set_freq_synth_frequency
import numpy as np
import time
import sys


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


def get_sensitivity_setting(freq, bands):
    for low, high, sens in bands:  # Iterate through all bands
        if low <= freq <= high:
            return sens  # Return the sensitivity associated with the band
    return 0.050  # Return 50uV by default


# Settings
freq_start = 225.0
freq_end = 275.0
num_steps = 200
freqs = np.linspace(freq_start, freq_end, num=num_steps, endpoint=False)
time_const = 100.0
chop_freq = 1.0
sens = 1.0 # 50uV
load_time = 4
lock_time = 0
multiplier = 18

# Get name of script
script_name = str(__file__)
script_name = script_name[:script_name.find('.py')]

# Start tests
wait_for_user_confirmation('please ensure that nothing is between the two mirrors')

sweep_parameter(set_freq_synth_frequency, freqs, time_constant=time_const, chopper_frequency=chop_freq, sensitivity=sens, load_time=load_time, lock_in_time=lock_time, multiplier=multiplier, save_path=script_name + '/no_sample0')

wait_for_user_confirmation('please place the sample between the two mirrors')

sweep_parameter(set_freq_synth_frequency, freqs, time_constant=time_const, chopper_frequency=chop_freq, sensitivity=sens, load_time=load_time, lock_in_time=lock_time, multiplier=multiplier, save_path=script_name + '/with_sample0')

sweep_parameter(set_freq_synth_frequency, freqs, time_constant=time_const, chopper_frequency=chop_freq, sensitivity=sens, load_time=load_time, lock_in_time=lock_time, multiplier=multiplier, save_path=script_name + '/with_sample1')

wait_for_user_confirmation('please remove the sample between the two mirrors')

sweep_parameter(set_freq_synth_frequency, freqs, time_constant=time_const, chopper_frequency=chop_freq, sensitivity=sens, load_time=load_time, lock_in_time=lock_time, multiplier=multiplier, save_path=script_name + '/no_sample1')

