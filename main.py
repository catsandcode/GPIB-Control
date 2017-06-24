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
    chopper_sweep_step = 1
    sample_rate = 512
    time_constant = 1000.0
    lock_in_time = 1.0

    # Setup sweeper
    wrapper.set_continuous_wave_freq(200)
    wrapper.set_power(9.5)

    # Setup chopper
    wrapper.set_chopper_amplitude(1)
    wrapper.set_chopper_on(True)

    # Setup lock-in
    wrapper.set_time_constant(time_constant)
    wrapper.set_low_pass_slope(18)
    wrapper.set_sensitivity(0.01)
    wrapper.set_sample_rate(sample_rate)
    wrapper.set_data('X', 'Y')

    # Create a new array to save data to
    data = np.array([0,0,0], float)  # This row will be deleted later

    # Sweep the chopper frequency and record data
    for freq in range(chopper_sweep_start, chopper_sweep_stop, chopper_sweep_step):
        # Set the frequency to chop at
        wrapper.set_chopper_frequency(freq)
        # Sleep to allow lock-in to lock to new frequency and for time constant to average
        time.sleep((time_constant*5.0)/1000.0)
        # Start the scan
        wrapper.start_scan()
        # Sleep for one second to collect data
        time.sleep((time_constant*5.0/1000.0) + lock_in_time)
        # Stop the scan
        wrapper.stop_scan()
        # Get data from the lock-in amplifier and average
        data_unaveraged_no_freq = wrapper.get_data()
        data_averaged_no_freq = np.mean(data_unaveraged_no_freq, 1)
        data_averaged = np.hstack(([freq], data_averaged_no_freq)).flatten()
        data = np.vstack((data, data_averaged))

    # Delete the first row in the collected data, as it was created to give the array shape earlier but holds no useful data
    np.delete(data, 0, 0)

    # Save data
    np.save('data/col1_chopper_sweep_1kHz_to_120kHz_col2_R_col3_Theta', data)

    # Close instruments
    wrapper.close()


def sweep_parameter(parameter_set_func, values_to_sweep, time_constant=1000.0, sensitivity=0.01, slope=12, sample_rate=512, samples_to_collect=512, load_time=5, lock_in_time=1.0, chopper_amplitude=1, chopper_frequency=50, power=11.5, sweeper_frequency=250):
    wrapper.initialize()

    # Setup sweeper
    wrapper.set_continuous_wave_freq(sweeper_frequency)
    wrapper.set_power(power)

    # Setup chopper
    wrapper.set_chopper_amplitude(chopper_amplitude)
    wrapper.set_chopper_frequency(chopper_frequency)
    wrapper.set_chopper_on(True)

    # Setup lock-in
    wrapper.set_time_constant(time_constant)
    wrapper.set_sensitivity(sensitivity)
    wrapper.set_low_pass_slope(slope)
    wrapper.set_sample_rate(sample_rate)
    wrapper.set_data('X', 'Y')

    # Sleep to allow instruments to adjust settings
    time.sleep(load_time)

    # Do some math
    data_collection_sleep_time = float(samples_to_collect)/float(sample_rate)

    # Create a new array to save data to
    data = np.array([0,0,0], float)  # This row will be deleted later

    # Sweep the selected parameter and record data
    for value in values_to_sweep:
        print 'At sweep value ' + str(value)
        # Set selected parameter to the given value
        parameter_set_func(value)
        # Sleep to allow lock-in to lock to new frequency and for time constant to average
        time.sleep((time_constant * 5.0 / 1000.0) + lock_in_time)  # Sleep for five time constants plus the lock_in_time
        # Start the scan
        wrapper.start_scan()
        # Sleep for one second to collect data
        time.sleep(data_collection_sleep_time)
        # Stop the scan
        wrapper.stop_scan()
        # Get data from the lock-in amplifier and average
        data_unaveraged_no_freq = wrapper.get_data()
        print data_unaveraged_no_freq
        data_averaged_no_freq = np.mean(data_unaveraged_no_freq, 1)
        data_averaged = np.hstack(([value], data_averaged_no_freq)).flatten()
        data = np.vstack((data, data_averaged))

    # Delete the first row in the collected data, as it was created to give the array shape earlier but holds no useful data
    data = np.delete(data, 0, 0)

    # Close instruments
    wrapper.close()

    # Return data
    return data


def generate_bode_plot(data, sensitivity=0):
    """
    Generates the appropriate plots from the given data.
    :param data: A n by 3 array, where there are n data points, column 0 is frequency, column 1 is x, and column 2 is y
    """

    # Generate response and phase from the data array
    freq = data[:,0]
    x = data[:,1]
    y = data[:,2]
    response = np.sqrt(np.add(np.square(x), np.square(y))) # r=sqrt(x^2+y^2)
    phase = np.arctan2(y,x) # theta=arctan(y/x)]

    # Define and stylize plots

    plt.figure(1)

    plt.subplot(3,1,1)
    plt.plot(freq, x, 'b-')
    plt.plot(freq, y, 'g-')
    plt.ylabel('(uV)')

    plt.subplot(3,1,2)
    plt.plot(freq, response, 'k-')
    plt.ylabel('Response (uV)')

    plt.subplot(3,1,3)
    plt.plot(freq, phase, 'k-')
    plt.ylabel('Phase (radians)')
    plt.xlabel('Frequency (kHz)')

    plt.show()


if __name__ == '__main__':
    #sweep_chopper_freq_script()

    #data = np.load('data/col1_chopper_sweep_1kHz_to_120kHz_col2_R_col3_Theta.npy')
    #data = np.delete(data, 0, 0)
    #generate_bode_plot(data)

    data = sweep_parameter(wrapper.set_continuous_wave_freq, [10.0*18, 11.0*18, 12.0*18, 12.5*18, 13.0*18, 13.5*18, 14.0*18, 14.5*18, 15.0*18, 15.5*18, 16.0*18, 17.0*18, 18.0*18, 19.0*18, 20.0*18], time_constant=300, sensitivity=2, slope=12, sample_rate=512, samples_to_collect=512, lock_in_time=1.0, chopper_amplitude=1.0, chopper_frequency=50, power=11.5)
    print data
