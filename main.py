import time, math, wrapper
from matplotlib import pyplot as plt
import numpy as np


def main():
    wrapper.initialize()

    # Constants
    chopper_sweep_start = 1
    chopper_sweep_stop = 120
    chopper_sweep_step = 1
    sample_rate = 512

    # Setup sweeper
    wrapper.set_continuous_wave_freq(200)
    wrapper.set_power(9.5)

    # Setup chopper
    wrapper.set_chopper_amplitude(1)
    wrapper.set_chopper_sweep_on(False)

    # Setup lock-in
    wrapper.set_time_constant(300.0)
    wrapper.set_low_pass_slope(18)
    wrapper.set_sensitivity(0.005)
    wrapper.set_sample_rate(sample_rate)
    wrapper.set_data('R', 'Theta')

    # Start the scan
    wrapper.start_scan()
    wrapper.start_sweep()
    start_time = time.time()

    # Sleep
    time.sleep(20)

    # Stop the scan and record the time
    wrapper.stop_scan()
    stop_time = time.time()

    # Get data from the lock-in amplifier
    data_no_frequency = wrapper.get_data()
    (data_rows, data_columns) = data_no_frequency.shape

    # Figure out the frequency at each data point
    daq_time = stop_time - start_time
    freq_per_sec = (chopper_sweep_stop - chopper_sweep_start) / daq_time

    frequency = []
    for i in range(
            data_columns):  # Creates an array of frequency where each index corresponds to the frequency at the same index of the data array
        time_passed_sec = (1.0 / sample_rate) * i
        frequency.append(chopper_sweep_start + (freq_per_sec * time_passed_sec))
    frequency = np.array(frequency)

    # Stack frequency with lock-in data
    data = np.vstack((frequency, data_no_frequency)).transpose()

    # Save data
    np.save('data/col1_chopper_sweep_1kHz_to_120kHz_col2_R_col3_Theta', data)

def sweep_chopper_freq_script():
    wrapper.initialize()

    # Constants
    chopper_sweep_start = 1
    chopper_sweep_stop = 140
    chopper_sweep_step = 10
    sample_rate = 512
    lock_in_sensitivity = 300.0

    # Setup sweeper
    wrapper.set_continuous_wave_freq(200)
    wrapper.set_power(9.5)

    # Setup chopper
    wrapper.set_chopper_amplitude(1)
    wrapper.set_chopper_on(True)

    # Setup lock-in
    wrapper.set_time_constant(lock_in_sensitivity)
    wrapper.set_low_pass_slope(18)
    wrapper.set_sensitivity(0.01)
    wrapper.set_sample_rate(sample_rate)
    wrapper.set_data('X', 'Y')

    # Create a new array to save data to
    data = np.array([0,0,0], float)

    # Sweep the chopper frequency and record data
    for freq in range(chopper_sweep_start, chopper_sweep_stop, chopper_sweep_step):
        # Set the frequency to chop at
        wrapper.set_chopper_frequency(freq)
        # Sleep to allow lock-in to lock to new frequency
        time.sleep(1)
        # Start the scan
        wrapper.start_scan()
        # Sleep for one second to collect data
        time.sleep((lock_in_sensitivity*5.0)/1000.0)
        # Stop the scan
        wrapper.stop_scan()
        # Get data from the lock-in amplifier and average
        data_unaveraged_no_freq = wrapper.get_data()
        data_averaged_no_freq = np.mean(data_unaveraged_no_freq, 1)
        data_averaged = np.hstack(([freq], data_averaged_no_freq)).flatten()
        data = np.vstack((data, data_averaged))

    print data

    freq = data[:,0]
    x = data[:,1]
    y = data[:,2]
    response = np.sqrt(np.add(np.square(x), np.square(y))) # r=sqrt(x^2+y^2)
    theta = np.arctan(np.divide(y,x)) # theta=arctan(y/x)


    plt.figure(1)

    plt.subplot(2,2,1)
    plt.plot(freq, response, 'g-')

    plt.subplot(2,2,2)
    plt.plot(freq, phase, 'r-')

    plt.subplot(2,2,3)
    plt.plot(freq, phase, 'r-')

    plt.subplot(2,2,4)
    plt.plot(freq, phase, 'r-')


    plt.show()

    # Stack frequency with lock-in data
    #data = np.vstack((frequency, data_no_frequency)).transpose()

    # Save data
    #np.save('data/col1_chopper_sweep_1kHz_to_120kHz_col2_R_col3_Theta', data)

if __name__ == '__main__':
    sweep_chopper_freq_script()
