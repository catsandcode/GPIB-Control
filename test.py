#Import libraries
import numpy as np
from matplotlib import pyplot as plt

from control import daq, experiment_wrapper

daq.sweep_parameter(experiment_wrapper.set_freq_synth_frequency, daq.generate_frequency_list(12.5,16.5,4))