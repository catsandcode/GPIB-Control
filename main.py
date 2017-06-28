import time, wrapper
from instruments import PasternackPE11S390
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


def generate_bode_plot(data_list):
    """
    Generates the appropriate plots from the given data.
    :param data: A list of n by 3 arrays, where there are n data points, column 0 is frequency, column 1 is x, and column 2 is y
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
    """
    Generates the list of frequencies between start and end with a step size of step.
    :param start: The start frequency
    :param end: The end frequency
    :param step: The step in between frequencies
    :return: The list of frequencies
    """
    to_return = []
    current_frequency = start
    while(current_frequency <= end):
        to_return.append(current_frequency)
        current_frequency += step
    return to_return


def subtract_reference(reference, sample):
    """
    Subtracts a reference from a sample. Both reference and sample are numpy arrays with frequency in the 0th col, x in the 1st col, and y in the 2nd col.
    :param reference: The reference array.
    :param sample: The sample array.
    :return: The subtracted array (i.e. sample/reference).
    """
    # Extract x and y from the reference and sample
    freq = sample[:, 0]
    sample_x = sample[:, 1]
    sample_y = sample[:, 2]
    reference_x = reference[:, 1]
    reference_y = reference[:, 2]
    # Divide sample x by reference x, do same for y
    subtracted_x = np.divide(sample_x, reference_x)
    subtracted_y = np.divide(sample_y, reference_y)
    # Construct a new array of the subtracted data
    subtracted = np.vstack((freq, subtracted_x, subtracted_y)).transpose()
    # Return the new array
    return subtracted


def subtract2(num, ref, sample):
    freq = ref[:, 0]
    x = ref[:, 1]
    y = ref[:, 2]
    sample_x = sample[:, 1]
    sample_y = sample[:, 2]
    response = np.sqrt(np.add(np.square(x), np.square(y))) # r=sqrt(x^2+y^2)
    sample_response = np.sqrt(np.add(np.square(sample_x), np.square(sample_y))) # r=sqrt(x^2+y^2)

    # Define and stylize plots

    print 'x'
    print sample_x
    print 'y'
    print sample_y

    plt.figure(num)

    plt.subplot(2, 1, 1)
    plt.plot(freq, x, 'y-')
    plt.plot(freq, y, 'm-')
    plt.plot(freq, sample_x, 'r-')
    plt.plot(freq, sample_y, 'g-')
    # plt.yscale('log')
    plt.ylabel('A [V]')

    plt.subplot(2, 1, 2)
    plt.plot(freq, np.divide(sample_response, response), 'k-')
    # plt.yscale('log')
    plt.ylabel('Response')


def sweep_parameter2(parameter_set_func, values_to_sweep, time_constant=1000.0, sensitivity=0.01, slope=12, sample_rate=512, samples_to_collect=512, load_time=5, lock_in_time=1.0, chopper_amplitude=1, chopper_frequency=50, power=7.5, sweeper_frequency=250):
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

    # Sweep the selected parameter and record data
    count = 0
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
        data = wrapper.get_data()
        x_data = data[0, :]
        y_data = data[1, :]

        print 'x'
        print x_data
        print 'y'
        print y_data

        plt.figure(count)
        plt.subplot(1, 2, 1)
        plt.title('X histogram for ' + str(value))
        plt.hist(x_data, 50)

        plt.subplot(1, 2, 2)
        plt.title('Y histogram for ' + str(value))
        plt.hist(y_data, 50)

        count += 1

    plt.show()
    # Close instruments
    wrapper.close()


if __name__ == '__main__':

    power = 15
    chopper_amplitude = 5
    chopper_freq = 5
    time_constant = 300
    sensitivity = 500
    slope = 12
    load_time = 2
    lock_in_time = 0.5

    wrapper.initialize()

    freq_synth = PasternackPE11S390(wrapper.resource_manager, 'USB0::0x2012::0x0011::5001::INSTR')
    freq_synth.open()
    freq_synth.initialize_instrument()

    # Setup sweeper
    freq_synth.set_power(power)

    # Setup chopper
    wrapper.set_chopper_amplitude(chopper_amplitude)
    wrapper.set_chopper_frequency(chopper_freq)
    wrapper.set_chopper_on(True)

    # Setup lock-in
    wrapper.set_time_constant(time_constant)
    wrapper.set_sensitivity(sensitivity)
    wrapper.set_low_pass_slope(slope)
    wrapper.set_data('X', 'Y')

    # Sleep to allow instruments to adjust settings
    time.sleep(load_time)

    # Create a new array to save data to
    data = np.array([0, 0, 0], float)  # This row will be deleted later

    for freq in generate_frequency_list(12, 16, 0.2):
        # Set selected parameter to the given value
        freq_synth.set_frequency(freq)
        print 'At frequency value ' + str(freq_synth.get_frequency())
        # Sleep to allow lock-in to lock to new frequency and for time constant to average
        time.sleep((time_constant * 5.0 / 1000.0) + lock_in_time)  # Sleep for five time constants plus the lock_in_time
        # Snap the data
        (x, y) = wrapper.snap_data()
        print 'x:' + str(x)
        print 'y:' + str(y)
        # Get data from the lock-in amplifier and average
        data_averaged = np.hstack((freq, x, y))
        data = np.vstack((data, data_averaged))

    # Delete the first row in the collected data, as it was created to give the array shape earlier but holds no useful data
    data = np.delete(data, 0, 0)

    freq_synth.close()
    # Close instruments
    wrapper.close()

    freq = data[:, 0]
    x = data[:, 1]
    y = data[:, 2]

    plt.figure(0)

    plt.plot(freq, x, 'r-')
    plt.plot(freq, y, 'b-')

    plt.show()

    """
    data_list = []
    for i in range(10):
        data = np.load('data/repeat_sweep_trial_' + str(i)+'.npy')
        data_list.append(data)

    #generate_bode_plot(data_list)
    
    subtracted_list = []
    for i in range(1, 10):
        subtracted_list.append(subtract_reference(data_list[0], data_list[i]))
    plt.show()
    

    #sweep_parameter2(wrapper.set_sample_rate, [512, 256, 128, 8, 1], time_constant=1000, sensitivity=0.5, slope=12, sample_rate=8, samples_to_collect=8, lock_in_time=1.0, chopper_amplitude=1.0, chopper_frequency=20, power=7.5)

    for i in range(10):
        data = sweep_parameter(wrapper.set_continuous_wave_freq, generate_frequency_list(220, 260, 1), time_constant=1000, sensitivity=0.5, slope=12, sample_rate=8, samples_to_collect=8, lock_in_time=1.0, chopper_amplitude=1.0, chopper_frequency=5, power=7.5)
        np.save('data/repeat_sweep_trial_' + str(i), data)

    data = np.load('data/data collection week 1/col1_sweeper_sweep_200GHz_to_300GHz_col2_X_col3_Y.npy')
    print data
    generate_bode_plot([data])
    """
