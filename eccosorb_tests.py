from control.snippets import sweep_parameter
from control.experiment_wrapper import set_freq_synth_frequency
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


def sweep(title):
    # Get name of script
    script_name = str(__file__)
    script_name = script_name[:script_name.find('.py')]
    # Sweep
    sweep_parameter(set_freq_synth_frequency, np.linspace(freq_start, freq_end, num=num_steps, endpoint=True),
                    time_constant=time_const, chopper_frequency=chop_freq, sensitivity=sens, load_time=load_time,
                    lock_in_time=lock_time, multiplier=multiplier,
                    save_path=script_name + '/' + title)

# Sample holder test
wait_for_user_confirmation('please ensure that nothing is between the two antenna horns and the two mirrors')

sweep('test0_nothing')

wait_for_user_confirmation('please place the sample holder between the two mirrors')

sweep('test0_holder')

# Eccosorb cover test
wait_for_user_confirmation('please ensure that nothing is between the two antenna horns and the two mirrors')

sweep('test1_nothing')

wait_for_user_confirmation('please place the eccosorb on the table between the two mirrors')

sweep('test1_eccosorb_cover')

# Eccosorb cover and sample holder test
wait_for_user_confirmation('please ensure that nothing is between the two antenna horns and the two mirrors')

sweep('test2_nothing')

wait_for_user_confirmation('please place the sample holder and eccosorb on the table between the two mirrors')

sweep('test2_both')
