import visa
import numpy as np
from instruments import HP8350B, SR830, Agilent33220A
from instrument_manager import Instrument

sweeper = None
lock_in = None
func_gen = None


def get_sweep_range():
    """
    Gets the sweep range as a tuple (start, stop), where units are in GHz. This will automatically multiply the ranges
    by a factor of 18 (as the source is attached to a x18 frequency multiplier).
    """
    return sweeper.get_freq_start() * 18.0, sweeper.get_freq_stop() * 18.0


def set_sweep_range(start=200, stop=300):
    """
    Sets the sweep range as a tuple (start, stop), where units are in GHz. This will automatically divide the ranges by
    a factor of 18 (as the source is attached to a x18 frequency multiplier).
    """
    sweeper.start_stop_sweep(start / 18.0, HP8350B.UNIT_GHZ, stop / 18.0, HP8350B.UNIT_GHZ)


def get_sweep_time():
    """
    Gets the sweep time in seconds.
    """
    return sweeper.get_sweep_time()


def set_sweep_time(time=5):
    """
    Sets the sweep time in seconds.
    :param time: The sweep time in seconds
    """
    sweeper.set_sweep_time(time, HP8350B.UNIT_SECOND)


def get_chopper_frequency():
    """
    Gets the chopper frequency in kHz.
    :return: The chopper frequency in kHz
    """
    return func_gen.get_wave_frequency() / 1000.0


def set_chopper_frequency(freq=10):
    """
    Sets the chopper frequency in kHz.
    :param freq: The frequency in kHz
    """
    func_gen.set_wave_frequency(freq * 1000.0)

def get_chopper_amplitude():
    """
    Returns the chopper amplitude in volts.
    """
    return func_gen.get_wave_amplitude()

def set_chopper_amplitude(amplitude=0.5):
    """
    Sets the chopper amplitude in volts.
    :param amplitude: The amplitude in volts
    """
    func_gen.set_wave_amplitude(amplitude)


def get_chopper_sweep_on():
    """
    Gets the chopper sweep state, True if on, False if off.
    :return: The chopper sweep state
    """
    if func_gen.get_sweep_state == Agilent33220A.STATE_ON:
        return True
    else:
        return False


def set_chopper_sweep_on(turn_on=False):
    """
    Sets the chopper sweep on if turn_on is True.
    :param turn_on: Turns on if True
    """
    if turn_on:
        func_gen.set_sweep_state(Agilent33220A.STATE_ON)
    else:
        func_gen.set_sweep_state(Agilent33220A.STATE_OFF)


def set_chopper_sweep(start=10, stop=1000, time=20, logarithmic=False):
    """
    Sets the chopper sweep parameters.
    :param start: The start frequency in kHz
    :param stop: The stop frequency in kHz
    :param time: The sweep time in seconds
    :param logarithmic: True if a logarithmic sweep should be used, False otherwise
    """
    func_gen.set_sweep_start(start * 1000.0)
    func_gen.set_sweep_stop(stop * 1000.0)
    func_gen.set_sweep_time(time)
    if logarithmic:
        func_gen.set_sweep_spacing(Agilent33220A.SWEEP_SPACING_LOGARITHMIC)
    else:
        func_gen.set_sweep_spacing(Agilent33220A.SWEEP_SPACING_LINEAR)


def get_power():
    """
    Gets the power level of the sweeper in dBm.
    """
    return sweeper.get_power_level()


def set_power(power_level=0):
    """
    Sets the power level in dBm.
    :param power_level: The power level in dBm
    """
    sweeper.set_power_level(power_level)


def set_sweep_trigger(mode='internal'):
    """
    Sets the sweep trigger using either 'internal', 'external',  or 'single'
    :param mode: Either 'internal' (sweeps are continuously triggered by the sweeper's internal clock), 'external'
    (sweeps are triggered by an external trigger), or 'single' (sweeps are triggered by the trigger_sweep() function).
    """
    if mode == 'internal':
        sweeper.set_trigger_mode_internal()
    if mode == 'external':
        sweeper.set_trigger_mode_external()
    elif mode == 'single':
        sweeper.set_trigger_mode_single()


def start_sweep():
    """
    Triggers a single sweep. This will also send a trigger to the lock-in amplifier.
    """
    sweeper.single_trigger()


def start_chopper_sweep():
    """
    Starts the chopper sweep.
    """
    func_gen.send_trigger()


_SENSITIVITY_DICT = {0: 0.000002,
                     1: 0.000005,
                     2: 0.00001,
                     3: 0.00002,
                     4: 0.00005,
                     5: 0.0001,
                     6: 0.0002,
                     7: 0.0005,
                     8: 0.001,
                     9: 0.002,
                     10: 0.005,
                     11: 0.01,
                     12: 0.02,
                     13: 0.05,
                     14: 0.1,
                     15: 0.2,
                     16: 0.5,
                     17: 1.0,
                     18: 2.0,
                     19: 5.0,
                     20: 10.0,
                     21: 20.0,
                     22: 50.0,
                     23: 100.0,
                     24: 200.0,
                     25: 500.0,
                     26: 1000.0}


def get_sensitivity():
    """
    Returns the current sensitivity of the lock-in in mV.
    :return: The sensitivity in mV
    """
    return _SENSITIVITY_DICT.get(lock_in.get_sensitivity())


def set_sensitivity(sensitivity=1000.0):
    """
    Sets the sensitivity of the lock-in in mV. The lock-in has a set of allowed sensitivities. This method will choose
    the first allowed sensitivity that is larger than the one entered.
    :param sensitivity: The preferred sensitivity in mV
    :return: The chosen sensitivity
    """
    sens_key = 26
    for key, value in _SENSITIVITY_DICT.iteritems():
        if sensitivity <= value:
            sens_key = key
            break
    lock_in.set_sensitivity(sens_key)
    return _SENSITIVITY_DICT.get(sens_key)


_TIME_CONSTANT_DICT = {0: 0.01,
                       1: 0.03,
                       2: 0.1,
                       3: 0.3,
                       4: 1,
                       5: 3,
                       6: 10,
                       7: 30,
                       8: 100,
                       9: 300,
                       10: 1 * (10 ** 3),
                       11: 3 * (10 ** 3),
                       12: 10 * (10 ** 3),
                       13: 30 * (10 ** 3),
                       14: 100 * (10 ** 3),
                       15: 300 * (10 ** 3),
                       16: 1 * (10 ** 6),
                       17: 3 * (10 ** 6),
                       18: 10 * (10 ** 6),
                       19: 30 * (10 ** 6)}


def get_time_constant():
    """
    Returns the current time constant of the lock-in in ms.
    :return: The sensitivity in ms
    """
    return _TIME_CONSTANT_DICT.get(lock_in.get_time_constant())


def set_time_constant(time_constant=1000):
    """
    Sets the time constant of the lock-in in ms. The lock-in has a set of allowed time constants. This method will
    choose the first allowed time constant that is larger than the one entered.
    :param time_constant: The preferred time constant in ms
    :return: The chosen time constant
    """
    time_const_key = 19
    for key, value in _TIME_CONSTANT_DICT.iteritems():
        if time_constant <= value:
            time_const_key = key
            break
    lock_in.set_time_constant(time_const_key)
    return _TIME_CONSTANT_DICT.get(time_const_key)


_SAMPLE_RATE_DICT = {0: 0.0625,
                     1: 0.125,
                     2: 0.25,
                     3: 0.5,
                     4: 1,
                     5: 2,
                     6: 4,
                     7: 8,
                     8: 16,
                     9: 32,
                     10: 64,
                     11: 128,
                     12: 256,
                     13: 512}


def get_sample_rate():
    """
    Returns the current sample rate of the lock-in in Hz.
    :return: The sample rate in Hz
    """
    return _SAMPLE_RATE_DICT.get(lock_in.get_sample_rate())


def set_sample_rate(sample_rate=512):
    """
    Sets the sample rate of the lock-in in Hz. The lock-in has a set of allowed sample rates. This method will choose
    the first allowed sample rate constant that is larger than the one entered.
    :param sample_rate: The preferred sample rate in Hz
    :return: The chosen time constant
    """
    sample_rate_key = 13
    for key, value in _TIME_CONSTANT_DICT.iteritems():
        if sample_rate <= value:
            sample_rate_key = key
            break
    lock_in.set_sample_rate(sample_rate_key)
    return _SAMPLE_RATE_DICT.get(sample_rate_key)


def get_time_to_fill():
    """
    Returns the time needed to fill storage in seconds.
    :return: The time needed to fill storage in seconds
    """
    return lock_in.get_storage_time()


def start_scan():
    """
    Starts data collection. Returns the time needed to fill storage in seconds.
    :return: The time needed to fill storage in seconds
    """
    lock_in.reset_scan()
    storage_time = lock_in.get_storage_time()
    lock_in.start_scan()
    return storage_time


def stop_scan():
    """
    Stops the current scan.
    """
    lock_in.pause_scan()


def get_data():
    """
    Gets the recorded data as a numpy array.
    :return: A numpy array object with frequency in the first column and R in the second column
    """
    length = lock_in.get_scanned_data_length()
    r_data = lock_in.get_channel1_scanned_data(0, length)
    raw_sweep_data = lock_in.get_channel2_scanned_data(0, length)
    sweep_data = _convert_raw_sweep_data_to_frequency(raw_sweep_data)
    return np.array([sweep_data, r_data]).transpose()


def _convert_raw_sweep_data_to_frequency(raw_data):
    """
    Converts DC voltage data (where the voltage is proportional to the current frequency of the sweep oscillator) to
    frequency data in Hz.
    :param raw_data: A list of 'raw' data, in other words a list of DC voltages
    :return: A list of frequency data
    """
    frequency_data = []
    for raw_data_point in raw_data:
        # For each data point multiply by 1/10 * 20.40GHz (i.e. 20.40 * 10^9)
        frequency_data.append(float(raw_data_point) * (1.0 / 10.0) * (20.40 * (10 ** 9)))
    return frequency_data


def initialize():
    """
    Initializes the instruments and prepares the relevant settings.
    """
    # Create a ResourceManager to deal with all of the instruments being used.
    rm = visa.ResourceManager()
    # Use global variables
    global sweeper
    global lock_in
    global func_gen
    # Instantiate each instrument
    sweeper = HP8350B(rm, 'GPIB0::19::INSTR')
    lock_in = SR830(rm, 'GPIB0::8::INSTR')
    func_gen = Agilent33220A(rm, 'GPIB0::10::INSTR')
    # Open each instrument
    sweeper.open()
    lock_in.open()
    func_gen.open()
    # Initialize the sweeper and set the trigger mode to internal
    sweeper.initialize_instrument()
    sweeper.set_trigger_mode_internal()
    # Initialize the lock-in, reset, set the reference source and trigger, set what happens when the data buffer is full, and set the display and data recording settings.
    lock_in.initialize_instrument()
    lock_in.reset()
    lock_in.set_reference_source(SR830.REFERENCE_SOURCE_EXTERNAL)
    lock_in.get_reference_trigger_mode(SR830.REFERENCE_TRIGGER_MODE_TTL_RISING_EDGE)
    lock_in.set_trigger_mode(SR830.TRIGGER_START_MODE_OFF)
    lock_in.set_end_of_buffer_mode(SR830.END_OF_BUFFER_SHOT)
    lock_in.set_channel1_display(SR830.DISPLAY_CHANNEL1_X)
    lock_in.set_channel2_display(SR830.DISPLAY_CHANNEL2_Y)
    # Initialize the function generator and set the trigger source to software
    func_gen.set_wave_type(Agilent33220A.WAVE_TYPE_SQUARE)
    func_gen.set_trigger_source(Agilent33220A.SWEEP_TRIGGER_SOFTWARE)

def sweep_command_line():
    _command_line('GPIB0::19::INSTR')


def lock_in_command_line():
    _command_line('GPIB0::8::INSTR')


def func_gen_command_line():
    _command_line('GPIB0::10::INSTR')


def _command_line(address):
    rm = visa.ResourceManager()
    inst = Instrument(rm, address)
    inst.open()
    while (True):
        user_input = raw_input(
            "Type 'EXIT' to stop, 'QUERY [command]' to query, 'WRITE [command]' to write, and 'READ' to read.\n(Note the prompt is not case sensitive.)\n")
        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'read':
            try:
                print inst.read()
            except visa.VisaIOError:
                print 'Timeout, returning to command prompt...'
        elif user_input.rfind(' ') != -1 and user_input.lower()[0:user_input.find(' ')] == 'query':
            try:
                print inst.query(user_input[user_input.find(' ') + 1:])
            except visa.VisaIOError:
                print 'Timeout, returning to command prompt...'
        elif user_input.rfind(' ') != -1 and user_input.lower()[0:user_input.find(' ')] == 'write':
            print inst.write(user_input[user_input.find(' ') + 1:])
        else:
            print "Please use one of the commands specified"
    inst.close()
