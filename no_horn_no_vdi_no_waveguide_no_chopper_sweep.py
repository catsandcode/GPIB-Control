from setup_control import experiment_wrapper
import numpy as np
import time

"""
Sweeps from 12.5GHz to 16.5GHz in 25MHz steps. Power of the frequency synthesizer is set to 8dBm in an attempt to get out of the diode's saturation range. Returns values in volts.
"""

for i in range(0, 3):
    experiment_wrapper.initialize()

    # Disable chopper
    experiment_wrapper.set_chopper_on(False)

    # Set the frequency multiplier, as it is particular to the experiment
    experiment_wrapper.set_freq_multiplier(1)

    # Setup the frequency synthesizer
    experiment_wrapper.set_freq_synth_power(8.0)
    experiment_wrapper.set_freq_synth_enable(True)

    # Sleep to allow instruments to adjust settings
    time.sleep(5)

    # Create a new array to save data to
    data = np.array([0, 0], float)  # This row will be deleted later

    # Sweep the selected parameter and record data
    for freq in np.linspace(12.5, 16.5, num=160, endpoint=True):
        print('At frequency ' + str(freq))

        # Set selected parameter to the given value
        experiment_wrapper.set_freq_synth_frequency(freq)

        # Sleep to allow multimeter to reset and then clear buffer
        time.sleep(2)  # Sleep for 1 seconds
        experiment_wrapper.multimeter.reset()

        # Sleep to allow multimeter to adjust to the new voltage
        time.sleep(3)  # Sleep for 1 seconds

        # Get data from the multimeter and add it to the data array
        voltage = experiment_wrapper.get_multimeter_dc_measurement()

        data_row = np.array([freq, voltage])
        data = np.vstack((data, data_row))

    # Delete the first row in the collected data, as it was created to give the array shape earlier but holds no useful data
    data = np.delete(data, 0, 0)

    # Close instruments
    experiment_wrapper.close()

    # Save collected data
    np.savez('no_horn_no_vdi_no_waveguide_no_chopper_sweep_data_folder/sweep_num_' + str(i), data=data)