import abc
from gpib import Prologix, GpibDeviceInterface

CONNECTION_TYPE_GPIB = 0
CONNECTION_TYPE_USB = 1


def write(func):
    """
    This function is intended to be used as a decorator. It takes a function in a subclass of Instrument that returns a string and wrties to that instrument with the returned string. The function also prints any communication with the instrument to the command line.
    :param func: An instance function of a subclass of Instrument that returns a string
    """

    def write_wrapper(self, *args, **kwargs):
        content = func(self, *args, **kwargs)
        if type(content) is list:
            for command in content:
                print "Writing to " + self.get_name() + " --> " + command
                self.write(command)
        else:
            command = content
            print "Writing to " + self.get_name() + " --> " + command
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
        print "Querying to " + self.get_name() + " --> " + command
        response = str(self.query(command))
        if response.rfind('\n') != -1:
            response = response[:response.rfind('\n')]
        print "Received from " + self.get_name() + " <-- " + response
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

class USBManager(object):

    def __init__(self):
        pass

    def open_resource(self, address):
        return USBDevice(address)

class USBDevice(object):

    def __init__(self, address):
        self._address = address
        self._device = open(self._address, 'w+')

    def read(self):
        return self._device.read()

    def write(self, command):
        self._device.write(command)
        self._device.flush()

    def query(self, command):
        self._device.write(command)
        self._device.flush()
        return self._device.read().strip()

class Instrument(object):

    def __init__(self, connection_manager, address):
        """
        Initializes the instrument object.
        :param connection_manager: The resource manager to use with the instrument.
        :param address: The GPIB address of the instrument.
        """
        self._connection_manager = connection_manager
        self._address = address
        self._name = address
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
            print self._address
            self._instrument = self._connection_manager.open_resource(self._address)
            if self._instrument is None:
                return False
        return True

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
