import time, wrapper
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


def sweep_parameter(parameter_set_func, values_to_sweep, time_constant=10, sensitivity=10, slope=12, load_time=5, lock_in_time=1.0, chopper_amplitude=5, chopper_frequency=5, power=15, freq_synth_frequency=250, multiplier=18, save_path=''):
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
    :param multiplier: The multiplier (i.e. product of all frequency multipliers in the setup).
    :param save_path: If a non-empty string variable save_path is passed the the sweep will be saved as a .npy file with the sweep settings saved in metadata.
    :return: The data collected, where the first column is frequency, the second column is X, and the third column is Y.
    """
    wrapper.initialize()
    
    # Set the frequency multiplier, as it is particular to the experiment
    wrapper.set_freq_multiplier(multiplier)

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
    
    if save_path != '':
        np.savez(save_path, data = data, parameter_set_func=str(parameter_set_func), time_constant=time_constant, sensitivity=sensitivity, slope=slope, load_time=load_time, lock_in_time=lock_in_time, chopper_amplitude=chopper_amplitude, chopper_frequency=chopper_frequency, power=power, freq_synth_frequency=freq_synth_frequency, multiplier=multiplier)

    # Return data
    return data


if __name__ == '__main__':
    sweep_parameter(wrapper.set_freq_synth_frequency, generate_frequency_list(12.5, 16.5, 0.05), save_path='no_virginia_diode', power=15, sensitivity=1000, multiplier=1)
