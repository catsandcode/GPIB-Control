from matplotlib import pyplot as plt
import numpy as np


def calculate_response_and_phase(sweep):
    """
    This function takes an array where the first column is frequency, the second is x, and the third is y and returns
    an array where the first column is frequency, the second column is response, and the third column is phase.
    :param sweep: The array where the first column is frequency, the second is x, and the third is y.
    :return: An array where the first column is frequency, the second column is response, and the third column is phase.x
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
    return np.hstack((freq, response, phase))


def subtract_reference(reference, sweep):

    """
    This function takes a reference sweep and a sweep. The reference sweep is subtracted from the sweep and displayed.
    Subtraction takes place by first finding the response and phase of the reference sweep and the sweep. The response
    of the sweep is then divided by the response of the reference. Finally the phase of the reference is subtracted
    from the phase of the sweep.
    :param reference: The reference sweep.
    :param sweep: The sweep.
    :return: A tuple of form (response, phase).
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

    return (response, phase)
    # Plot the data
    plt.subplot(2, 2, 1)
    plt.plot(freq, ref_x, 'b--')
    plt.plot(freq, test_x, 'k-')
    plt.ylabel('X Amplitude [V]')

    plt.subplot(2, 2, 2)
    plt.plot(freq, ref_y, 'b--.')
    plt.plot(freq, test_y, 'k-.')
    plt.ylabel('Y Amplitude [V]')
    plt.xlabel('Frequency [GHz]')

    plt.subplot(2, 2, 3)
    plt.plot(freq, response, 'k-')
    plt.ylabel('Response')

    plt.subplot(2, 2, 4)
    plt.plot(freq, phase, 'k-')
    plt.ylabel('Phase [degrees]')
    plt.xlabel('Frequency [GHz]')

    plt.show()


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
    print to_print

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


if __name__ == '__main__':
    sweep = np.load('data/no_virginia_diode.npz')
    save_x_and_y_graphs(sweep, 'data/no_virginia_diode')
