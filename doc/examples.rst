examples
========

The following example program will sweep through a set of frequencies. At each frequency, the program will sample x and y multiple times after changing to its current frequency.

.. literalinclude:: ../lock_in_sample_wait_time.py
   :language: python

Although it is not strictly the goal of this library to visualize and analyze data, the following code has been provided to show how the data collected in the previous example might be visualized and analyzed.

.. literalinclude:: ../lock_in_sample_wait_time_analysis.py
   :language: python

This script will display the plot below when run.

.. image:: ../figures/lock_in_sample_wait_time_analysis_plot.png
