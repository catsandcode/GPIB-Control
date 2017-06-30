from matplotlib import pyplot as plt
import numpy as np


def generate_bode_plot(reference, test):
    # Test array frequency equality
    ref_freq = reference[:, 0]
    test_freq = test[:, 0]
    if np.array_equal(ref_freq, test_freq) is not True:
        raise ValueError('Passed arrays do not have the same frequency values.')

    # Extract data from the reference and test arrays
    freq = ref_freq
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
    #plt.legend(handles=[ref_x_plt, ref_y_plt, test_x_plt, test_y_plt])
    plt.yscale('log')
    plt.ylabel('Amplitude [V]')

    plt.subplot(3, 1, 2)
    plt.plot(freq, response, 'k-')
    #plt.yscale('log')
    plt.ylabel('Response [test/reference]')

    plt.subplot(3, 1, 3)
    plt.plot(freq, phase, 'k-')
    plt.ylabel('Phase [degrees]')
    plt.xlabel('Frequency [GHz]')

    plt.show()

if __name__ == '__main__':
