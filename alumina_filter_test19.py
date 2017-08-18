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


def sweep(freqs, sens_bands, save_path):
    # Initialize instruments
    ew.initialize()

    # Set the frequency multiplier, as it is particular to the experiment
    ew.set_freq_multiplier(18)

    # Setup the frequency synthesizer
    ew.set_freq_synth_power(15.0)
    ew.set_freq_synth_enable(True)

    # Setup chopper
    ew.set_chopper_amplitude(5.0)
    ew.set_chopper_frequency(0.010) # 10Hz chop frequency
    ew.set_chopper_on(True)

    # Setup lock-in
    ew.set_time_constant(300.0)
    ew.set_low_pass_slope(24.0)
    ew.set_sync_enabled(True)

    # Sleep to allow instruments to adjust settings
    time.sleep(4.0)

    # Create a new array to save data to
    data = np.array([0, 0, 0], float)  # This row will be deleted later

    # Sweep the selected parameter and record data
    for freq in freqs:
        print('At frequency ' + str(freq) + 'GHz')

        # Set sensitivity and frequency
        ew.set_sensitivity(get_sensitivity_setting(freq, sens_bands))
        time.sleep(0.3)  # Allow sensitivity to set
        ew.set_freq_synth_frequency(freq)

        # Sleep to allow lock-in to lock to new frequency and for time constant to average
        time.sleep(300.0 * 5.0 / 1000.0 + 0.5)  # Sleep for five time constants plus an additional half a second

        # Get data from the lock-in amplifier and and add it to the data array
        (x, y) = ew.snap_data()

        data_row = np.array([freq, x, y])
        data = np.vstack((data, data_row))

    # Delete the first row in the collected data, as it was created to give the array shape earlier but holds no useful data
    data = np.delete(data, 0, 0)

    np.save(save_path, data)

# Settings
freq_start = 225.0
freq_end = 275.0
num_steps = 200
freqs = np.linspace(freq_start, freq_end, num=num_steps, endpoint=False)
time_const = 100.0
chop_freq = 1.0
sens = 0.050 # 50uV
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
