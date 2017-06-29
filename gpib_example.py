from __future__ import division, print_function

import time

from gpib_manager import Prologix

# Initialize communications with the yellow Prologix controller.
# /dev/ttyUSB0 is the serial port ID and could change depending on
# how many are plugged in.
prologix0 = Prologix('/dev/tty.usbserial-PXHB40P8')

# Initialize communication with a device
agilent = prologix0.get_device_interface(10) # 9 is the GPIB address

# "Ask" works like you're used to.  It sends a command and returns the result.
# There is a timeout if the device doesn't send anything.
# Don't forget the \n or the device won't know the command was completed!
print("Ask test 1 (Should show Agilent identity):", agilent.query("*IDN?\n"))

# We could do the same thing with separate write and read commands
agilent.write("*IDN?\n")
print("Read test (Should show Agilent identity):", agilent.read())

# Reset the power supply
agilent.write("*RST\n")
