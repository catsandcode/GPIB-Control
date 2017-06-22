import time, math, wrapper
import numpy as np


if __name__ == '__main__':
    wrapper.initialize()

    # Constants
    start = 200.0
    stop = 300.0
    sweep_time = 0.5
    sample_rate = 512

    # Setup sweeper
    wrapper.set_sweep_range(start, stop)
    wrapper.set_sweep_time(sweep_time)
    wrapper.set_power(5.0)

    # Setup chopper
    wrapper.set_chopper_amplitude(1)
    wrapper.set_chopper_sweep_on(False)
    wrapper.set_chopper_frequency(10.0)

    # Setup lock-in
    wrapper.set_sample_rate(sample_rate)

    # Start the scan
    wrapper.start_scan()
    wrapper.start_sweep()
    start_time = time.time()

    # Sleep
    time.sleep(sweep_time)

    # Stop the scan and record the time
    wrapper.stop_scan()
    stop_time = time.time()

    # Get data from the lock-in amplifier
    data_no_frequency = wrapper.get_data()
    (data_rows, data_columns) = data_no_frequency.shape

    # Figure out the frequency at each data point
    daq_time = stop_time - start_time
    freq_per_sec = (stop - start) / daq_time

    frequency = []
    for i in range(data_columns): # Creates an array of frequency where each index corresponds to the frequency at the same index of the data array
        time_passed_sec = (1.0/sample_rate)*i
        frequency.append(start + (freq_per_sec * time_passed_sec))
    frequency = np.array(frequency)

    # Stack frequency with lock-in data
    data = np.vstack((frequency, data_no_frequency)).transpose()

    # Display data
    print data
