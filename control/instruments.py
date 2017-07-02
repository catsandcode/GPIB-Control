from control.inst_io import Instrument, write, query


class HP8350B(Instrument):
    # noinspection SpellCheckingInspection
    """
    The HP8350B class is used to control an HP8350B Sweep Oscillator via GPIB (now owned by Keysight).
    """

    UNIT_GHZ = 'GZ'
    UNIT_MHZ = 'MZ'
    UNIT_KHZ = 'KZ'
    UNIT_HZ = 'HZ'

    UNIT_SECOND = 'SC'
    UNIT_MILLISECOND = 'MS'

    @write
    def start_stop_sweep(self, freq_start=11, unit_start=UNIT_GHZ, freq_stop=13, unit_stop=UNIT_GHZ):
        """
        Starts a sweep from freq_start to freq_stop.
        :param freq_start: The frequency to start sweeping from
        :param unit_start: The unit of the start frequency, either UNIT_GHZ, UNIT_MHZ, UNIT_KHZ, or UNIT_HZ
        :param freq_stop: The frequency to stop sweeping at
        :param unit_stop: The unit of the stop frequency, either UNIT_GHZ, UNIT_MHZ, UNIT_KHZ, or UNIT_HZ
        """
        return ['FA ' + str(freq_start) + unit_start, 'FB ' + str(freq_stop) + unit_stop]

    @query
    def get_freq_start(self):
        """
        Returns frequency start in Hz.
        """
        return 'OP FA'

    @query
    def get_freq_stop(self):
        """
        Returns the frequency stop in Hz.
        """
        return 'OP FB'

    @query
    def get_freq_center(self):
        """
        Returns the frequency center in Hz.
        """
        return 'OP CF'

    @query
    def get_freq_width(self):
        """
        Returns the frequency width in Hz.
        """
        return 'OP DF'

    @query
    def get_continuous_wave_frequency(self):
        """
        Returns the continuous wave frequency in Hz.
        """
        return 'OP CW'

    @write
    def center_sweep(self, freq_center=12, unit_center=UNIT_GHZ, freq_width=500, unit_width=UNIT_MHZ):
        """
        Starts a sweep of width freq_width around freq_center.
        :param freq_center: The center frequency
        :param unit_center: The unit of the center frequency, either UNIT_GHZ, UNIT_MHZ, UNIT_KHZ, or UNIT_HZ
        :param freq_width: The width to sweep
        :param unit_width: The unit of the width frequency, either UNIT_GHZ, UNIT_MHZ, UNIT_KHZ, or UNIT_HZ
        """
        return ['CF ' + str(freq_center) + unit_center, 'DF ' + str(freq_width) + unit_width]

    @write
    def continuous_wave_sweep(self, freq=12, unit=UNIT_GHZ):
        """
        Outputs at a constant frequency, freq
        :param freq: The frequency to output
        :param unit: The unit of the output frequency, either UNIT_GHZ, UNIT_MHZ, UNIT_KHZ, or UNIT_HZ
        """
        return 'CW ' + str(freq) + unit

    @write
    def set_sweep_time(self, time=0.01, unit=UNIT_SECOND):
        """
        Sets the amount of time to complete each sweep in.
        :param time: The time
        :param unit: The unit of the time
        """
        return 'ST ' + str(time) + unit

    @query
    def get_sweep_time(self):
        """
        Gets the sweep time in seconds.
        """
        return 'OP ST'

    @write
    def set_power_level(self, power=5):
        """
        Sets the power of the output in dBm.
        :param power: The power in dBm
        """
        return 'PL ' + str(power)

    @write
    def set_trigger_mode_internal(self):
        """
        Sets the trigger mode to internal. That is, sweeps are triggered by the sweep oscillator's internal clock.
        :return:
        """
        return 'T1'

    @write
    def set_trigger_mode_external(self):
        """
        Sets the trigger mode to external. That is, sweeps are triggered by an external trigger.
        :return:
        """
        return 'T3'

    @write
    def set_trigger_mode_single(self):
        """
        Sets the trigger mode to single. That is, sweeps are triggered by the T4 command. Note that in order to set the
        sweeper to single mode the command T4 must be sent. In order to avoid triggering a previously set trigger mode,
        the command T1 is first sent followed by T4. See the single_trigger() function to trigger a sweep.
        """
        return ['T1', 'T4']

    @write
    def single_trigger(self):
        """
        Triggers a single sweep.
        """
        return 'T4'

    @query
    def get_power_level(self):
        """
        Returns the power level of the sweep oscillator.
        """
        return 'OP PL'

    @write
    def reset_sweep(self):
        """
        Resets the current sweep.
        """
        return 'RS'

    @write
    def take_sweep(self):
        """
        Takes a new sweep.
        """
        return 'TS'

    @write
    def initialize_instrument(self):
        super(HP8350B, self).initialize_instrument()
        return 'REN'


class SR830(Instrument):
    # noinspection SpellCheckingInspection
    """
    The SR830 class is used to control a Stanford Research Systems SR830 Lock-In Amplifier via GPIB.
    """

    UNIT_GHZ = 'GZ'
    UNIT_MHZ = 'MZ'
    UNIT_KHZ = 'KZ'
    UNIT_HZ = 'HZ'

    REFERENCE_SOURCE_EXTERNAL = 0
    REFERENCE_SOURCE_INTERNAL = 1

    REFERENCE_TRIGGER_MODE_SINE_ZERO_CROSSING = 0
    REFERENCE_TRIGGER_MODE_TTL_RISING_EDGE = 1
    REFERENCE_TRIGGER_MODE_TTL_FALLING_EDGE = 2

    INPUT_CONFIGURATION_A = 0
    INPUT_CONFIGURATION_A_MINUS_B = 1
    INPUT_CONFIGURATION_I_1M_OHM = 2
    INPUT_CONFIGURATION_I_100M_OHM = 3

    INPUT_SHIELD_GROUNDING_FLOAT = 0
    INPUT_SHIELD_GROUNDING_GROUND = 1

    INPUT_COUPLING_AC = 0
    INPUT_COUPLING_DC = 1

    INPUT_NOTCH_OUT_OR_NO = 0
    INPUT_NOTCH_IN = 1
    INPUT_NOTCH_2X_IN = 2
    INPUT_NOTCH_BOTH_IN = 3

    SENSITIVITY_2nV_PER_fA = 0
    SENSITIVITY_5nV_PER_fA = 1
    SENSITIVITY_10nV_PER_fA = 2
    SENSITIVITY_20nV_PER_fA = 3
    SENSITIVITY_50nV_PER_fA = 4
    SENSITIVITY_100nV_PER_fA = 5
    SENSITIVITY_200nV_PER_fA = 6
    SENSITIVITY_500nV_PER_fA = 7
    SENSITIVITY_1uV_PER_pA = 8
    SENSITIVITY_2uV_PER_pA = 9
    SENSITIVITY_5uV_PER_pA = 10
    SENSITIVITY_10uV_PER_pA = 11
    SENSITIVITY_20uV_PER_pA = 12
    SENSITIVITY_50uV_PER_pA = 13
    SENSITIVITY_100uV_PER_pA = 14
    SENSITIVITY_200uV_PER_pA = 15
    SENSITIVITY_500uV_PER_pA = 16
    SENSITIVITY_1mV_PER_nA = 17
    SENSITIVITY_2mV_PER_nA = 18
    SENSITIVITY_5mV_PER_nA = 19
    SENSITIVITY_10mV_PER_nA = 20
    SENSITIVITY_20mV_PER_nA = 21
    SENSITIVITY_50mV_PER_nA = 22
    SENSITIVITY_100mV_PER_nA = 23
    SENSITIVITY_200mV_PER_nA = 24
    SENSITIVITY_500mV_PER_nA = 25
    SENSITIVITY_1V_PER_uA = 26

    RESERVE_MODE_HIGH_RESERVE = 0
    RESERVE_MODE_NORMAL = 1
    RESERVE_MODE_LOW_NOISE = 2

    TIME_CONSTANT_10us = 0
    TIME_CONSTANT_30us = 1
    TIME_CONSTANT_100us = 2
    TIME_CONSTANT_300us = 3
    TIME_CONSTANT_1ms = 4
    TIME_CONSTANT_3ms = 5
    TIME_CONSTANT_10ms = 6
    TIME_CONSTANT_30ms = 7
    TIME_CONSTANT_100ms = 8
    TIME_CONSTANT_300ms = 9
    TIME_CONSTANT_1s = 10
    TIME_CONSTANT_3s = 11
    TIME_CONSTANT_10s = 12
    TIME_CONSTANT_30s = 13
    TIME_CONSTANT_100s = 14
    TIME_CONSTANT_300s = 15
    TIME_CONSTANT_1ks = 16
    TIME_CONSTANT_3ks = 17
    TIME_CONSTANT_10ks = 18
    TIME_CONSTANT_30ks = 19

    LOW_PASS_FILTER_SLOPE_6dB_PER_OCT = 0
    LOW_PASS_FILTER_SLOPE_12dB_PER_OCT = 1
    LOW_PASS_FILTER_SLOPE_18dB_PER_OCT = 2
    LOW_PASS_FILTER_SLOPE_24dB_PER_OCT = 3

    SYNC_FILTER_OFF = 0
    SYNC_FILTER_ON = 1

    DISPLAY_CHANNEL1_X = 0
    DISPLAY_CHANNEL1_R = 1
    DISPLAY_CHANNEL1_X_NOISE = 2
    DISPLAY_CHANNEL1_AUX1 = 3
    DISPLAY_CHANNEL1_AUX2 = 4

    DISPLAY_CHANNEL2_Y = 0
    DISPLAY_CHANNEL2_THETA = 1
    DISPLAY_CHANNEL2_Y_NOISE = 2
    DISPLAY_CHANNEL2_AUX3 = 3
    DISPLAY_CHANNEL2_AUX4 = 4

    DISPLAY_CHANNEL1_RATIO_NONE = 0
    DISPLAY_CHANNEL1_RATIO_AUX1 = 1
    DISPLAY_CHANNEL1_RATIO_AUX2 = 2

    DISPLAY_CHANNEL2_RATIO_NONE = 0
    DISPLAY_CHANNEL2_RATIO_AUX3 = 1
    DISPLAY_CHANNEL2_RATIO_AUX4 = 2

    CHANNEL1_OUTPUT_DISPLAY = 0
    CHANNEL1_OUTPUT_X = 1

    CHANNEL2_OUTPUT_DISPLAY = 0
    CHANNEL2_OUTPUT_Y = 1

    OFFSET_EXPAND_1X = 0
    OFFSET_EXPAND_10X = 1
    OFFSET_EXPAND_100X = 2

    _PARAMETER_X = 1
    _PARAMETER_Y = 2
    _PARAMETER_R = 3
    _PARAMETER_THETA = 4

    CHANNEL_AUX1 = 1
    CHANNEL_AUX2 = 2
    CHANNEL_AUX3 = 3
    CHANNEL_AUX4 = 4

    OUTPUT_INTERFACE_RS232 = 0
    OUTPUT_INTERFACE_GPIB = 1

    FRONT_PANEL_LOCK_ON = 0
    FRONT_PANEL_LOCK_OFF = 1

    KEY_CLICK_OFF = 0
    KEY_CLICK_ON = 1

    ALARM_OFF = 0
    ALARM_ON = 1

    SAMPLE_RATE_62_POINT_5_mHz = 0
    SAMPLE_RATE_125_mHz = 1
    SAMPLE_RATE_250_mHz = 2
    SAMPLE_RATE_500_mHz = 3
    SAMPLE_RATE_1_Hz = 4
    SAMPLE_RATE_2_Hz = 5
    SAMPLE_RATE_4_Hz = 6
    SAMPLE_RATE_8_Hz = 7
    SAMPLE_RATE_16_Hz = 8
    SAMPLE_RATE_32_Hz = 9
    SAMPLE_RATE_64_Hz = 10
    SAMPLE_RATE_128_Hz = 11
    SAMPLE_RATE_256_Hz = 12
    SAMPLE_RATE_512_Hz = 13
    SAMPLE_RATE_TRIGGER = 14

    END_OF_BUFFER_SHOT = 0
    END_OF_BUFFER_LOOP = 1

    TRIGGER_START_MODE_OFF = 0
    TRIGGER_START_MODE_ON = 1

    _SNAP_VALUES_MAP = dict(X=1, Y=2, R=3, THETA=4, AUX1=5, AUX2=6, AUX3=7, AUX4=8, REF_FREQ=9, CH1=10, CH2=11)

    _CHANNEL1 = 1
    _CHANNEL2 = 2

    @query
    def identify(self):
        return '*IDN?'

    @query
    def get_reference_phase_shift(self):
        """
        Returns the phase shift in degrees.
        """
        # noinspection SpellCheckingInspection
        return 'PHAS?'

    @write
    def set_reference_phase_shift(self, phase):
        """
        Sets the reference phase shift (in degrees), rounded to 0.01. The phase may be programmed from -360.00 <= x <=
        729.99 and will be wrapped around at +/-180.
        :param phase: Phase in degrees
        """
        # noinspection SpellCheckingInspection
        return 'PHAS ' + str(phase)

    @query
    def get_reference_source(self):
        """
        Returns the selected reference source (either REFERENCE_SOURCE_EXTERNAL or REFERENCE_SOURCE_INTERNAL).
        """
        # noinspection SpellCheckingInspection
        return 'FMOD?'

    @write
    def set_reference_source(self, reference_source=REFERENCE_SOURCE_EXTERNAL):
        """
        Sets the reference source (either REFERENCE_SOURCE_EXTERNAL or REFERENCE_SOURCE_INTERNAL).
        :param reference_source: Either REFERENCE_SOURCE_EXTERNAL or REFERENCE_SOURCE_INTERNAL
        """
        # noinspection SpellCheckingInspection
        return 'FMOD ' + str(reference_source)

    @query
    def get_reference_frequency(self):
        """
        Returns the reference frequency (in internal or external mode) in Hz.
        """
        return 'FREQ?'

    @write
    def set_reference_frequency(self, reference_frequency, unit):
        """
        Sets the reference frequency, only used in internal mode.
        :param reference_frequency: The reference frequency to set (default 1)
        :param unit: The units of the reference frequency (default UNIT_KHZ)
        """
        return 'FREQ ' + str(self._scale_freq_to_unit(reference_frequency, unit))

    @query
    def get_reference_trigger_mode(self):
        """
        Returns the reference trigger mode (either REFERENCE_TRIGGER_MODE_SINE_ZERO_CROSSING,
        REFERENCE_TRIGGER_MODE_TTL_RISING_EDGE, or REFERENCE_TRIGGER_MODE_TTL_FALLING_EDGE).
        """
        # noinspection SpellCheckingInspection
        return 'RSLP?'

    @write
    def set_reference_trigger_mode(self, mode=REFERENCE_TRIGGER_MODE_TTL_RISING_EDGE):
        """
        Sets the reference trigger mode to either REFERENCE_TRIGGER_MODE_SINE_ZERO_CROSSING,
        REFERENCE_TRIGGER_MODE_TTL_RISING_EDGE, or REFERENCE_TRIGGER_MODE_TTL_FALLING_EDGE.
        :param mode: Either REFERENCE_TRIGGER_MODE_SINE_ZERO_CROSSING, REFERENCE_TRIGGER_MODE_TTL_RISING_EDGE, or
        REFERENCE_TRIGGER_MODE_TTL_FALLING_EDGE
        """
        # noinspection SpellCheckingInspection
        return 'RSLP ' + str(mode)

    @query
    def get_detection_harmonic(self):
        """
        Returns the detection harmonic.
        """
        return 'HARM?'

    @write
    def set_detection_harmonic(self, harmonic=1):
        """
        Sets the detection harmonic. Should be a value between 1 and 19999. Other values will be brought into this
        range. Defaults to 1.
        :param harmonic: The harmonic to set detection to.
        """
        if harmonic > 19999:
            harmonic = 19999
        elif harmonic < 1:
            harmonic = 1
        return 'HARM ' + str(harmonic)

    @query
    def get_sine_output_amplitude(self):
        """
        Returns the sine output amplitude.
        """
        # noinspection SpellCheckingInspection
        return 'SLVL?'

    @write
    def set_sine_output_amplitude(self, amplitude=1):
        """
        The amplitude to set the sine output to in volts, rounded to 0.002V.
        :param amplitude: The amplitude (in volts) to set the sine output to, between 0.004V and 5.000V.
        """
        # noinspection SpellCheckingInspection
        return 'SLVL ' + str(amplitude)

    @query
    def get_input_configuration(self):
        """
        Returns the input configuration, either INPUT_CONFIGURATION_A, INPUT_CONFIGURATION_A_MINUS_B,
        INPUT_CONFIGURATION_I_1M_OHM, or INPUT_CONFIGURATION_I_100M_OHM.
        """
        # noinspection SpellCheckingInspection
        return 'ISRC?'

    @write
    def set_input_configuration(self, configuration=INPUT_CONFIGURATION_A):
        """
        Sets the input configuration to either INPUT_CONFIGURATION_A, INPUT_CONFIGURATION_A_MINUS_B,
        INPUT_CONFIGURATION_I_1M_OHM, or INPUT_CONFIGURATION_I_100M_OHM.
        :param configuration: The input configuraiton to set, either INPUT_CONFIGURATION_A,
        INPUT_CONFIGURATION_A_MINUS_B, INPUT_CONFIGURATION_I_1M_OHM, or INPUT_CONFIGURATION_I_100M_OHM
        """
        # noinspection SpellCheckingInspection
        return 'ISRC ' + str(configuration)

    @query
    def get_input_shield_grounding(self):
        """
        Returns the input shield grounding, either INPUT_SHIELD_GROUNDING_FLOAT or INPUT_SHIELD_GROUNDING_GROUND.
        """
        # noinspection SpellCheckingInspection
        return 'IGND?'

    @write
    def set_input_shield_grounding(self, mode=INPUT_SHIELD_GROUNDING_FLOAT):
        """
        Sets the input shield grounding to either INPUT_SHIELD_GROUNDING_FLOAT or INPUT_SHIELD_GROUNDING_GROUND.
        :param mode: The input shield grounding mode, either INPUT_SHIELD_GROUNDING_FLOAT or
        INPUT_SHIELD_GROUNDING_GROUND
        """
        # noinspection SpellCheckingInspection
        return 'IGND ' + str(mode)

    @query
    def get_input_coupling(self):
        """
        Returns the input coupling, either INPUT_COUPLING_AC or INPUT_COUPLING_DC.
        """
        # noinspection SpellCheckingInspection
        return 'ICPL?'

    @write
    def set_input_coupling(self, coupling=INPUT_COUPLING_DC):
        """
        Sets the input coupling, either INPUT_COUPLING_AC or INPUT_COUPLING_DC.
        :param coupling: Either INPUT_COUPLING_AC or INPUT_COUPLING_DC
        """
        # noinspection SpellCheckingInspection
        return 'ICPL ' + str(coupling)

    @query
    def get_input_notch_line_filter(self):
        """
        Returns the input notch line filter status, either INPUT_NOTCH_OUT_OR_NO, INPUT_NOTCH_IN, INPUT_NOTCH_2X_IN, or
        INPUT_NOTCH_BOTH_IN.
        :return:
        """
        # noinspection SpellCheckingInspection
        return 'ILIN?'

    @write
    def set_input_notch_line_filter(self, mode=INPUT_NOTCH_OUT_OR_NO):
        """
        Sets the input notch line filter to either INPUT_NOTCH_OUT_OR_NO, INPUT_NOTCH_IN, INPUT_NOTCH_2X_IN, or
        INPUT_NOTCH_BOTH_IN.
        :param mode: Either INPUT_NOTCH_OUT_OR_NO, INPUT_NOTCH_IN, INPUT_NOTCH_2X_IN, or INPUT_NOTCH_BOTH_IN
        """
        # noinspection SpellCheckingInspection
        return 'ILIN ' + str(mode)

    @query
    def get_sensitivity(self):
        """
        Returns the sensitivity, which will be one of the constants of form SENSITIVITY_?*V_per_?A.
        """
        return 'SENS?'

    @write
    def set_sensitivity(self, sensitivity=SENSITIVITY_10uV_PER_pA):
        """
        Sets the sensitivity to one of the constants of form SENSITIVITY_?*V_per_?A.
        :param sensitivity: The sensitivity, one of the constants of form SENSITIVITY_?*V_per_?A
        """
        return 'SENS ' + str(sensitivity)

    @query
    def get_reserve_mode(self):
        """
        Returns the reserve mode, either RESERVE_MODE_HIGH_RESERVE, RESERVE_MODE_NORMAL, or RESERVE_MODE_LOW_NOISE.
        """
        return 'RMOD?'

    @write
    def set_reserve_mode(self, mode=RESERVE_MODE_LOW_NOISE):
        """
        Sets the reserve mode to either RESERVE_MODE_HIGH_RESERVE, RESERVE_MODE_NORMAL, or RESERVE_MODE_LOW_NOISE.
        :param mode: Either RESERVE_MODE_HIGH_RESERVE, RESERVE_MODE_NORMAL, or RESERVE_MODE_LOW_NOISE
        """
        return 'RMOD ' + str(mode)

    @query
    def get_time_constant(self):
        """
        Returns the time constant, which will be one of the constants of form TIME_CONSTANT_?*s.
        """
        # noinspection SpellCheckingInspection
        return 'OFLT?'

    @write
    def set_time_constant(self, time_constant=TIME_CONSTANT_100ms):
        """
        Sets the time constant, which will be one of the constants of form TIME_CONSTANT_?*s.
        :param time_constant: The time constant, one of the constants of form TIME_CONSTANT_?*s
        """
        # noinspection SpellCheckingInspection
        return 'OFLT ' + str(time_constant)

    @query
    def get_low_pass_filter_slope(self):
        """
        Returns the low pass filter slope, either LOW_PASS_FILTER_SLOPE_6dB_PER_OCT, LOW_PASS_FILTER_SLOPE_12dB_PER_OCT,
        LOW_PASS_FILTER_SLOPE_18dB_PER_OCT, or LOW_PASS_FILTER_SLOPE_24dB_PER_OCT.
        """
        # noinspection SpellCheckingInspection
        return 'OFSL?'

    @write
    def set_low_pass_filter_slope(self, slope):
        """
        Sets the low pass filter slope, either LOW_PASS_FILTER_SLOPE_6dB_PER_OCT, LOW_PASS_FILTER_SLOPE_12dB_PER_OCT,
        LOW_PASS_FILTER_SLOPE_18dB_PER_OCT, or LOW_PASS_FILTER_SLOPE_24dB_PER_OCT.
        :param slope: Either LOW_PASS_FILTER_SLOPE_6dB_PER_OCT, LOW_PASS_FILTER_SLOPE_12dB_PER_OCT,
        LOW_PASS_FILTER_SLOPE_18dB_PER_OCT, or LOW_PASS_FILTER_SLOPE_24dB_PER_OCT
        """
        # noinspection SpellCheckingInspection
        return 'OFSL ' + str(slope)

    @query
    def get_synchronous_filter_status(self):
        """
        Returns the synchronous filter status, either SYNC_FILTER_ON or SYNC_FILTER_OFF.
        :return:
        """
        return 'SYNC?'

    @write
    def set_synchronous_filter_status(self, on_off=SYNC_FILTER_OFF):
        """
        Sets the synchronous filter status, either SYNC_FILTER_ON or SYNC_FILTER_OFF.
        :param on_off: Either SYNC_FILTER_ON or SYNC_FILTER_OFF
        """
        return 'SYNC ' + str(on_off)

    def get_channel1_display(self):
        """
        Returns a tuple of the channel 1 display and ratio, see the DISPLAY_CHANNEL1 and DISPLAY_CHANNEL1_RATIO
        constants.
        """
        print("Querying to " + self.get_name() + " --> DDEF? 1")
        response = self.query('DDEF? 1')
        if response.rfind('\n') != -1:
            response = response[:response.rfind('\n')]
        print("Received from " + self.get_name() + " <-- " + response)
        parameter = int(response[:1])
        ratio = int(response[2:])
        return parameter, ratio

    @write
    def set_channel1_display(self, display=DISPLAY_CHANNEL1_R, ratio=DISPLAY_CHANNEL1_RATIO_NONE):
        """
        Sets the channel one display and ratio, see the DISPLAY_CHANNEL1 and DISPLAY_CHANNEL1_RATIO constants.
        :param display: The display, see the DISPLAY_CHANNEL1 constants.
        :param ratio: The ratio, see the DISPLAY_CHANNEL1_RATIO constants.
        """
        # noinspection SpellCheckingInspection
        return 'DDEF 1,' + str(display) + ',' + str(ratio)

    def get_channel2_display(self):
        """
        Returns a tuple of the channel 2 display and ratio, see the DISPLAY_CHANNEL2 and DISPLAY_CHANNEL2_RATIO
        constants.
        """
        print("Querying to " + self.get_name() + " --> DDEF? 2")
        response = self.query('DDEF? 2')
        if response.rfind('\n') != -1:
            response = response[:response.rfind('\n')]
        print("Received from " + self.get_name() + " <-- " + response)
        parameter = int(response[:1])
        ratio = int(response[2:])
        return parameter, ratio

    @write
    def set_channel2_display(self, display=DISPLAY_CHANNEL2_THETA, ratio=DISPLAY_CHANNEL2_RATIO_NONE):
        """
        Sets the channel one display and ratio, see the DISPLAY_CHANNEL2 and DISPLAY_CHANNEL2_RATIO constants.
        :param display: The display, see the DISPLAY_CHANNEL2 constants.
        :param ratio: The ratio, see the DISPLAY_CHANNEL2_RATIO constants.
        """
        # noinspection SpellCheckingInspection
        return 'DDEF 2,' + str(display) + ',' + str(ratio)

    @query
    def get_channel1_output(self):
        """
        Returns the source of the front panel channel 1 output, either CHANNEL1_OUTPUT_DISPLAY or CHANNEL1_OUTPUT_X.
        """
        return 'FPOP? 1'

    @write
    def set_channel1_output(self, output=CHANNEL1_OUTPUT_DISPLAY):
        """
        Returns the source of the front panel channel 1 output, either CHANNEL1_OUTPUT_DISPLAY or CHANNEL1_OUTPUT_X.
        """
        return 'FPOP 1,' + str(output)

    @query
    def get_channel2_output(self):
        """
        Returns the source of the front panel channel 1 output, either CHANNEL2_OUTPUT_DISPLAY or CHANNEL2_OUTPUT_Y.
        """
        return 'FPOP? 2'

    @write
    def set_channel2_output(self, output=CHANNEL2_OUTPUT_DISPLAY):
        """
        Returns the source of the front panel channel 1 output, either CHANNEL2_OUTPUT_DISPLAY or CHANNEL2_OUTPUT_Y.
        """
        return 'FPOP 2,' + str(output)

    def _get_offset(self, parameter):
        """
        Returns a tuple of the specified parameter's offset and expand (the expand will be one of the OFFSET_EXPAND_?*X
        constants).
        :param parameter: The parameter to set the offset of (see _PARAMETER_? constants)
        """
        print("Querying to " + self.get_name() + " --> OEXP? " + str(parameter))
        response = self.query('OEXP? ' + str(parameter))
        if response.rfind('\n') != -1:
            response = response[:response.rfind('\n')]
        print("Received from " + self.get_name() + " <-- " + response)
        offset = float(response[:1])
        expand = int(response[2:])
        return offset, expand

    @write
    def _set_offset(self, parameter, offset=0, expand=OFFSET_EXPAND_1X):
        """
        Sets the offset of the specified parameter.
        :param parameter: The parameter to set the offset of (see _PARAMETER_? constants)
        :param offset: The offset in percent from -105 to 105
        :param expand: Multiplier for the offset, will have form OFFSET_EXPAND_?*X
        """
        # noinspection SpellCheckingInspection
        return str('OEXP ' + str(parameter) + ',' + str(offset) + ',' + str(expand))

    def get_x_offset(self):
        return self._get_offset(self._PARAMETER_X)

    def set_x_offset(self, offset=0, expand=OFFSET_EXPAND_1X):
        self._set_offset(self._PARAMETER_X, offset, expand)

    def get_y_offset(self):
        return self._get_offset(self._PARAMETER_Y)

    def set_y_offset(self, offset=0, expand=OFFSET_EXPAND_1X):
        self._set_offset(self._PARAMETER_Y, offset, expand)

    def get_r_offset(self):
        return self._get_offset(self._PARAMETER_R)

    def set_r_offset(self, offset=0, expand=OFFSET_EXPAND_1X):
        self._set_offset(self._PARAMETER_R, offset, expand)

    def clear_all_offsets(self):
        self._set_offset(self._PARAMETER_X, 0, self.OFFSET_EXPAND_1X)
        self._set_offset(self._PARAMETER_Y, 0, self.OFFSET_EXPAND_1X)
        self._set_offset(self._PARAMETER_R, 0, self.OFFSET_EXPAND_1X)

    @write
    def _auto_offset(self, parameter):
        """
        Automatically adjusts the offset of the specified parameter to zero.
        :param parameter: The parameter to set the offset of (see _OFFSET_PARAMETER_? constants)
        """
        # noinspection SpellCheckingInspection
        return 'AOFF ' + str(parameter)

    def auto_offset_x(self):
        self._auto_offset(self._PARAMETER_X)

    def auto_offset_y(self):
        self._auto_offset(self._PARAMETER_Y)

    def auto_offset_r(self):
        self._auto_offset(self._PARAMETER_R)

    @query
    def get_aux_input_voltage(self, channel=CHANNEL_AUX1):
        """
        Gets the voltage at the specified auxiliary input in volts with a resolution of 1/3mV.
        :param channel: Constant of form CHANNEL_AUX?
        """
        return 'OAUX? ' + str(channel)

    @query
    def get_aux_output_voltage(self, channel=CHANNEL_AUX1):
        """
        Gets the voltage at the specified auxiliary output in volts.
        :param channel: Constant of form CHANNEL_AUX?
        """
        return 'AUXV? ' + str(channel)

    @write
    def set_aux_output_voltage(self, channel=CHANNEL_AUX1, voltage=0):
        # noinspection SpellCheckingInspection
        """
        Gets the voltage at the specified auxiliary output in volts.
        :param channel: Constant of form CHANNEL_AUX?
        :param voltage: Voltage to set output at, to the nearest millivolt and between -10.5V and 10.5V
        """
        return 'AUXV ' + str(channel) + ',' + str(voltage)

    @query
    def get_output_interface(self):
        """
        Gets the output interface of the SR830, either OUTPUT_INTERFACE_RS232 or OUTPUT_INTERFACE_GPIB. The output
        interface is where data communications are output to.
        """
        return 'OUTX?'

    @write
    def set_output_interface(self, output_interface=OUTPUT_INTERFACE_GPIB):
        """
        Sets the output interface of the SR830, either OUTPUT_INTERFACE_RS232 or OUTPUT_INTERFACE_GPIB. The output
        interface is where data communications are output to.
        :param output_interface: Either OUTPUT_INTERFACE_RS232 or OUTPUT_INTERFACE_GPIB
        """
        return 'OUTX ' + str(output_interface)

    @write
    def set_front_panel_lock(self, lock_on_off=FRONT_PANEL_LOCK_ON):
        """
        Sets the front panel lock on or off to user input. By default the SR830 begins with the front panel locked to
        user input.
        :param lock_on_off: Either FRONT_PANEL_LOCK_ON or FRONT_PANEL_LOCK_OFF
        """
        return 'OVRM ' + str(lock_on_off)

    @query
    def get_key_click_state(self):
        """
        Gets the key click state, either KEY_CLICK_ON or KEY_CLICK_OFF.
        """
        return 'KCLK?'

    @query
    def set_key_click_state(self, state=KEY_CLICK_OFF):
        """
        Sets the key click state using either KEY_CLICK_ON or KEY_CLICK_OFF.
        :param state: Either KEY_CLICK_ON or KEY_CLICK_OFF
        """
        return 'KCLK ' + str(state)

    @query
    def get_alarm_state(self):
        """
        Gets the alarm state, either ALARM_ON or ALARM_OFF
        """
        return 'ALRM?'

    @query
    def set_alarm_state(self, state=ALARM_OFF):
        """
        Sets the alarm state using either ALARM_ON or ALARM_OFF.
        :param state: Either ALARM_ON or ALARM_OFF
        """
        return 'ALRM ' + str(state)

    @write
    def save_instrument_state(self, index):
        """
        Saves the instrument settings to the buffer index.
        :param index: The index at which to store the system settings, an integer from 1 to 9
        """
        index = int(index)
        if 1 <= index <= 9:
            return 'SSET ' + str(index)
        return ''

    @write
    def load_instrument_state(self, index):
        """
        Loads the instrument settings from the buffer index.
        :param index: The index at which to retrieve the system settings, an integer from 1 to 9
        """
        index = int(index)
        if 1 <= index <= 9:
            # noinspection SpellCheckingInspection
            return 'SSET ' + str(index)
        return ''

    @write
    def auto_gain(self):
        """
        Performs the Auto Gain function. This command is the same as pressing the [Auto Gain] key.Auto Gain may take
        some time if the time constant is long. AGAN does nothing if the time constant is greater than 1 second. Check
        the command execution in progress bit in the Serial Poll Status Byte (bit 1) to determine when the function is
        finished.
        """
        # noinspection SpellCheckingInspection
        return 'AGAN'

    @write
    def auto_reserve(self):
        """
        Performs the Auto Reserve function. This command is the same as pressing the [Auto Reserve] key. Auto Reserve
        may take some time. Check the command execution in progress bit in the Serial Poll Status Byte (bit 1) to
        determine when the function is finished.
        """
        # noinspection SpellCheckingInspection
        return 'ARSV'

    @write
    def auto_reserve(self):
        """
        Performs the Auto Phase function. This command is the same as pressing the [Auto Phase] key. The outputs will
        take many time constants to reach their new values. Do not send the APHS command again without waiting the
        appropriate amount of time. If the phase is unstable, then APHS will do nothing. Query the new value of the
        phase shift to see if APHS changed the phase shift.
        """
        # noinspection SpellCheckingInspection
        return 'APHS'

    @query
    def get_sample_rate(self):
        """
        Returns the sample rate of the lock-in, will be a SAMPLE_RATE_?* constant.
        """
        return 'SRAT?'

    @write
    def set_sample_rate(self, rate=SAMPLE_RATE_256_Hz):
        """
        Sets the sample rate using a SAMPLE_RATE_?* constant.
        :param rate: The rate, a SAMPLE_RATE_?* constant
        """
        return 'SRAT ' + str(rate)

    def get_storage_time(self):
        """
        Returns the amount of time in seconds that the instrument can store at the current sample rate.
        """
        rate = self.get_sample_rate()
        if rate == self.SAMPLE_RATE_62_POINT_5_mHz:
            return 16383 / 0.0625
        elif rate == self.SAMPLE_RATE_125_mHz:
            return 15383 / 0.125
        elif rate == self.SAMPLE_RATE_250_mHz:
            return 15383 / 0.25
        elif rate == self.SAMPLE_RATE_500_mHz:
            return 15383 / 0.5
        elif rate == self.SAMPLE_RATE_1_Hz:
            return 15383 / 1
        elif rate == self.SAMPLE_RATE_2_Hz:
            return 15383 / 2
        elif rate == self.SAMPLE_RATE_4_Hz:
            return 15383 / 4
        elif rate == self.SAMPLE_RATE_8_Hz:
            return 15383 / 8
        elif rate == self.SAMPLE_RATE_16_Hz:
            return 15383 / 16
        elif rate == self.SAMPLE_RATE_32_Hz:
            return 15383 / 32
        elif rate == self.SAMPLE_RATE_64_Hz:
            return 15383 / 64
        elif rate == self.SAMPLE_RATE_128_Hz:
            return 15383 / 128
        elif rate == self.SAMPLE_RATE_256_Hz:
            return 15383 / 256
        elif rate == self.SAMPLE_RATE_512_Hz:
            return 15383 / 512
        else:
            return None

    @query
    def get_end_of_buffer_mode(self):
        """
        Returns the end of buffer mode, either END_OF_BUFFER_SHOT or END_OF_BUFFER_LOOP. The former stops data storage
        once the buffer is full, while the latter begins to overwrite the oldest data once the buffer is full. The
        instrument will keep the oldest data in bin#0 and the newest data in bin#16382. Data acquisition should be
        paused when reading data in loop mode, as this can cause confusion about which data is the most recent.
        """
        return 'SEND?'

    @write
    def set_end_of_buffer_mode(self, mode=END_OF_BUFFER_SHOT):
        """
        Returns the end of buffer mode, either END_OF_BUFFER_SHOT or END_OF_BUFFER_LOOP. The former stops data storage
        once the buffer is full, while the latter begins to overwrite the oldest data once the buffer is full. The
        instrument will keep the oldest data in bin#0 and the newest data in bin#16382. Data acquisition should be
        paused when reading data in loop mode, as this can cause confusion about which data is the most recent.
        """
        return 'SEND ' + str(mode)

    @write
    def trigger_scan(self):
        return 'TRIG'

    @query
    def get_trigger_mode(self):
        """
        Returns TRIGGER_START_MODE_ON if the trigger start mode is on, TRIGGER_START_MODE_OFF otherwise. If the trigger
        start mode is on, a TTL high trigger to the back panel trigger will start a scan (or the trigger_scan()
        function). If the trigger start mode is off, the start_scan() function will start the scan.
        """
        return 'TSTR?'

    @write
    def set_trigger_mode(self, mode=TRIGGER_START_MODE_OFF):
        """
        Sets the trigger start mode using TRIGGER_START_MODE_ON or TRIGGER_START_MODE_OFF otherwise. If the trigger
        start mode is on, a TTL high trigger to the back panel trigger will start a scan (or the trigger_scan()
        function). If the trigger start mode is off, the start_scan() function will start the scan.
        """
        return 'TSTR ' + str(mode)

    @write
    def start_scan(self):
        """
        Starts or resumes data storage, ignored if storage is already in progress.
        """
        return 'STRT'

    @write
    def pause_scan(self):
        """
        Pauses data storage, ignored if storage is already paused.
        """
        return 'PAUS'

    @write
    def reset_scan(self):
        """
        Resets and erases teh data buffers.
        """
        return 'REST'

    @query
    def _get_output(self, parameter):
        """
        Gets the value of some parameter
        :param parameter: The parameter to set the output of (see _PARAMETER_? constants)
        """
        return 'OUTP? ' + str(parameter)

    def get_x(self):
        return self._get_output(self._PARAMETER_X)

    def get_y(self):
        return self._get_output(self._PARAMETER_Y)

    def get_r(self):
        return self._get_output(self._PARAMETER_R)

    def get_theta(self):
        return self._get_output(self._PARAMETER_THETA)

    @query
    def get_channel1(self):
        """
        Gets the value of the output of channel1.
        """
        return 'OUTR? 1'

    @query
    def get_channel2(self):
        """
        Gets the value of the output of channel2.
        """
        return 'OUTR? 2'

    @write
    def _get_output(self, parameter):
        """
        Gets the value of some parameter
        :param parameter: The parameter to set the output of (see _PARAMETER_? constants)
        """
        return 'OUTP? ' + str(parameter)

    def snap_values(self, values):
        """
        Measures most of values specified in values at a single instant in time. Measurements are returned in a
        dictionary where the keys are the strings in the values list parameter. Please see the SR830 manual p 5-15 for
        more.
        :param values: A list containing up to 6 values to snap. The list can contain strings 'X', 'Y', 'R', 'THETA',
        'AUX1', 'AUX2', 'AUX3', 'AUX4', 'REF_FREQ' (for the reference frequency), 'CH1', and 'CH2' (for channels 1 and
        2, respectively). If the list is longer than 6 values, only the first 6 values will be snapped.
        """
        if 6 < len(values):  # Trim the length of values down to 6 if need be
            values = values[:6]
        snaps = ''
        for val in values:  # Add the integer associated with each value to the snaps string using the _SNAP_VALUES_MAP
            snaps += str(self._SNAP_VALUES_MAP.get(val)) + ','
        snaps = snaps[:len(snaps) - 1]  # Remove the trailing comma from the snaps string
        print("Querying to " + self.get_name() + " --> SNAP? " + snaps)
        response = str(self.query('SNAP? ' + snaps))  # Query the command and save the response as string response
        if response.rfind('\n') != -1:
            response = response[:response.rfind('\n')]  # Remove any newline f
        print("Received from " + self.get_name() + " <-- " + response)
        measurements = response.split(',')  # Split the string response into a list using ',' as delimiters
        to_return = {}
        for i in range(len(measurements)):
            measurement = measurements[i]
            try:
                measurement = float(measurement)
                if measurement.is_integer():
                    measurement = int(measurement)
            except ValueError:
                pass
            to_return[values[i]] = measurement
        return to_return

    @query
    def get_scanned_data_length(self):
        """
        Returns the number of data points in the buffer.
        """
        # noinspection SpellCheckingInspection
        return 'SPTS?'

    def get_channel1_scanned_data(self, start_bin=0, bins_to_return=0):
        """
        Returns a list of data stored in the channel1 data buffer. This data is whatever has been selected by the
        set_channel1_output() function (see also the set_channel1_display() function).
        :param start_bin: The bin in the data buffer to start returning.
        :param bins_to_return: The number of bins to return. If start_bin + bins_to_return is greater than the total
        number of bins than an error occurs.
        """
        return self._get_scanned_data(self._CHANNEL1, start_bin, bins_to_return)

    def get_channel2_scanned_data(self, start_bin=0, bins_to_return=0):
        """
        Returns a list of data stored in the channel2 data buffer. This data is whatever has been selected by the
        set_channel2_output() function (see also the set_channel2_display() function).
        :param start_bin: The bin in the data buffer to start returning.
        :param bins_to_return: The number of bins to return. If start_bin + bins_to_return is greater than the total
        number of bins than an error occurs.
        """
        return self._get_scanned_data(self._CHANNEL2, start_bin, bins_to_return)

    def _get_scanned_data(self, channel, start_bin=0, bins_to_return=0):
        """
        Returns a list of data stored in a channel data buffer.
        :param start_bin: The bin in the data buffer to start returning.
        :param bins_to_return: The number of bins to return. If start_bin + bins_to_return is greater than the total
        number of bins than an error occurs.
        """
        # noinspection SpellCheckingInspection
        print('Querying to ' + self.get_name() + ' --> TRCL? ' + str(channel) + ',' + str(start_bin) + ',' + str(
            bins_to_return))
        # Write the command
        # noinspection SpellCheckingInspection
        self.write('TRCL? ' + str(channel) + ',' + str(start_bin) + ',' + str(bins_to_return))
        # Read the raw response to the command
        raw_response = self.read_raw()
        print("Received from " + self.get_name() + " <-- " + raw_response)
        # Convert the raw_response into a string of 0s and 1s
        bit_string = self._raw_to_bit_string(raw_response)
        # Convert the string of 0s and 1s into a list of numbers and return
        return self._bit_string_to_num_list(bit_string)

    def _raw_to_bit_string(self, raw):
        """
        This function takes a 'raw' string and converts it into a string of bits that represent the string.
        :param raw: The raw string to convert, i.e. 'h'
        :return: The binary string that represents the raw string, i.e. '01101000'
        """
        to_return = ''
        for char in raw:
            # Find the bits that represent each character, removing the leading '0b'
            bits = bin(ord(char))[2:]
            # Add the appropriate number of leading zeros to bits to ensure that there are 8 bits (and thus 1 byte)
            bits = '00000000'[len(bits):] + bits
            # Append bits to the to_return string
            to_return += bits
        return to_return

    def _bit_string_to_num_list(self, bit_string):
        """
        This function takes an arbitrarily long string composed of 0s and 1s, chops it into strings of length 32, and then converts each of these strings into a number using the encoding specified on page 5-17 of the SR830 Lock-In Amplifier manual. These numbers are returned as a list.
        :param bit_string: The string of 0s and 1s to convert.
        :return: The list of numbers represented by the string of 0s and 1s.
        """
        # Create an empty list bin_list to populate with strings of 32 0s and 1s (to represent each number using the encoding specified on page 5-17 of the SR830 Lock-In Amplifier manual).
        bin_list = []
        # Create a count variable and an empty bin variable
        count = 0
        bin = ''
        for char in bit_string:
            # For each character in the bit string, iterate the count and add the character to the bin.
            count += 1
            bin += char
            # Once the count is at 32
            if count >= 32:
                # Add the bin to the bin_list
                bin_list.append(bin)
                # And reset the count and bin variables to their original values
                count = 0
                bin = ''
        num_list = []
        for bin_string in bin_list:
            # Convert each string of binary values (i.e. 0s and 1s) in the bin_list to a number and append it to the num_list.
            num_list.append(self._32_bit_string_to_num(bin_string))
        # Return the num_list
        return num_list

    def _32_bit_string_to_num(self, bit_string):
        """
        This function takes a 32 character string of 1s and 0s (to represent a binary number) and returns the number they represent. It uses the number encoding specified on page 5-17 of the SR830 Lock-In Amplifier manual.
        :param bit_string: The 32 character string that represents the number.
        :return: The number represented by the string as a float.
        """
        # Split up the 32-bits used to represent the number into four bytes
        byte0 = bit_string[0:8]
        byte1 = bit_string[8:16]
        byte2 = bit_string[16:24]
        # byte3 = bit_string[24:32] # byte3 is unused, so it has been commented out
        # Concatenate byte1 and byte0 (i.e. bits 8 to 16 and then bits 0 to 8)
        byte_mantissa = byte1 + byte0
        # Create a new variable to represent byte2 using a friendlier name
        byte_exp = byte2
        # Convert the byte_mantissa string (which is a binary 16-bit integer signed with the twos compliment) to decimal.
        int_mantissa = self._16_bit_string_to_signed_int(byte_mantissa)
        # Convert the byte_exp string (which is a binary 8-bit unsigned integer) to decimal.
        int_exp = int(byte_exp, 2)
        # Calculate the value represented by the 32-bits and return
        value = float(int_mantissa) * (2.0 ** (int_exp - 124.0))
        return value

    def _16_bit_string_to_signed_int(self, bit_string):
        """
        This function takes a 16-bit binary string and returns its signed integer value (signed using two's compliment).
        :param bit_string: The binary string to convert.
        :return: The signed integer
        """
        # First check if the bit_string represents a positive number.
        if bit_string[0] != '1':
            # If the bit_string represents a positive number, return that number.
            return int(bit_string, 2)
        # The bit_string represents a negative number, so find the substring of bit_string that needs to be inverted. This is the string from the first character to the character before the last '1'.
        to_invert = bit_string[:bit_string.rfind('1')]
        # Invert the to_invert string, creating a string inverted
        inverted = ''
        for char in to_invert:
            if char == '0':
                # If the character is '0', append '1' to the inverted string
                inverted += '1'
            else:
                # If the character is '1', append '0' to the inverted string
                inverted += '0'
        # Append the non-inverted part of bit_string to inverted
        inverted += bit_string[bit_string.rfind('1'):]
        # Multiply the integer value of inverted by -1 and return
        return -1 * int(inverted, 2)

    @write
    def reset(self):
        """
        Resets the SR830 to its default configurations.
        """
        return '*RST'

    def initialize_instrument(self):
        super(SR830, self).initialize_instrument()
        self.set_output_interface(self.OUTPUT_INTERFACE_GPIB)

    @classmethod
    def _scale_freq_to_unit(cls, reference_frequency, unit):
        """
        Takes a reference_frequency and a unit (either UNIT_GHZ, UNIT_MHZ, UNIT_KHZ, or UNIT_HZ) and returns the same
        frequency in Hz.
        :param reference_frequency: The frequency associated with a unit
        :param unit: The unit of frequency (either UNIT_GHZ, UNIT_MHZ, UNIT_KHZ, or UNIT_HZ). If no unit is supplied the
        method will assume UNIT_HZ
        :return: The reference_frequency in Hz
        """
        if unit == cls.UNIT_GHZ:
            return reference_frequency * (10 ^ 9)
        elif unit == cls.UNIT_MHZ:
            return reference_frequency * (10 ^ 6)
        elif unit == cls.UNIT_KHZ:
            return reference_frequency * (10 ^ 3)
        else:
            return reference_frequency


class Agilent33220A(Instrument):
    # noinspection SpellCheckingInspection
    """
    The Agilent33220A class is used to control a Agilent 33220A function generator via GPIB.
    """

    WAVE_TYPE_SINE = 'SIN'
    WAVE_TYPE_SQUARE = 'SQU'
    WAVE_TYPE_RAMP = 'RAMP'
    WAVE_TYPE_PULSE = 'PULS'
    WAVE_TYPE_NOISE = 'NOIS'
    WAVE_TYPE_DC = 'DC'

    _VOLTAGE_UNIT_VPP = 'VPP'
    _VOLTAGE_UNIT_RMS = 'VRMS'

    STATE_ON = 1
    STATE_OFF = 0

    SWEEP_SPACING_LINEAR = 'LIN'
    SWEEP_SPACING_LOGARITHMIC = 'LOG'

    @query
    def get_wave_type(self):
        """
        Gets the wave type. Will be one of the WAVE_TYPE_?* constants.
        """
        return 'FUNC?'

    @write
    def set_wave_type(self, wave_type=WAVE_TYPE_SQUARE):
        """
        Sets the wave type using one of the WAVE_TYPE_?* constants.
        :param wave_type: The wave type to set, one of the WAVE_TYPE_?* constants
        """
        return 'FUNC ' + wave_type

    @query
    def get_wave_frequency(self):
        """
        Gets the wave frequency in hertz.
        """
        return 'FREQ?'

    @write
    def set_wave_frequency(self, freq=10000.0):
        """
        Sets the wave frequency in hertz.
        :param freq: The wave frequency in hertz
        """
        return 'FREQ ' + str(freq)

    @query
    def get_wave_amplitude(self):
        """
        Gets the wave RMS amplitude in volts.
        """
        return 'VOLT?'

    @write
    def set_wave_amplitude(self, amplitude=0.5):
        """
        Sets the wave RMS amplitude in volts.
        :param amplitude: The wave amplitude in volts
        """
        return ['VOLT:HIGH ' + str(amplitude), 'VOLT:LOW 0']

    @query
    def _get_voltage_unit(self):
        """
        Gets the voltage unit, either _VOLTAGE_UNIT_VPP or _VOLTAGE_UNIT_RMS.
        """
        return 'UNIT?'

    @write
    def _set_voltage_unit(self, unit=_VOLTAGE_UNIT_RMS):
        """
        Sets the voltage unit, either _VOLTAGE_UNIT_VPP or _VOLTAGE_UNIT_RMS.
        :param unit: The unit, either _VOLTAGE_UNIT_VPP or _VOLTAGE_UNIT_RMS
        """
        return 'UNIT ' + unit

    @query
    def get_output_state(self):
        """
        Gets the output state, either OUTPUT_STATE_ON or OUTPUT_STATE_OFF
        """
        return 'OUTP?'

    @write
    def set_output_state(self, state=STATE_OFF):
        """
        Gets the output state, either OUTPUT_STATE_ON or OUTPUT_STATE_OFF
        """
        return 'OUTP ' + str(state)

    @query
    def get_sweep_start(self):
        """
        Gets the frequency sweep start frequency in hertz.
        """
        return 'FREQ:STAR?'

    @write
    def set_sweep_start(self, freq=1000.0):
        """
        Sets the frequency start frequency in hertz.
        :param freq: The start frequency in hertz
        """
        return 'FREQ:STAR ' + str(freq)

    @query
    def get_sweep_stop(self):
        """
        Gets the frequency sweep stop frequency in hertz.
        """
        return 'FREQ:STOP?'

    @write
    def set_sweep_stop(self, freq=100000.0):
        """
        Sets the frequency stop frequency in hertz.
        :param freq: The stop frequency in hertz
        """
        return 'FREQ:STOP ' + str(freq)

    @query
    def get_sweep_time(self):
        """
        Gets the frequency sweep time in seconds.
        """
        return 'SWE:TIME?'

    @write
    def set_sweep_time(self, time=10):
        """
        Sets the frequency sweep time in seconds.
        :param time: The frequency sweep time in seconds
        """
        return 'SWE:TIME ' + str(time)

    @query
    def get_sweep_spacing(self):
        """
        Gets the frequency spacing, either SWEEP_SPACING_LINEAR or SWEEP_SPACING_LOGARITHMIC.
        """
        return 'SWE:SPAC?'

    @write
    def set_sweep_spacing(self, spacing=SWEEP_SPACING_LINEAR):
        """
        Sets the frequency spacing, either SWEEP_SPACING_LINEAR or SWEEP_SPACING_LOGARITHMIC.
        :param spacing: Either SWEEP_SPACING_LINEAR or SWEEP_SPACING_LOGARITHMIC
        """
        return 'SWE:SPAC ' + spacing

    @query
    def get_sweep_state(self):
        """
        Gets the sweep state, either STATE_ON or STATE_OFF.
        """
        return 'SWE:STAT?'

    @write
    def set_sweep_state(self, state=STATE_OFF):
        """
        Sets the sweep state, either STATE_ON or STATE_OFF.
        :param state: Either STATE_ON or STATE_OFF
        """
        return 'SWE:STAT ' + str(state)

    SWEEP_TRIGGER_IMMEDIATE = 'IMM'
    SWEEP_TRIGGER_EXTERNAL = 'EXT'
    SWEEP_TRIGGER_SOFTWARE = 'BUS'

    @query
    def get_trigger_source(self):
        """
        Gets the trigger source, one of the SWEEP_TRIGGER_?* constants.
        """
        return 'TRIG:SOUR?'

    @write
    def set_trigger_source(self, source=SWEEP_TRIGGER_SOFTWARE):
        """
        Sets the trigger source, one of the SWEEP_TRIGGER_?* constants.
        :param source: The sweep trigger source, one of the SWEEP_TRIGGER_?* constants
        """
        return 'TRIG:SOUR ' + source

    @write
    def send_trigger(self):
        """
        Sends a trigger signal.
        """
        return '*TRG'

    def initialize_instrument(self):
        super(Agilent33220A, self).initialize_instrument()


class AgilentE3631A(Instrument):
    """
    The AgilentE3631A class is used to control a Agilent E3631A DC power source via GPIB.
    """

    STATE_OFF = 0
    STATE_ON = 1

    @write
    def set_voltage(self, voltage=0, positive_25_voltage=5, negative_25_voltage=5):
        """
        Sets the voltage of the power source.
        :param voltage: The voltage to set the +6 volts source in volts
        :param positive_25_voltage: The voltage to set the +25 volts source in volts
        :param negative_25_voltage: The voltage to set the -25 volts source in volts (this voltage will be made negative automatically)
        """
        return ['APPL P6V,' + str(voltage), 'APPL P25V,' + str(positive_25_voltage),
                'APPL N25V,' + str(negative_25_voltage*-1)]

    @query
    def get_output_state(self):
        """
        Gets the output state of the DC power source, either STATE_ON or STATE_OFF
        """
        return 'OUTP:STAT?'

    @write
    def set_output_state(self, state=STATE_OFF):
        """
        Sets the output state of the DC power source, either STATE_ON or STATE_OFF
        :param state: Either STATE_ON or STATE_OFF
        """
        return 'OUTP:STAT ' + str(state)

    def initialize_instrument(self):
        self.set_output_state(self.STATE_OFF)
        self.set_voltage(0, 0, 0)


class AgilentE3633A(Instrument):
    """
    The AgilentE3633A class is used to control a Agilent E3633A DC power source via GPIB.
    """

    @write
    def set_voltage(self, voltage=8):
        """
        Sets the voltage of the power source.
        :param voltage: The voltage to set the +6 volts source in volts
        """
        return 'APPL ' + str(voltage) + ',0'

    @write
    def _set_current_state_off(self):
        """
        Disables current output
        """
        return 'SOUR:CURR:PROT:STAT 0'

    def initialize_instrument(self):
        self._set_current_state_off()
        self.set_voltage(0)



class PasternackPE11S390(Instrument):
    """
    The PasternackPE11S390 class is used to control a Pasternack PE11S390 series frequency synthesizers via USB.
    """

    OUTPUT_STATE_OFF = 0
    OUTPUT_STATE_ON = 1

    @write
    def set_output_state(self, output_state=OUTPUT_STATE_OFF):
        """
        Turns the RF output either on or off using the OUTPUT_STATE_ constants.
        :param output_state: Either OUTPUT_STATE_ON or OUTPUT_STATE_OFF
        """
        return 'POWE:RF ' + str(output_state) + ';'

    @query
    def get_output_state(self):
        """
        Gets the RF output, one of the OUTPUT_STATE_ constants.
        """
        return 'POWE:RF?;'

    @write
    def set_frequency(self, frequency=10):
        """
        Sets the frequency in GHz.
        :param frequency: The frequency in GHz
        """
        return 'FREQ:SET ' + str(frequency) + ';'

    @query
    def get_frequency(self):
        """
        Gets the frequency in GHz.
        """
        return 'FREQ:RETACT?;'

    @write
    def set_power(self, power=10):
        """
        Sets the power in dBm.
        :param power: The power in dBm
        """
        return 'POWE:SET ' + str(power) + ';'

    @query
    def get_power(self):
        """
        Gets the power in in dBm.
        """
        return 'POWE:SET?;'

    def initialize_instrument(self):
        self.set_output_state(self.OUTPUT_STATE_OFF)
