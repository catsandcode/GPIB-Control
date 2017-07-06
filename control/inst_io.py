# noinspection PyNonAsciiChar,PyByteLiteral
"""
The io module deals with all connections coming in and out of the computer. It provides decorator functions to enable
higher level programming of instruments in the instruments module. It abstracts between basic IO functions (i.e. dealing
with the serial connection used with the Prologix controller, dealing with the file connection with a USB device) using
the Instrument class, which should be used as the parent class for actual instruments. The Instrument class provides
basic functions-read, write, and query, as well as a few others made used to make programming instruments more
convenient and straight forward.
"""

import multiprocessing
import serial
import sys
import time


def write(func):
    """
    This function is intended to be used as a decorator. It takes a function in a subclass of Instrument that returns a string and wrties to that instrument with the returned string. The function also prints any communication with the instrument to the command line.

    :param func: An instance function of a subclass of Instrument that returns a string
    """

    def write_wrapper(self, *args, **kwargs):
        content = func(self, *args, **kwargs)
        if type(content) is list:
            for command in content:
                print("Writing to " + self.get_name() + " --> " + command)
                self.write(command)
        else:
            command = content
            print("Writing to " + self.get_name() + " --> " + command)
            self.write(command)

    return write_wrapper


def query(func):
    """
    This function is intended to be used as a decorator. It takes a function in a subclass of Instrument that returns a string and queries that instrument with the returned string. The function also prints any communication with the instrument to the command line.

    :param func: An instance function of a subclass of Instrument that returns a string

    :return: The response of the queried command
    """

    def query_wrapper(self, *args, **kwargs):
        command = func(self, *args, **kwargs)
        print("Querying to " + self.get_name() + " --> " + command)
        response = str(self.query(command))
        if type(response) is bytearray: # Check to see if the response is a byte array. If it is, decode to string.
            response = response.decode('utf-8')
        if response.rfind('\n') != -1:
            response = response[:response.rfind('\n')]
        print("Received from " + self.get_name() + " <-- " + response)
        # Try to cast the response as a float and then an int
        if response.rfind(';') != -1:
            response = response[:response.rfind(';')]
        try:
            response = float(response)
            if response.is_integer():
                response = int(response)
        except ValueError:
            pass
        return response

    return query_wrapper


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
            print("Prologix serial port opened successfully")
        except serial.SerialException:
            # Catch error and exit gracefully
            print("Error while opening serial communication with Prologix.")
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
        print("Prologix init complete")

    def __del__(self):
        """
        Destructor, closes the serial port.
        """
        # Close the serial port
        if hasattr(self, 'ser'):
            self.ser.close()

    def open_resource(self, gpibAddr):
        """
        Returns a GpibInstrument object.

        :param gpibAddr: An integer representing the GPIB bus address of the instrument
        """
        # Return a GpibDeviceInterface, which needs to know its own address and a pointer to its controller
        return GPIBDeviceInterface(gpibAddr, self)

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
        NOT SAFE IN MULTIPROCESSING ENVIORNMENTS!!!
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
                print("Read timed out when attempting to receive data from the GPIB device with address " + str(self.cur_addr.value) + ".  Is the device connected and powered on?")
                # If a message has been read, print the last character read and suggest that it might be the end of line character
                if len(msg) > 0:
                    print("Perhaps the end of line character should be ASCII " + msg[-1])
                break
        # Return the read message
        return msg

    def flush(self):
        """
        Flush the communication buffer between the computer and the Prologix.
        """
        self.ser.flush()


class GPIBDeviceInterface(object):
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

    def write(self, msg):
        """
        Sends a message to the instrument

        :param msg: A string containing the message to send
        """
        # Wait until a hardware lock is acquired
        with self.controller.hw_lock:
            self._write(msg)

    def _write(self, msg):
        """
        This function writes a command to the Prologix controller (if there is no '++' prefixed to the command, the command will be passed on to whatever device the Prologix controller is addressed to). It does not wait for a hardware lock.

        :param msg: The message to write
        """
        # Set the gpib address
        self.controller.set_gpib_address(self.gpibAddr)
        # Clear any gunk out
        self.controller.flush()
        # Finally write the message
        self.controller.write(msg)

    def clear(self):
        """
        Sends the command to clear the currently selected GPIB bus address. See the manual for each specific instrument to see how it responds to this command.
        """
        self.controller.write("++clr")

    def read(self, eol='\n', size=None):
        """
        Queries the instrument for a response and returns it (up to the end of line character, the max number of bytes, or the timeout)

        :param eol: A character indicating the end of the message from the device

        :param size: The maximum number of bytes to read, or None for no limit.

        :return: The response of the device.
        """
        # Wait until a hardware lock is acquired
        with self.controller.hw_lock:
            self._read(eol, size)

    def _read(self, eol='\n', size=None):
        """
        Reads from a GPIB device at the current GPIB address. This function does not wait for a hardware lock.

        :param eol: A character indicating the end of the message from the device

        :param size: The maximum number of bytes to read, or None for no limit.

        :return: The response of the device.
        """
        # Set the gpib address
        self.controller.set_gpib_address(self.gpibAddr)
        # Clear any gunk out
        self.controller.flush()
        # Finally read and return
        return self.controller.read(eol, size)

    def readNext(self, eol='\n', size=None):
        """
        NOT SAFE IN MULTIPROCESSING ENVIRONMENTS!!!
        Doesn't query the instrument for a response, but simply returns any response already in the buffer (up to the end of line character, the max number of bytes, or the timeout).

        :param eol: A character indicating the end of the message from the device

        :param size: The maximum number of bytes to read, or None for no limit.

        :return: The response of the device.
        """
        # Set the gpib address
        self.controller.set_gpib_address(self.gpibAddr)
        # Returns read next
        return self.controller.read_next(eol, size)

    def query(self, cmd, eol='\n', size=None):
        """
        Writes a command to the currently selected GPIB bus address and then returns the read response.

        :param cmd: A string containing the message to send

        :param eol: A character indicating the end of the message from the device

        :param size: The maximum number of bytes to read, or None for no limit.

        :return: The response of the device.
        """
        # Wait until a hardware lock is acquired
        with self.controller.hw_lock:
            # Write command
            self._write(cmd)
            # Return what is read
            return self._read(eol, size)

    def flush(self):
        """
        Flush the controller's communication buffer
        """
        # Wait until a hardware lock is acquired
        with self.controller.hw_lock:
            self.controller.flush()


class USBDevice(object):
    """
    This class is used to connect to USB devices using a file object (as you would read or write to a USB drive).
    """

    def __init__(self, address):
        """
        Constructor for the USBDevice class
        :param address: The address of the USB device
        """
        self._address = address
        # Open a device at the specified address, set to read/write mode
        self._device = open(self._address, 'w+')
        if self.query('*IDN?') != '':
            print('Successfully connected to ' + str(address))
        else:
            print('Connection to ' + str(address) + ' failed. Stopping...')
            self._device.close()
            sys.exit(0)

    def read(self):
        """
        Reads from the USB device

        :return: Returns the string that is read from the USB device
        """
        # Read from the device
        return self._device.read()

    def write(self, command):
        """
        Writes a command to the USB device

        :param command: The command to write
        """
        # Write to the device
        self._device.write(command)
        # Flush the connection
        self._device.flush()

    def query(self, command):
        """
        Writes a command from the USB device and then reads the response.

        :param command: The command to write.

        :return: The response.
        """
        # Write to the device
        self._device.write(command)
        # Flush the connection
        self._device.flush()
        # Return what is read and strip any whitespace away
        return self._device.read().strip()

    def close(self):
        """
        Closes the connection with the device.
        """
        # Close the connection
        self._device.close()

    def __del__(self):
        """
        Called on device delete, closes device connection.
        """
        if hasattr(self, '_device'):
            # On delete, close connection
            self.close()


class Instrument(object):
    """
    The instrument class wraps basic instrument functions, providing abstraction between different instrument connection interfaces (i.e. USB, GPIB).
    """

    CONNECTION_TYPE_GPIB = 0
    CONNECTION_TYPE_USB = 1

    def __init__(self, address, connection_type, connection_manager=None):
        """
        Initializes the instrument object.

        :param address: The GPIB address of the instrument.

        :param connection_type: The connection type, either CONNECTION_TYPE_GPIB or CONNECTION_TYPE_USB.

        :param connection_manager: The connection manager to use with the instrument, if one exists.
        """
        self._address = address
        self._name = address
        self._connection_type = connection_type
        self._connection_manager = connection_manager
        self._instrument = None

    def get_name(self):
        """
        Returns the name of the device. The default name is the device address.

        :return: The current name of the device
        """
        return self._name

    def set_name(self, name):
        """
        Sets the name of the device to something readable. The default name is the device address.

        :param name: The name to set the device name to
        """
        self._name = name

    def read(self):
        """
        Reads a string from the instrument.

        :return: The string read from the instrument
        """
        return self._instrument.read()

    def read_raw(self):
        """
        Reads raw values from the instrument.

        :return: The raw data read from the instrument
        """
        return self._instrument.read()

    def write(self, command):
        """
        Writes a string to the instrument.

        :return: The number of bytes written
        """
        return self._instrument.write(command + '\n')

    def query(self, command):
        """
        Queries a string from the instrument.

        :param command: The command to use to query the instrument

        :return: The string read from the instrument
        """
        return self._instrument.query(command + '\n')

    def open(self):
        """
        Opens a connection to the instrument at the specified address.

        :return: True if connection successful, False otherwise.
        """
        if self._instrument is None:
            if self._connection_type == self.CONNECTION_TYPE_GPIB:
                self._instrument = self._connection_manager.open_resource(self._address)
            elif self._connection_type == self.CONNECTION_TYPE_USB:
                self._instrument = USBDevice(self._address)
            if self._instrument is None:
                return False
        return True

    def close(self):
        """
        Closes a connection to the instrument at the specified address.
        """
        if self._connection_type == self.CONNECTION_TYPE_USB:
            self._instrument.close()

    def reset(self):
        """
        Resets the instrument.
        """
        self.write('*RST')

    def initialize_instrument(self):
        """
        Issues any commands that need to be issued before control of the instrument begins.
        """
        pass
