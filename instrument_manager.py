import abc, visa

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


class Instrument(object):

    def __init__(self, resource_manager, address):
        """
        Initializes the instrument object.
        :param resource_manager: The resource manager to use with the instrument.
        :param address: The GPIB address of the instrument.
        """
        self._resource_manager = resource_manager
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
        return self._instrument.read_raw()

    def write(self, command):
        """
        Writes a string to the instrument.
        :return: The number of bytes written
        """
        return self._instrument.write(command)

    def query(self, command):
        """
        Queries a string from the instrument.
        :param command: The command to use to query the instrument
        :return: The string read from the instrument
        """
        return self._instrument.query(command)

    def open(self):
        """
        Opens a connection to the instrument at the specified address.
        :return: True if connection successful, False otherwise.
        """
        if self._instrument is None:
            self._instrument = self._resource_manager.open_resource(self._address)
            if self._instrument is None:
                return False
        return True

    def close(self):
        """
        Closes the connection to the instrument at the specified address.
        """
        if self._instrument is not None:
            self._instrument.close()
            self._instrument = None

    def reset(self):
        """
        Resets the instrument.
        """
        self.write('*RST')

    def get_timeout(self):
        """
        Returns the timeout of the query and read functions in milliseconds. A timeout of 0 corresponds to an infinite
        timeout.
        """
        return self._instrument.timeout

    def set_timeout(self, timeout=3000):
        """
        Sets the timeout of the query and read functions in milliseconds. Defaults to 3000ms. To set an infinite timeout
        pass the parameter timeout=0.
        :param timeout: The timeout
        """
        self._instrument.timeout = timeout

    def initialize_instrument(self):
        """
        Issues any commands that need to be issued before control of the instrument begins.
        """
        pass
