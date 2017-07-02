"""
The daq module provides functions that might be useful for performing measurements and analyzing data. Some functions
<<<<<<< HEAD:control/daq.py
in the module are completely unrelated to data aquisition, and are purely analysis. It is essentially a module of code
=======
>>>>>>> 9754758e5841681524985c7d2b92ed739240c4b2:control/daq.py
in the module are completely unrelated to data acquisition, and are purely analysis. It is essentially a module of code
that would otherwise be repeated lots of times in experiment runs.
"""

<<<<<<< HEAD:control/daq.py
<<<<<<< HEAD:control/daq.py
import time, experiment_wrapper
from matplotlib import pyplot as plt
=======
import time
import control.experiment_wrapper as experiment_wrapper
>>>>>>> 9754758e5841681524985c7d2b92ed739240c4b2:control/daq.py
=======
import time
import control.experiment_wrapper as experiment_wrapper
>>>>>>> 9754758e5841681524985c7d2b92ed739240c4b2:control/daq.py
import numpy as np
from matplotlib import pyplot as plt


def calculate_response_and_phase(sweep):
    """
    This function takes an array where the first column is frequency, the second is x, and the third is y and returns
    an array where the first column is frequency, the second column is response, and the third column is phase.
    :param sweep: The array where the first column is frequency, the second is x, and the third is y.
<<<<<<< HEAD:control/daq.py
    :return: An array where the first column is frequency, the second column is response, and the third column is phase.x
=======
>>>>>>> 9754758e5841681524985c7d2b92ed739240c4b2:control/daq.py
    :return: An array where the first column is frequency, the second column is response, and the third column is phase.
    """
    # Extract data from the sweep array
    try:
        freq = sweep[:, 0]
        x = sweep[:, 1]
        y = sweep[:, 2]
    except IndexError:
        raise ValueError('Array does not have three columns.')
    # Calculate response and phase
    response = np.sqrt(np.add(np.square(x), np.square(y)))  # r=sqrt(x^2+y^2)
    phase = np.degrees(np.arctan2(y, x))  # theta=arctan(y/x)]
    # Return a new array where the first column is frequency, the second is response, and the third is phase
    return np.vstack((freq, response, phase)).transpose()


def subtract_reference(reference, sweep):
    """
    This function takes a reference sweep array and a sweep array. The reference sweep is subtracted from the sweep and
    displayed. Subtraction takes place by first finding the response and phase of the reference sweep and the sweep. The
    response of the sweep is then divided by the response of the reference. Finally the phase of the reference is
    subtracted from the phase of the sweep.
    :param reference: The reference sweep in an array where the first column is frequency, the second column is x, and
    the third column is y.
    :param sweep: The sweep  in an array where the first column is frequency, the second column is x, and the third
    column is y.
    :return: A an
    """
    # Test array frequency equality
    ref_freq = reference[:, 0]
    test_freq = sweep[:, 0]
    if np.array_equal(ref_freq, test_freq) is not True:
        raise ValueError('Passed arrays do not have the same frequency values.')

    # Extract data from the reference and test arrays
    freq = ref_freq
    ref_x = reference[:, 1]
    ref_y = reference[:, 2]

    test_x = sweep[:, 1]
    test_y = sweep[:, 2]

    # Calculate the response and phase
    ref_response = np.sqrt(np.add(np.square(ref_x), np.square(ref_y))) # r=sqrt(x^2+y^2)
    test_response = np.sqrt(np.add(np.square(test_x), np.square(test_y))) # r=sqrt(x^2+y^2)

    ref_phase = np.degrees(np.arctan2(ref_y, ref_x)) # theta=arctan(y/x)]
    test_phase = np.degrees(np.arctan2(test_y, test_x)) # theta=arctan(y/x)]

    #Subtract the reference from the test

    response = np.divide(test_response, ref_response)
    phase = np.subtract(test_phase, ref_phase)

    return response, phase


def print_attributes(sweep):
    """
    Prints the attributes associated with the sweep to the console. This should be included in notes about each sweep.
    :param sweep: The sweep to extract attributes from.
    """
    to_print = ''
    for key in sweep.keys():
        # If this is not the data key, add the key and the key's value to to_print
        if key != 'data':
            to_print += key + ': ' + str(sweep[key])
        # Append units
        if key == 'slope':
            to_print += 'dB/oct'
        elif key == 'power':
            to_print += 'dBm'
        elif key == 'lock_in_time':
            to_print += 's'
        elif key == 'sensitivity':
            to_print += 'mV'
        elif key == 'chopper_frequency':
            to_print += 'kHz'
        elif key == 'chopper_amplitude':
            to_print += 'V'
        elif key == 'load_time':
            to_print += 's'
        elif key == 'time_constant':
            to_print += 'ms'
        elif key == 'freq_synth_frequency':
            to_print += 'GHz'
        # If this is not the data key, add a new line
        if key != 'data':
            to_print += '\n'
    print(to_print)


def save_x_and_y_graphs(sweep, path):
    """
    This function saves a graph of x versus frequency and a graph of y versus frequency to the specified path. The
    suffixes _x and _y are appended to the x and y graphs, respectively.
    :param sweep: The sweep to print the x and y graphs from.
    :param path: The path to save the graphs at.
    """
    data = sweep['data']
    plt.figure(0)
    plt.plot(data[:,0], data[:,1])
    plt.xlabel('Frequency [GHz]')
    plt.ylabel('X Amplitude [V]')
    plt.savefig(path + '_x')
    plt.figure(1)
    plt.plot(data[:,0], data[:,2])
    plt.xlabel('Frequency [GHz]')
    plt.ylabel('Y Amplitude [V]')
    plt.savefig(path + '_y')


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
    while current_frequency <= end:
        to_return.append(current_frequency)
        current_frequency += step
    return to_return


def sweep_parameter(parameter_set_func, values_to_sweep, time_constant=10, sensitivity=10, slope=12, load_time=5, lock_in_time=1.0, chopper_amplitude=5, chopper_frequency=5, power=15, freq_synth_frequency=250, multiplier=18, save_path=''):
    """
    This method sweeps a parameter through a set of values. Any parameter can be chosen. If the chosen parameter is represented in one of this functions arguments, whatever is entered for that argument will be ignored,
    :param parameter_set_func: The function that sets the parameter the user wishes to sweep through, i.e. wrapper.set_continuous_wave_freq.
    :param values_to_sweep: The values to sweep the parameter through, i.e. range(200, 301, 2),
    :param time_constant: The lock-in amplifier time constant.
    :param sensitivity: The lock-in amplifier sensitivity.
    :param slope: The lock-in amplifier roll off slope in dB/octave.
    :param load_time: The amount of time to give the instruments to finish setting up before data collection begins.
    :param lock_in_time: The amount of time to give the lock in amplifier to lock back onto the reference signal after a parameter is changed.
    :param chopper_amplitude: The amplitude of the chopper signal.
    :param chopper_frequency: The frequency of the chopper signal.
    :param power: The power of the sweeper.
    :param freq_synth_frequency: The frequency of the sweeper.
    :param multiplier: The multiplier (i.e. product of all frequency multipliers in the setup).
    :param save_path: If a non-empty string variable save_path is passed the the sweep will be saved as a .npy file with the sweep settings saved in metadata.
    :return: The data collected, where the first column is frequency, the second column is X, and the third column is Y.
    """
    experiment_wrapper.initialize()
    
    # Set the frequency multiplier, as it is particular to the experiment
    experiment_wrapper.set_freq_multiplier(multiplier)

    # Setup the frequency synthesizer
    experiment_wrapper.set_freq_synth_frequency(freq_synth_frequency)
    experiment_wrapper.set_freq_synth_power(power)
    experiment_wrapper.set_freq_synth_enable(True)

    # Setup chopper
    experiment_wrapper.set_chopper_amplitude(chopper_amplitude)
    experiment_wrapper.set_chopper_frequency(chopper_frequency)
    experiment_wrapper.set_chopper_on(True)

    # Setup lock-in
    experiment_wrapper.set_time_constant(time_constant)
    experiment_wrapper.set_sensitivity(sensitivity)
    experiment_wrapper.set_low_pass_slope(slope)

    # Sleep to allow instruments to adjust settings
    time.sleep(load_time)

    # Create a new array to save data to
    data = np.array([0,0,0], float)  # This row will be deleted later

    # Sweep the selected parameter and record data
    for value in values_to_sweep:
        print('At sweep value ' + str(value))

        # Set selected parameter to the given value
        parameter_set_func(value)

        # Sleep to allow lock-in to lock to new frequency and for time constant to average
        time.sleep((time_constant * 5.0 / 1000.0) + lock_in_time)  # Sleep for five time constants plus the lock_in_time

        # Get data from the lock-in amplifier and and add it to the data array
        (x, y) = experiment_wrapper.snap_data()

        data_row = np.array([value, x, y])
        data = np.vstack((data, data_row))

    # Delete the first row in the collected data, as it was created to give the array shape earlier but holds no useful data
    data = np.delete(data, 0, 0)

    # Close instruments
    experiment_wrapper.close()
    
    if save_path != '':
        np.savez(save_path, data = data, parameter_set_func=str(parameter_set_func), time_constant=time_constant, sensitivity=sensitivity, slope=slope, load_time=load_time, lock_in_time=lock_in_time, chopper_amplitude=chopper_amplitude, chopper_frequency=chopper_frequency, power=power, freq_synth_frequency=freq_synth_frequency, multiplier=multiplier)

    # Return data
    return data
