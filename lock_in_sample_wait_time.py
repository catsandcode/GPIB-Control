import numpy as np
import time
from setup_control import experiment_wrapper as ew

# Initialize setup
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

# Frequencies to test
freqs_sens = [(225.0, 0.005), (230.0, 0.005), (235.0, 0.002), (240.0, 0.005), (245.0, 0.005), (250.0, 0.002), (255.0, 0.002), (260.0, 0.005), (265.0, 0.002), (270.0, 0.002), (275.0, 0.002)]

# Times to sample at (in seconds)
times = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0, 30.0, 40.0, 50.0, 60.0]

# Create a new array to save data to (note this first empty row will be deleted later)
data = np.empty((1, len(times) + 1), dtype=float)

# Loop through frequencies
for freq, sens in freqs_sens:
    print('Frequency set ' + str(freq) + 'GHz, sensitivity set ' + str(sens) + 'mV')
    # Create a new 2-by-1 array for the row data, x is in left col, y is in right col
    data_row = np.array((freq, freq))
    # Set sensitivity
    ew.set_sensitivity(sens)
    # Set frequency
    ew.set_freq_synth_frequency(freq)
    # Get start time in seconds
    t_start = time.time()
    # Wait, sample, repeat
    for t_wait in times:
        # Get data from the lock-in amplifier and and add it to the data array
        (x, y) = ew.snap_data()
        data_entry = np.array((x, y))
        data_row = np.vstack((data_row, data_entry))
        # Find the time elapsed since the frequency was changed
        t_elapse = time.time() - t_start
        # Find the time remaining until the next time to sample at occurs
        t_left = t_wait - t_elapse
        print t_left
        # Sleep until that time
        time.sleep(t_left)
    # Transpose data_row so that it is actually a row and then add it to the data array
    data_row = data_row.transpose()
    data = np.vstack((data, data_row))


# Delete the first row in the collected data, as it was created to give the array shape earlier but holds no useful data
data = np.delete(data, 0, 0)

# Close instruments
ew.close()

# Get name of script
script_name = str(__file__)
script_name = script_name[:script_name.find('.py')]

# Save array
np.save(script_name, data)
