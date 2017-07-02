from control import daq, experiment_wrapper
import numpy as np

for power in np.arange(8.0, 15.0, 0.5):
    daq.sweep_parameter(experiment_wrapper.set_freq_synth_frequency, np.arange(12.5, 16.5, 0.1), power=power, time_constant=100, sensitivity=500, load_time=3, lock_in_time=0.1, save_path='no_horn_no_vdi_power_sweep_data_folder/power_' + str(power))
