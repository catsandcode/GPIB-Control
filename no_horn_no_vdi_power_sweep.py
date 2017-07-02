from control import daq, experiment_wrapper
import numpy as np

for power in np.arange(8.0, 15.0, 0.5):
    if power >= 12.0:
        daq.sweep_parameter(experiment_wrapper.set_freq_synth_frequency, np.arange(12.5, 16.5, 0.1), power=power,
                            time_constant=100, sensitivity=50, load_time=1.5, lock_in_time=0.1, multiplier=1,
                            save_path='no_horn_no_vdi_power_sweep_data_folder/power_' + str(power))
    daq.sweep_parameter(experiment_wrapper.set_freq_synth_frequency, np.arange(12.5, 16.5, 0.1), power=power,
                        time_constant=100, sensitivity=10, load_time=1.5, lock_in_time=0.1, multiplier=1,
                        save_path='no_horn_no_vdi_power_sweep_data_folder/power_' + str(power))
