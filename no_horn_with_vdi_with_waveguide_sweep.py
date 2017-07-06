from control.daq import sweep_parameter
from control.experiment_wrapper import set_freq_synth_frequency
import numpy as np

for i in range(0, 3):
    sweep_parameter(set_freq_synth_frequency, np.linspace(12.5, 16.5, num=500, endpoint=True), time_constant=30,  sensitivity=10, load_time=0.5, lock_in_time=0.1, multiplier=1,
                    save_path='no_horn_with_vdi_with_waveguide_sweep_data_folder/sweep_num_' + str(i))
