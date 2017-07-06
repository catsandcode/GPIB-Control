from control import experiment_wrapper as ew
import time, datetime
import numpy as np


ew.initialize()

# Set the frequency multiplier, as it is particular to the experiment
ew.set_freq_multiplier(1)

# Setup the frequency synthesizer
ew.set_freq_synth_frequency(14.0)
ew.set_freq_synth_power(15.0)
ew.set_freq_synth_enable(True)

# Setup chopper
ew.set_chopper_amplitude(5.0)
ew.set_chopper_frequency(5.0)
ew.set_chopper_on(True)

# Setup lock-in
ew.set_time_constant(100.0)
ew.set_sensitivity(500.0)
ew.set_low_pass_slope(12.0)

# Sleep to allow instruments to adjust settings
time.sleep(5)

# Create a new array to save data to
data = np.array([0, 0, 0], float)  # This row will be deleted later

# Get start time

start_time = time.time()

start_datetime = datetime.datetime.now()

start_hour = start_datetime.time().hour

start_min = start_datetime.time().minute

start_sec = start_datetime.time().second

str_start_time = str(start_hour) + ' hours ' + str(start_min) + ' mins ' + str(start_sec) + ' seconds'


# Sweep the selected parameter and record data
while True:
    t = time.time() - start_time

    t_mins = ((t / 1000.0) / 60.0)

    print(str(t_mins) + ' minutes since ' + str_start_time)

    # Get data from the lock-in amplifier
    (x, y) = ew.snap_data()

    # Add data to the data array
    data_row = np.array([t, x, y])
    data = np.vstack((data, data_row))

    # Check if the experiment has been running for 14 hours or more, if so stop
    if t > (1000.0 * 60.0 * 60.0 * 14.0):
        break

    # Sleep for 30 seconds
    time.sleep(30)

# Delete the first row in the collected data, as it was created to give the array shape earlier but holds no useful data
data = np.delete(data, 0, 0)

# Close instruments
ew.close()

# Save data
np.savez('overnight_test', data=data)
