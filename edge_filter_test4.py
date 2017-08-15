import time
import sys
import numpy as np
from setup_control import experiment_wrapper as ew

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
    for low, high, sens in bands: # Iterate through all bands
        if low <= freq <= high:
            return sens # Return the sensitivity associated with the band
    return 0.050 # Return 50uV by default


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
    ew.set_chopper_frequency(1.0)
    ew.set_chopper_on(True)

    # Setup lock-in
    ew.set_time_constant(100.0)
    ew.set_low_pass_slope(24.0)

    # Sleep to allow instruments to adjust settings
    time.sleep(4.0)

    # Create a new array to save data to
    data = np.array([0, 0, 0], float)  # This row will be deleted later

    # Sweep the selected parameter and record data
    for freq in freqs:
        print('At frequency ' + str(freq) + 'GHz')

        # Set frequency and sensitivity
        ew.set_freq_synth_frequency(freq)
        ew.set_sensitivity(get_sensitivity_setting(freq, sens_bands))

        # Sleep to allow lock-in to lock to new frequency and for time constant to average
        time.sleep(100.0 * 5.0 / 1000.0)  # Sleep for five time constants plus the lock_in_time

        # Get data from the lock-in amplifier and and add it to the data array
        (x, y) = ew.snap_data()

        data_row = np.array([freq, x, y])
        data = np.vstack((data, data_row))

    # Delete the first row in the collected data, as it was created to give the array shape earlier but holds no useful data
    data = np.delete(data, 0, 0)

    np.save(save_path, data)

# Settings
freq_start = 225
freq_end = 275
num_steps = 200

# Get name of script
script_name = str(__file__)
script_name = script_name[:script_name.find('.py')]

bands = [(225.0, 226.0, 0.050), (226.0, 237.0, 0.020), (237.0, 239.0, 0.010), (239.0, 241.0, 0.020), (241.0, 246.0, 0.050), (246.0, 247.0, 0.020, (247.0, 249.0, 0.010), (249.0, 253.0, 0.005), (253.0, 254.0, 0.010), (254.0, 262.0, 0.020), (262.0, 265.0, 0.010), (265.0, 270.0, 0.020), (270.0, 274.0, 0.010), (274.0, 275.0, 0.005))]

# Start tests
wait_for_user_confirmation('please ensure that nothing is between the two lenses')

sweep(np.linspace(freq_start, freq_end, num=num_steps, endpoint=True), bands, script_name + '/no_filter0')

wait_for_user_confirmation('please place the edge filter between the two lenses')

sweep(np.linspace(freq_start, freq_end, num=num_steps, endpoint=True), bands, script_name + '/filter0')

sweep(np.linspace(freq_start, freq_end, num=num_steps, endpoint=True), bands, script_name + '/filter1')

wait_for_user_confirmation('please remove the edge filter between the two lenses')

sweep(np.linspace(freq_start, freq_end, num=num_steps, endpoint=True), bands, script_name + '/filter1')
