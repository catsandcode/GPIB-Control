import serial
import sys
import traceback
import time
import logging
import multiprocessing


# noinspection SpellCheckingInspection
class Prologix(object):
    """
    A class which handles communication with a Prologix GPIB-USB module. This class is safe to use with multiprocessing,
    although it does not use multiprocessing itself (rather it is safe to use with multiprocessing implementations).
    Note that commands sent to the Prologix are terminated with a new line character ('\n'). This must be appended to
    commands sent by the user.
    """

    def __init__(self, port=0, read_timeout=1):
        """
        Initializes serial communication with the GPIB-USB module.
        :param port: A string containing the name of the com port.  Defaults to the integer 0, which refers to the first available serial port.
        :param read_timeout: The number of seconds to wait before giving up while reading.
        """
        # Create a hardware lock, used to ensure multiple GpibDeviceInterface objects don't try to access their Prologix controller at once
        self.hw_lock = multiprocessing.Lock()
        # Attempt to open a serial connection to the device
        try:
            self.ser = serial.Serial(port=port, baudrate=19200, timeout=read_timeout)
            print "Prologix serial port opened successfully"
        except serial.SerialException:
            # Catch error and exit gracefully
            print "Error while opening serial communication with Prologix."
            sys.exit(0)
        # Set to Prologix to controller mode
        self.write("++mode 1\n")
        # Set the Prologix to tell GPIB devices to go to listen mode after a command is sent
        self.write("++auto 0\n")
        # Set the current GPIB address to "unknown". Save in multiprocessing shared memory.
        self.cur_addr = multiprocessing.Value('i', -1)
        # Create a current address lock, used to make sure that multiple GpibDeviceInterface objects don't try to change the Prologix's device address at once
        self.cur_addr_lock = multiprocessing.Lock()
        # Clear out any gunk from the serial conneciton
        self.flush()
        # Notify user of successful initialization
        print "Prologix init complete"

    def __del__(self):
        """
        Destructor, closes the serial port.
        """
        # Close the serial port
        self.ser.close()

    def open_resource(self, gpibAddr):
        """
        Returns a GpibInstrument object.
        :param gpibAddr: An integer representing the GPIB bus address of the instrument
        """
        # Return a GpibDeviceInterface, which needs to know its own address and a pointer to its controller
        return GpibDeviceInterface(gpibAddr, self)

    def write(self, msg):
        """
        Sends a message to the Prologix
        :param msg: A string containing the message to send
        """
        # Write to the serial port
        self.ser.write(msg)

    def set_gpib_address(self, gpib_address):
        """
        Sets the current GPIB bus address that the Pologix is communicating with
        :param gpib_address: An integer representing the GPIB bus address of the instrument
        """
        # Wait until the current process has a lock to ensure that no other processes try to change the current address while the current process is setting it
        with self.cur_addr_lock:
            # Only change the current address if it is not equal to the address to set to
            if self.cur_addr.value != gpib_address:
                # Write the new address to the Prologix
                self.write("++addr %i\n" % int(gpib_address))
                # Update the current address value
                self.cur_addr.value = gpib_address

    def read(self, eol='\n', size=None):
        """
        Queries the currently selected GPIB bus address for a response and returns it (up to the eol char, the max number of bytes, or the timeout)
        :param eol: A character indicating the end of the message from the device
        :param size: The maximum number of bytes to read, or None for no limit.
        :return: The response of the device.
        """
        # Ask the controller to send us everything until the EOI,
        self.write("++read eoi\n")
        # Return what is read up until the end of line.
        return self.read_next(eol, size)

    def read_next(self, eol='\n', size=None, timeout=1):
        """
        Doesn't query the currently selected GPIB bus address for a response, but simply returns any response already in the buffer (up to the eol char, the max number of bytes, or the timeout)
        :param eol: A character indicating the end of the message from the device
        :param size: The maximum number of bytes to read, or None for no limit.
        :param timeout: The maximum amount of time to allow this function to run
        :return: The response of the device.
        """
        # Create a bytearray to read data into
        msg = bytearray()
        # Find the ASCII value of the end of line character
        eolAscii = ord(eol)
        # Get the current time, will be used to detect if operation has timed out
        startTime = time.clock()
        while True:
            # If nothing is waiting in the serial buffer, break
            if self.ser.inWaiting() > 0:
                # Read the next byte into the msg bytearray
                msg.append(self.ser.read(1))
                # See if the last byte in the msg bytearray (i.e. the byte read on the previous line) is the end of line character. If so, break.
                if int(msg[-1]) == eolAscii:
                    break
                # If read_next was called with a size constraint and the msg bytearray is larger than that size, break.
                if (size > 0) and (len(msg) >= size):
                    break
            # Check for timeout. If timeout, break.
            if time.clock() > (startTime + timeout):
                print "Read timed out when attempting to receive data from the GPIB device with address " + str(self.cur_addr.value) + ".  Is the device connected and powered on?"
                # If a message has been read, print the last character read and suggest that it might be the end of line character
                if len(msg) > 0:
                    logging.debug("Perhaps the end of line character should be ASCII " + bytes(msg[-1]))
                break
        # Return the read message
        return msg

    def flush(self):
        """
        Flush the communication buffer between the computer and the Prologix.
        """
        self.ser.flush()


class GpibDeviceInterface(object):
    """
    A class representing a single GPIB instrument hooked up to some controller.
    """

    def __init__(self, gpibAddr, controller):
        """
        Saves the information the instrument needs to know about itself.
        :param gpibAddr: An integer representing the GPIB bus address of the instrument
        :param controller: A controller object (such as an instance of the Prologix class)
        """
        self.gpibAddr = gpibAddr
        self.controller = controller

    '''
	

	Arguments:
	   msg - 
	   applyEscape - 
	'''

    def write(self, msg, applyEscape=False):
        """
        Sends a message to the instrument
        :param msg: A string containing the message to send
        :param applyEscape: A bool which, if True, will cause the function to scan the contents of msg and escape any reserved characters
        """
        # Wait until a hardware lock is aquired
        with self.controller.hw_lock:
            self.controller.set_gpib_address(self.gpibAddr)
            self.controller.flush()  # Clear any gunk out
            self.controller.write(msg)


    '''
	Sends the command to clear the currently selected GPIB bus address.  See the manual
	for each specific instrument to see how it responds to this command.  
	'''

    def clear(self):
        with self.controller.hw_lock:
            self._clear()

    def _clear(self):
        self.controller.write("++clr")

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
        self.controller.set_gpib_address(self.gpibAddr)
        self.controller.flush()  # Clear any gunk out
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
        self.controller.set_gpib_address(self.gpibAddr)
        return self.controller.read_next(eol, size)

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
        self._write(cmd)
        return self._read(eol, size)

    '''
	Flush the controller's communication buffer
	'''

    def flush(self):
        with self.controller.hw_lock:
            self._flush()

    def _flush(self):
        self.controller.flush()
