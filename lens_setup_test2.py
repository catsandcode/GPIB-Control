from control.daq import sweep_parameter
from control.experiment_wrapper import set_freq_synth_frequency
import numpy as np
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

# Settings
freq_start = 225
freq_end = 275
num_steps = 200
time_const = 100.0
chop_freq = 1.0
sens = 0.2
load_time = 4
lock_time = 0
multiplier = 18

# Get name of script
script_name = str(__file__)
script_name = script_name[:script_name.find('.py')]

# Start tests
wait_for_user_confirmation('please ensure that there is sufficient attenuation in front of the detector')

sweep_parameter(set_freq_synth_frequency, np.linspace(freq_start, freq_end, num=num_steps, endpoint=True), time_constant=time_const, chopper_frequency=chop_freq, sensitivity=sens, load_time=load_time, lock_in_time=lock_time, multiplier=multiplier,
                    save_path=script_name + '/sweep0')

sweep_parameter(set_freq_synth_frequency, np.linspace(freq_start, freq_end, num=num_steps, endpoint=True), time_constant=time_const, chopper_frequency=chop_freq, sensitivity=sens, load_time=load_time, lock_in_time=lock_time, multiplier=multiplier,
                    save_path=script_name + '/sweep1')
