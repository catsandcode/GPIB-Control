'''
A set of classes to facilitate interfacing with GPIB devices over serial
'''

from __future__ import division, print_function

import serial
import sys
import traceback
import time
import logging
import multiprocessing


# To access serial ports on Ubunutu, run "sudo adduser USERNAMEHERE dialout" and log out/in

'''
A class which handles communication with a Prologix GPIB-USB module.
Be sure to wrap your critial sections in the hw_lock!  Use "with" block.
'''
class Prologix():
	
	'''
	Initializes serial communication with the GPIB-USB module.
	
	Arguments:
	   comPort - A string containing the name of the com port.  Defaults to
			 the integer 0, which refers to the first available serial port.
	   readTimeout - The number of seconds to wait before giving up while reading.
	''' 
	def __init__(self, port=0, readTimeout=1):
		
		self.hw_lock = multiprocessing.Lock()

		try:
			# Open the serial port to the prologix device
			self.ser = serial.Serial(port=port, baudrate=19200, timeout=readTimeout)
			logging.debug("Prologix serial port opened successfully")
		
		except serial.SerialException:
			
			# Show the error and exit gracefully
			logging.error("Error while opening serial communication with Prologix: " + str(traceback.format_exc()))
			sys.exit(0)
						
		# Set to command mode
		self.write("++mode 1\n")
		
		# Turn off auto-reply
		self.write("++auto 0\n")

		# Set the current GPIB address to "unknown".
		self.cur_addr = multiprocessing.Value('i', -1)
		self.cur_addr_lock = multiprocessing.Lock()
		
		# Clear out any gunk
		self.flush()

		logging.debug("Prologix init complete")

	'''
	Destructor, closes the serial port.
	'''
	def __del__(self):
		
		# Close the serial port
		self.ser.close()

	'''
	Returns a GpibInstrument object.
	
	Arguments:
	   gpibAddr - An integer representing the GPIB bus address of the instrument
	''' 
	def get_device_interface(self, gpibAddr):
		
		# Return a GpibDeviceInterface, which needs to know its own address and the
		# handle to its controller
		return GpibDeviceInterface(gpibAddr, self)

	'''
	Sends a message to the Prologix

	Arguments:
	   msg - A string containing the message to send
	   applyEscape - A bool which, if True, will cause the function to scan the 
				 contents of msg and escape any reserved characters
	'''
	def write(self, msg, applyEscape=False):
		
		# Escape any restricted characters
		if applyEscape:
			# TODO: Implement this
			pass

		# Write to the serial port		
		self.ser.write(msg)

	'''
	Sets the current GPIB bus address that the Pologix is communicating with

	Arguments:
	   gpibAddr - An integer representing the GPIB bus address of the instrument
	'''
	def setGpibAddr(self, gpibAddr):

		with self.cur_addr_lock:
		
			if self.cur_addr.value != gpibAddr:
				# Tell the Prologix to switch addresses
				self.write("++addr %i\n" % int(gpibAddr))
				self.cur_addr.value = gpibAddr


	'''
	Queries the currently selected GPIB bus address for a response and returns it (up to
	the eol char, the max number of bytes, or the timeout)
	
	Arguments:
	   eol - A character indicating the end of the message from the device
	   size - The maximum number of bytes to read, or None for no limit.
	Returns:
	   msg - The response of the device.
	'''
	def read(self, eol='\n', size=None):

		# Ask the controller to send us everything until the EOI, which indicates
		# the end of a transmission
		self.write("++read eoi\n")
		return self.readNext(eol, size)
		
		
	'''
	Doesn't query the currently selected GPIB bus address for a response, but simply returns
	any response already in the buffer (up to the eol char, the max number of bytes, or the timeout)
	
	Arguments:
	   eol - A character indicating the end of the message from the device
	   size - The maximum number of bytes to read, or None for no limit.
	   timeout - The maximum amount of time to allow this function to run
	Returns:
	   msg - The response of the device.
	'''
	def readNext(self, eol='\n', size=None, timeout = 1):

		# TODO: Optimize this function.

		msg = bytearray()

		# Find the ASCII value of the eol char
		eolAscii = ord(eol)
		
		# Read until the given end of line or size
		startTime = time.clock()
		while (True):
			
			# Don't even try if we know there is nothing
			if (self.ser.inWaiting() > 0):

				# Read the next byte
				msg.append(self.ser.read(1))
			
				# See if we are done
				if int(msg[-1]) == eolAscii:
					break
				if (size > 0) and (len(msg) >= size):
					break
				
			# Don't run on forever			
			if (time.clock() > (startTime + timeout)):
				logging.error("Read timed out when attempting to receive data from the GPIB device with address " + str(self.cur_addr.value) + ".  Is the device connected and powered on?")
				if len(msg) > 0:				
					logging.debug("Perhaps EOL should be ASCII " + bytes(msg[-1]))
				break
	
		return msg
	
	'''
	Flush the communication buffer between the computer and the Prologix.
	'''
	def flush(self):	
		self.ser.flush()


'''
A class representing a single GPIB instrument hooked up to some controller.
'''
class GpibDeviceInterface:

	'''
	Contructor - saves the information the instrument needs to know about itself.

	Arguments:
	   gpibAddr - An integer representing the GPIB bus address of the instrument
	   controller - A controller object (such as an instance of the Prologix class)
	'''
	def __init__(self, gpibAddr, controller):

		self.gpibAddr = gpibAddr
		self.controller = controller		

	'''
	Sends a message to the instrument

	Arguments:
	   msg - A string containing the message to send
	   applyEscape - A bool which, if True, will cause the function to scan the 
				 contents of msg and escape any reserved characters
	'''
	def write(self, msg, applyEscape=False):

		with self.controller.hw_lock:
			self._write(msg, applyEscape)
		
	def _write(self, msg, applyEscape=False):

		self.controller.setGpibAddr(self.gpibAddr)
		self.controller.flush() # Clear any gunk out
		self.controller.write(msg, applyEscape)

	'''
	Sends the command to clear the currently selected GPIB bus address.  See the manual
	for each specific instrument to see how it responds to this command.  
	'''
	def clear(self):
		
		with self.controller.hw_lock:
			self._clear()
		
	def _clear(self):
		controller.write("++clr")

	'''
	Queries the instrument for a response and returns it (up to
	the eol char, the max number of bytes, or the timeout)
	
	Arguments:
	   eol - A character indicating the end of the message from the device
	   size - The maximum number of bytes to read, or None for no limit.
	Returns:
	   msg - The response of the device.
	'''
	def read(self, eol='\n', size=None):

		with self.controller.hw_lock:
			return self._read(eol, size)
		
	def _read(self, eol='\n', size=None):

		self.controller.setGpibAddr(self.gpibAddr)
		self.controller.flush() # Clear any gunk out
		return self.controller.read(eol, size)
		
		
	'''
	Doesn't query the instrument for a response, but simply returns
	any response already in the buffer (up to the eol char, the max number of bytes, or the timeout).
	
	This is NOT SAFE in a multithreaded environment, so I have started it with an underscore.
	Use at your own risk.
	
	Arguments:
	   eol - A character indicating the end of the message from the device
	   size - The maximum number of bytes to read, or None for no limit.
	Returns:
	   msg - The response of the device.
	'''
	def _readNext(self, eol='\n', size=None):

		self.controller.setGpibAddr(self.gpibAddr)
		return self.controller.readNext(eol, size)
		

	'''
	Sends a command to the currently selected GPIB bus address and returns the response.
	
	Arguments:
	   cmd - A string containing the message to send
	   applyEscape - A bool which, if True, will cause the function to scan the 
				 contents of msg and escape any reserved characters
	   eol - A character indicating the end of the message from the device
	   size - The maximum number of bytes to read, or None for no limit.
	Returns:
	   msg - The response of the device.
	'''
	def query(self, cmd, eol='\n', size=None, applyEscape=False):

		with self.controller.hw_lock:
			return self._query(cmd, eol, size, applyEscape)
		
	def _query(self, cmd, eol='\n', size=None, applyEscape=False):

		self._write(cmd, applyEscape)	
		return self._read(eol, size)
			
			
	'''
	Flush the controller's communication buffer
	'''
	def flush(self):
		
		with self.controller.hw_lock:
			self._flush()
		
	def _flush(self):
		self.controller.flush()
		
		
		




