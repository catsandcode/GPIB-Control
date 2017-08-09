from setup_control.snippets import sweep_parameter
from setup_control.experiment_wrapper import set_freq_synth_frequency
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

wait_for_user_confirmation('please ensure that no filter is between the two antenna horns')

sweep_parameter(set_freq_synth_frequency, np.linspace(225, 300, num=150, endpoint=True), time_constant=100,  sensitivity=0.2, load_time=4, lock_in_time=0, multiplier=18,
                save_path='zotefoam_window_test1/no_filter')

wait_for_user_confirmation('please place the filter between the two antenna horns')

sweep_parameter(set_freq_synth_frequency, np.linspace(225, 300, num=150, endpoint=True), time_constant=100,  sensitivity=0.2, load_time=4, lock_in_time=0, multiplier=18,
                save_path='zotefoam_window_test1/with_filter_sweep1')

sweep_parameter(set_freq_synth_frequency, np.linspace(225, 300, num=150, endpoint=True), time_constant=100,  sensitivity=0.2, load_time=4, lock_in_time=0, multiplier=18,
                save_path='zotefoam_window_test1/with_filter_sweep2')
