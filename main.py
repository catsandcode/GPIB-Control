import time, wrapper
from matplotlib import pyplot as plt
import numpy as np


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


def sweep_parameter(parameter_set_func, values_to_sweep, time_constant=10, sensitivity=10, slope=12, load_time=5, lock_in_time=1.0, chopper_amplitude=5, chopper_frequency=5, power=15, freq_synth_frequency=250):
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

    # Setup the frequency synthesizer
    wrapper.set_freq_synth_frequency(freq_synth_frequency)
    wrapper.set_freq_synth_power(power)
    wrapper.set_freq_synth_enable(True)

    # Setup chopper
    wrapper.set_chopper_amplitude(chopper_amplitude)
    wrapper.set_chopper_frequency(chopper_frequency)
    wrapper.set_chopper_on(True)

    # Setup lock-in
    wrapper.set_time_constant(time_constant)
    wrapper.set_sensitivity(sensitivity)
    wrapper.set_low_pass_slope(slope)

    # Sleep to allow instruments to adjust settings
    time.sleep(load_time)

    # Create a new array to save data to
    data = np.array([0,0,0], float)  # This row will be deleted later

    # Sweep the selected parameter and record data
    for value in values_to_sweep:
        print 'At sweep value ' + str(value)

        # Set selected parameter to the given value
        parameter_set_func(value)

        # Sleep to allow lock-in to lock to new frequency and for time constant to average
        time.sleep((time_constant * 5.0 / 1000.0) + lock_in_time)  # Sleep for five time constants plus the lock_in_time

        # Get data from the lock-in amplifier and and add it to the data array
        (x, y) = wrapper.snap_data()

        data_row = np.array([value, x, y])
        data = np.vstack((data, data_row))

    # Delete the first row in the collected data, as it was created to give the array shape earlier but holds no useful data
    data = np.delete(data, 0, 0)

    # Close instruments
    wrapper.close()

    # Return data
    return data


def generate_bode_plot(reference, test):

    # Extract data from the reference and test arrays
    freq = reference[:, 0]
    ref_x = reference[:, 1]
    ref_y = reference[:, 2]

    test_x = test[:, 1]
    test_y = test[:, 2]

    # Calculate the response and phase
    ref_response = np.sqrt(np.add(np.square(ref_x), np.square(ref_y))) # r=sqrt(x^2+y^2)
    test_response = np.sqrt(np.add(np.square(test_x), np.square(test_y))) # r=sqrt(x^2+y^2)

    ref_phase = np.degrees(np.arctan2(ref_y, ref_x)) # theta=arctan(y/x)]
    test_phase = np.degrees(np.arctan2(test_y, test_x)) # theta=arctan(y/x)]

    #Subtract the reference from the test

    response = np.divide(test_response, ref_response)
    phase = np.subtract(test_phase, ref_phase)

    # Plot the data
    plt.subplot(3, 1, 1)
    ref_x_plt = plt.plot(freq, ref_x, 'r--')
    ref_y_plt = plt.plot(freq, ref_y, 'r-.')
    test_x_plt = plt.plot(freq, test_x, 'k--')
    test_y_plt = plt.plot(freq, test_y, 'k-.')
    plt.legend(handles=[ref_x_plt, ref_y_plt, test_x_plt, test_y_plt])
    plt.yscale('log')
    plt.ylabel('Amplitude [V]')

    plt.subplot(3, 1, 2)
    plt.plot(freq, response, 'k-')
    plt.yscale('log')
    plt.ylabel('Response [test/reference]')

    plt.subplot(3, 1, 3)
    plt.plot(freq, phase, 'k-')
    plt.ylabel('Phase [degrees]')
    plt.xlabel('Frequency [GHz]')

    plt.show()


if __name__ == '__main__':
    """
    ref = sweep_parameter(wrapper.set_freq_synth_frequency, generate_frequency_list(200, 300, 1))
    test = sweep_parameter(wrapper.set_freq_synth_frequency, generate_frequency_list(200, 300, 1))
    np.save('ref', ref)
    np.save('test', test)
    """
    ref = np.load('data/sweep_220GHz_to_240GHz_half_GHz_step_1st_run.npy')
    #generate_bode_plot(ref, test)

    freq = ref[:, 0]
    ref_x = ref[:, 1]
    ref_y = ref[:, 2]

    plt.figure(1)
    plt.plot(freq, ref_x, 'r-')
    plt.plot(freq, ref_y, 'b-')
    plt.show()