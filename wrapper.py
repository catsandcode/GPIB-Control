import numpy as np
from instruments import SR830, Agilent33220A, PasternackPE11S390
from instrument_manager import Instrument, USBManager
from gpib import Prologix

gpib_manager = None
freq_synth = None
lock_in = None
func_gen = None

freq_multiple = None


def get_freq_synth_enable():
    """
    Returns true if the frequency sythesizer is enabled, false otherwise.
    """
    if freq_synth.get_output_state() == PasternackPE11S390.OUTPUT_STATE_ON:
        return True
    return False


def set_freq_synth_enable(enable=False):
    """
    Turns the frequency synthesizer output on or off.
    :param enable: True if the frequency synthesizer should be on, false if off.
    """
    if enable:
        freq_synth.set_output_state(PasternackPE11S390.OUTPUT_STATE_ON)
    else:
        freq_synth.set_output_state(PasternackPE11S390.OUTPUT_STATE_OFF)


def get_freq_synth_freq():
    """
    Returns the frequency in GHz.
    """
    return freq_synth.get_frequency() * freq_multiple


def set_freq_synth_frequency(freq=200):
    """
    Sets the frequency synthesizer to continuous wave mode at the specified frequency where units are in GHz. This will
    automatically divide the ranges by freq_multiple (as the source is attached to a set of frequency multipliers).
    """
    freq_synth.set_frequency(freq / freq_multiple)
    
def get_freq_multiplier():
    """
    Returns the frequency multiplier, which can be changed depending on the experimental setup.
    """
    return freq_multiple
    
def set_freq_multiplier(multiple = 18):
    """
    Sets the frequency multiplier, which should be equal to the product of the frequency multipliers present in the experimental setup.
    """
    global freq_multiple
    freq_multiple = multiple


def get_freq_synth_power():
    """
    Gets the power level of the frequency synthesizer in dBm.
    """
    return freq_synth.get_power()


def set_freq_synth_power(power_level=0.0):
    """
    Sets the power level of the frequency synthesizer in dBm.
    :param power_level: The power level in dBm
    """
    freq_synth.set_power(power_level)



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


def set_chopper_on(turn_on=False):
    """
    Sets the chopper output on if turn_on is True.
    :param turn_on: Turns on if True
    """
    if turn_on:
        func_gen.set_output_state(Agilent33220A.STATE_ON)
    else:
        func_gen.set_output_state(Agilent33220A.STATE_OFF)


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

_LOW_PASS_SLOPE = {SR830.LOW_PASS_FILTER_SLOPE_6dB_PER_OCT: 6,
                   SR830.LOW_PASS_FILTER_SLOPE_12dB_PER_OCT: 12,
                   SR830.LOW_PASS_FILTER_SLOPE_18dB_PER_OCT: 18,
                   SR830.LOW_PASS_FILTER_SLOPE_24dB_PER_OCT: 24}


def get_low_pass_slope():
    """
    Returns the current low pass filter slope of the lock-in in dB per octave.
    :return: The slope in dB per octave
    """
    return _LOW_PASS_SLOPE.get(lock_in.get_low_pass_filter_slope())


def set_low_pass_slope(slope=18):
    """
    Sets the low pass filter slope of the lock-in in dB per octave. The lock-in has a set of allowed slopes. This method
    will choose the first allowed slope that is smaller than the one entered. If no allowed slope is smaller, 6dB per
    octave will be selected.
    :param slope: The preferred slope in dB per octave
    :return: The chosen slope in dB per octave
    """
    slope_key = SR830.LOW_PASS_FILTER_SLOPE_6dB_PER_OCT
    for key, value in _LOW_PASS_SLOPE.iteritems():
        if slope >= value:
            slope_key = key
        else:
            break
    lock_in.set_low_pass_filter_slope(slope_key)
    return _LOW_PASS_SLOPE.get(slope_key)


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
    for key, value in _SAMPLE_RATE_DICT.iteritems():
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

def snap_data():
    """
    Gets the current value in the X and Y readouts on the lock-in amplifier
    :return: A tuple of the form (x, y)
    """
    data_dict = lock_in.snap_values(['X', 'Y'])
    x = data_dict.get('X')
    y = data_dict.get('Y')
    return (x, y)

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
    channel1_data = lock_in.get_channel1_scanned_data(0, length)
    channel2_data = lock_in.get_channel2_scanned_data(0, length)
    return np.array([channel1_data, channel2_data])


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


def set_data(col1='X', col2='Y'):
    """
    Sets the data to record in columns 1 and 2.
    :param col1: Either 'X', 'R', 'X noise', 'Aux1', or 'Aux2'
    :param col2: Either 'Y', 'Theta', 'Y noise', 'Aux3', or 'Aux4'
    """
    # Set column 1
    if col1 == 'X':
        lock_in.set_channel1_display(SR830.DISPLAY_CHANNEL1_X)
    elif col1 == 'R':
        lock_in.set_channel1_display(SR830.DISPLAY_CHANNEL1_R)
    elif col1 == 'X noise':
        lock_in.set_channel1_display(SR830.DISPLAY_CHANNEL1_X_NOISE)
    elif col1 == 'Aux1':
        lock_in.set_channel1_display(SR830.DISPLAY_CHANNEL1_AUX1)
    elif col1 == 'Aux2':
        lock_in.set_channel1_display(SR830.DISPLAY_CHANNEL1_AUX2)
    # Set column 2
    if col2 == 'Y':
        lock_in.set_channel2_display(SR830.DISPLAY_CHANNEL2_Y)
    elif col2 == 'Theta':
        lock_in.set_channel2_display(SR830.DISPLAY_CHANNEL2_THETA)
    elif col2 == 'Y noise':
        lock_in.set_channel2_display(SR830.DISPLAY_CHANNEL2_Y_NOISE)
    elif col2 == 'Aux3':
        lock_in.set_channel2_display(SR830.DISPLAY_CHANNEL2_AUX3)
    elif col2 == 'Aux4':
        lock_in.set_channel2_display(SR830.DISPLAY_CHANNEL2_AUX4)


def initialize():
    """
    Initializes the instruments and prepares the relevant settings.
    """
    # Use global variables
    global freq_synth
    global lock_in
    global func_gen
    global gpib_manager
    # Create new ConnectionManagers to deal with all of the instruments being used.
    gpib_manager = Prologix('/dev/ttyUSB0')
    usb_manager = USBManager()
    # Instantiate each instrument
    freq_synth = PasternackPE11S390(usb_manager, '/dev/usbtmc0')
    lock_in = SR830(gpib_manager, 8)
    func_gen = Agilent33220A(gpib_manager, 10)
    # Name each instrument
    freq_synth.set_name('Frequency Synthesizer')
    lock_in.set_name('Lock-In')
    func_gen.set_name('Function Generator')
    # Open each instrument
    freq_synth.open()
    lock_in.open()
    func_gen.open()
    # Initialize the frequency synthesizer
    freq_synth.initialize_instrument()
    # Initialize the lock-in, reset, set the reference source and trigger, set what happens when the data buffer is full, and set the display and data recording settings.
    lock_in.initialize_instrument()
    lock_in.reset()
    lock_in.set_input_shield_grounding(SR830.INPUT_SHIELD_GROUNDING_GROUND)
    lock_in.set_input_coupling(SR830.INPUT_COUPLING_AC)
    lock_in.set_input_configuration(SR830.INPUT_CONFIGURATION_A)
    lock_in.set_input_notch_line_filter(SR830.INPUT_NOTCH_OUT_OR_NO)
    lock_in.set_reserve_mode(SR830.RESERVE_MODE_LOW_NOISE)
    lock_in.set_reference_source(SR830.REFERENCE_SOURCE_EXTERNAL)
    lock_in.set_reference_trigger_mode(SR830.REFERENCE_TRIGGER_MODE_TTL_RISING_EDGE)
    lock_in.set_trigger_mode(SR830.TRIGGER_START_MODE_OFF)
    lock_in.set_end_of_buffer_mode(SR830.END_OF_BUFFER_SHOT)
    lock_in.set_channel1_output(SR830.CHANNEL1_OUTPUT_DISPLAY)
    lock_in.set_channel2_output(SR830.CHANNEL2_OUTPUT_DISPLAY)
    # Initialize the function generator and set the trigger source to software
    func_gen.set_wave_type(Agilent33220A.WAVE_TYPE_SQUARE)
    func_gen.set_output_state(Agilent33220A.STATE_OFF)
    func_gen.set_sweep_state(Agilent33220A.STATE_OFF)
    # Set freq_multiple to 18, as is standard with this experiment
    freq_multiple = 18.0


def close():
    freq_synth.close()
    lock_in.close()
    func_gen.close()


def lock_in_command_line():
    _command_line('GPIB0::8::INSTR')


def func_gen_command_line():
    _command_line('GPIB0::10::INSTR')


def frequency_synthesizer_command_line():
    _command_line('USB0::0x2012::0x0011::5001::INSTR')


def _command_line(address, connection_manager):
    inst = Instrument(connection_manager, address)
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
