import time, wrapper
from matplotlib import pyplot as plt
import numpy as np


def sweep_parameter(parameter_set_func, values_to_sweep, time_constant=1000.0, sensitivity=0.01, slope=12, sample_rate=512, samples_to_collect=512, load_time=5, lock_in_time=1.0, chopper_amplitude=1, chopper_frequency=50, power=11.5, sweeper_frequency=250):
    """
    This method sweeps a parameter through a set of values. Any parameter can be chosen. If the chosen parameter is represented in one of this functions arguments, whatever is entered for that argument will be ignored,
    :param parameter_set_func: The function that sets the parameter the user wishes to sweep through, i.e. wrapper.set_continuous_wave_freq.
    :param values_to_sweep: The values to sweep the parameter through, i.e. range(200, 301, 2),
    :param time_constant: The lock-in amplifier time constant.
    :param sensitivity: The lock-in amplifier sensitivity.
    :param slope: The lock-in amplifier roll off slope in dB/octave.
    :param sample_rate: The lock-in amplifier sample rate.
    :param samples_to_collect: The number of samples to collect.
    :param load_time: The amount of time to give the instruments to finish setting up before data collection begins.
    :param lock_in_time: The amount of time to give the lock in amplifier to lock back onto the reference signal after a parameter is changed.
    :param chopper_amplitude: The amplitude of the chopper signal.
    :param chopper_frequency: The frequency of the chopper signal.
    :param power: The power of the sweeper.
    :param sweeper_frequency: The frequency of the sweeper.
    :return: The data collected, where the first column is frequency, the second column is X, and the third column is Y.
    """
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
        data_averaged_no_freq = np.mean(data_unaveraged_no_freq, 1)
        data_averaged = np.hstack(([value], data_averaged_no_freq)).flatten()
        data = np.vstack((data, data_averaged))

    # Delete the first row in the collected data, as it was created to give the array shape earlier but holds no useful data
    data = np.delete(data, 0, 0)

    # Close instruments
    wrapper.close()

    # Return data
    return data


def generate_bode_plot(*data_list):
    """
    Generates the appropriate plots from the given data.
    :param data: An arbitrary number of n by 3 arrays, where there are n data points, column 0 is frequency, column 1 is x, and column 2 is y
    """
    count = 0
    for data in data_list:

        # Generate response and phase from the data array
        freq = data[:,0]
        x = data[:,1]
        y = data[:,2]
        response = np.sqrt(np.add(np.square(x), np.square(y))) # r=sqrt(x^2+y^2)
        phase = np.arctan2(y,x) # theta=arctan(y/x)]
        phase_deg = np.degrees(phase)

        # Determine axis scales
        x_max = np.amax(x)
        y_max = np.amax(y)
        subplot1_max = max(x_max, y_max)


        # Define and stylize plots

        plt.figure(count)

        plt.subplot(3,1,1)
        plt.plot(freq, x, 'b-')
        plt.plot(freq, y, 'g-')
        plt.yscale('log')
        plt.ylabel('A [V]')

        plt.subplot(3,1,2)
        plt.plot(freq, response, 'k-')
        plt.yscale('log')
        plt.ylabel('Response [V]')

        plt.subplot(3,1,3)
        plt.plot(freq, phase_deg, 'k-')
        plt.ylabel('Phase [degrees]')
        plt.xlabel('Frequency [GHz]')

        count += 1
    plt.show()


def generate_frequency_list(start, end, step):
    to_return = []
    current_frequency = start
    while(current_frequency <= end):
        to_return.append(current_frequency)
        current_frequency += step
    return to_return

if __name__ == '__main__':

    #data = sweep_parameter(wrapper.set_continuous_wave_freq, generate_frequency_list(230,250,0.2), time_constant=3000, sensitivity=0.005, slope=12, sample_rate=512, samples_to_collect=512, lock_in_time=1.0, chopper_amplitude=1.0, chopper_frequency=50, power=10)
    #np.save('data/col1_sweeper_sweep_200GHz_to_300GHz_col2_X_col3_Y_take2', data)

    filt = np.load('data/filter.npy')
    no_filter = np.load('data/no_filter.npy')

    freq = filt[:, 0]
    filter_x = filt[:, 1]
    filter_y = filt[:, 2]
    no_filter_x = no_filter[:, 1]
    no_filter_y = no_filter[:, 2]

    subtracted_x = np.subtract(filter_x, no_filter_x)
    subtracted_y = np.subtract(filter_y, no_filter_y)

    subtracted = np.vstack((freq, subtracted_x, subtracted_y)).transpose()
    generate_bode_plot(filt, no_filter, subtracted)

    #data = sweep_parameter(wrapper.set_continuous_wave_freq, generate_frequency_list(200,300,1), time_constant=1000, sensitivity=0.5, slope=12, sample_rate=512, samples_to_collect=512, lock_in_time=1.0, chopper_amplitude=1.0, chopper_frequency=50, power=10)
    #np.save('data/filter', data)
