import numpy as np
from matplotlib import pyplot as plt

# Load data
data = np.load('lock_in_sample_wait_time.npy')

# Define helper function
def calc_response_phase(x, y):
    response = np.sqrt(np.add(np.square(x), np.square(y)))
    phase = np.degrees(np.arctan2(y, x))
    return response, phase

# Define x-axis
times = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0, 30.0, 40.0, 50.0, 60.0] # Referred to lock_in_sample_wait_time.py for these values

# Get shape of data
rows, cols = data.shape

# Create plot
fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True)

# Iterate through data two rows at a time
for row in range(0, rows, 2):
    # Find row frequency
    x_freq = data[row, 0]
    y_freq = data[row + 1, 0]
    # Only continue to plot if frequencies are equal
    if x_freq == y_freq:
        # Load data at row
        row_label = "{0:.3f}".format(x_freq)
        x = data[row, 1:]
        y = data[row + 1, 1:]
        # Calculate response and phase
        response, phase = calc_response_phase(x, y)
        # Plot
        axs[0].plot(times, response, label=row_label)
        axs[1].plot(times, phase, label=row_label)

# Configure plot
axs[0].set_ylabel('response [V]')
axs[1].set_ylabel('phase [deg]')
axs[1].set_xlabel('time [sec]')

axs[0].ticklabel_format(style='sci', scilimits=(0,0), axis='y')
axs[1].ticklabel_format(style='sci', scilimits=(0,0), axis='y')

axs[0].set_xscale('log')

axs[0].legend()
axs[1].legend()

# Show plot
plt.show()

