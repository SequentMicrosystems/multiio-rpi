#!/usr/bin/python3

from smbus2 import SMBus
import struct
import datetime

import multiio.multiio_data as data
I2C_MEM = data.I2C_MEM
CHANNEL_NO = data.CHANNEL_NO
CALIB = data.CALIB

class SMmultiio: 
    """Python class to control the Multiio Card for Raspberry Pi.

    Args:
        stack (int): Stack level/device number.
        i2c (int): i2c bus number
    """
    def __init__(self, stack=0, i2c=1):
        if stack < 0 or stack > data.STACK_LEVEL_MAX:
            raise ValueError("Invalid stack level!")
        self._hw_address_ = data.SLAVE_OWN_ADDRESS_BASE + stack
        self._i2c_bus_no = i2c
        self.bus = SMBus(self._i2c_bus_no)
        try:
            self._card_rev_major = self.bus.read_byte_data(self._hw_address_, I2C_MEM.REVISION_HW_MAJOR_ADD)
            self._card_rev_minor = self.bus.read_byte_data(self._hw_address_, I2C_MEM.REVISION_HW_MINOR_ADD)
        except Exception:
            print("{} not detected!".format(data.CARD_NAME))
            raise

    def _get_byte(self, address):
        return self.bus.read_byte_data(self._hw_address_, address)
    def _get_word(self, address):
        return self.bus.read_word_data(self._hw_address_, address)
    def _get_i16(self, address):
        buf = self.bus.read_i2c_block_data(self._hw_address_, address, 2)
        i16_value = struct.unpack("h", bytearray(buf))[0]
        return i16_value
    def _get_float(self, address):
        buf = self.bus.read_i2c_block_data(self._hw_address_, address, 4)
        float_value = struct.unpack("f", bytearray(buf))[0]
        return float_value
    def _get_i32(self, address):
        buf = self.bus.read_i2c_block_data(self._hw_address_, address, 4)
        i32_value = struct.unpack("i", bytearray(buf))[0]
        return i32_value
    def _get_u32(self, address):
        buf = self.bus.read_i2c_block_data(self._hw_address_, address, 4)
        u32_value = struct.unpack("I", bytearray(buf))[0]
        return u32_value
    def _get_block_data(self, address, byteno=4):
        return self.bus.read_i2c_block_data(self._hw_address_, address, byteno)
    def _set_byte(self, address, value):
        self.bus.write_byte_data(self._hw_address_, address, value)
    def _set_word(self, address, value):
        self.bus.write_word_data(self._hw_address_, address, value)
    def _set_float(self, address, value):
        ba = bytearray(struct.pack("f", value))
        self.bus.write_block_data(self._hw_address_, address, ba)
    def _set_i32(self, address, value):
        ba = bytearray(struct.pack("i", value))
        self.bus.write_block_data(self._hw_address_, address, ba)
    def _set_block(self, address, ba):
        self.bus.write_i2c_block_data(self._hw_address_, address, ba)

    @staticmethod
    def _check_channel(channel_type, channel):
        if not (0 <= channel and channel <= CHANNEL_NO[channel_type]):
            raise ValueError("Invalid {} channel number. Must be [1..{}]!".format(channel_type, CHANNEL_NO[channel_type]))
    def _calib_set(self, channel, value):
        ba = bytearray(struct.pack("f", value))
        ba.extend([channel, data.CALIBRATION_KEY])
        self._set_block(I2C_MEM.CALIB_VALUE, ba)

    def _calib_reset(self, channel):
        ba = bytearray([channel, data.CALIBRATION_KEY])
        self._set_block(I2C_MEM.CALIB_CHANNEL, ba)

    def calib_status(self):
        """Get current calibration status of device.

        Returns:
            (int) Calib status
        """
        status = self._get_byte(I2C_MEM.CALIB_STATUS)
        return status

    def get_version(self):
        """Get firmware version.

        Returns: (int) Firmware version number
        """
        version_major = self._get_byte(I2C_MEM.REVISION_MAJOR_ADD)
        version_minor = self._get_byte(I2C_MEM.REVISION_MINOR_ADD)
        version = str(version_major) + "." + str(version_minor)
        return version

    def get_relay(self, relay):
        """Get relay state.

        Args:
            relay (int): Relay number

        Returns:
            (int) Relay state
        """
        self._check_channel("relay", relay)
        val = self._get_byte(I2C_MEM.RELAYS)
        if (val & (1 << (relay - 1))) != 0:
            return 1
        return 0
    def get_all_relays(self):
        """Get all relays state as bitmask.

        Returns:
            (int) Relays state bitmask
        """
        val = self._get_byte(I2C_MEM.RELAYS)
        return val
    def set_relay(self, relay, val):
        """Set relay state.

        Args:
            relay (int): Relay number
            val: 0(OFF) or 1(ON)
        """
        self._check_channel("relay", relay)
        if val == 0:
            self._set_byte(I2C_MEM.RELAY_CLR, relay)
        elif val == 1:
            self._set_byte(I2C_MEM.RELAY_SET, relay)
        else:
            raise ValueError("Invalid relay value[0-1]")
    def set_all_relays(self, val):
        """Set all relays states as bitmask.

        Args:
            val (int): Relay bitmask
        """
        if(not (0 <= val and val <= (1 << CHANNEL_NO["relay"]) - 1)):
            raise ValueError("Invalid relay mask!")
        self._set_byte(I2C_MEM.RELAYS, 0xff & val)

    def get_u_in(self, channel):
        """Get 0-10V input channel value in volts.

        Args:
            channel (int): Channel number

        Returns:
            (float) Input value in volts
        """
        self._check_channel("u_in", channel)
        value = self._get_word(I2C_MEM.U_IN + (channel - 1) * 2)
        return value / data.VOLT_TO_MILIVOLT
    def cal_u_in(self, channel, value):
        """Calibrate 0-10V input channel.
        Calibration must be done in 2 points at min 5V apart.

        Args:
            channel (int): Channel number
            value (int): Voltage value
        """
        self._check_channel("u_in", channel)
        self._calib_set(CALIB.U_IN_CH1 + channel, value)
    def get_u_out(self, channel):
        """Get 0-10V output channel value in volts.

        Args:
            channel (int): Channel number

        Returns:
            (float) 0-10V output value
        """
        self._check_channel("u_out", channel)
        value = self._get_word(I2C_MEM.U_OUT + (channel - 1) * 2)
        return value / data.VOLT_TO_MILIVOLT
    def set_u_out(self, channel, value):
        """Set 0-10V output channel value in volts.

        Args:
            channel (int): Channel number
            value (float): Voltage value
        """
        self._check_channel("u_out", channel)
        value = value * data.VOLT_TO_MILIVOLT
        self._set_word(I2C_MEM.U_OUT + (channel - 1) * 2, value)
    def cal_u_out(self, channel, value):
        """Calibrate 0-10V output channel.
        Calibration must be done in 2 points at min 5V apart.

        Args:
            channel (int): Channel number
            value (float): Real(measured) voltage value
        """
        self._check_channel("u_out", channel)
        self._calib_set(CALIB.U_OUT_CH1 + channel, value)

    def get_i_in(self, channel):
        """Get 4-20mA input channel value in mA.

        Args:
            channel (int): Channel number

        Returns:
            (float) 4-20mA input channel value in mA
        """
        self._check_channel("i_in", channel)
        value = self._get_word(I2C_MEM.I_IN + (channel - 1) * 2)
        return value / data.VOLT_TO_MILIVOLT
    def cal_i_in(self, channel, value):
        """Calibrate 4-20mA input channel.
        Calibration must be done in 2 points at min 10mA apart.

        Args:
            channel (int): Channel number
            value (float): Real(measured) amperage value
        """
        self._check_channel("i_in", channel)
        self._calib_set(CALIB.I_IN_CH1 + channel, value)
    def get_i_out(self, channel):
        """Get 4-20mA output channel value in mA.

        Args:
            channel (int): Channel number

        Returns:
            (float) 4-20mA output value in mA
        """
        self._check_channel("i_out", channel)
        value = self._get_word(I2C_MEM.I_OUT + (channel - 1) * 2)
        return value / data.VOLT_TO_MILIVOLT
    def set_i_out(self, channel, value):
        """Set 4-20mA output channel value in mA.

        Args:
            channel (int): Channel number
            value (float): Amperage value in mA
        """
        self._check_channel("i_out", channel)
        value = value * data.VOLT_TO_MILIVOLT
        self._set_word(I2C_MEM.I_OUT + (channel - 1) * 2, value)
    def cal_i_out(self, channel, value):
        """Calibrate 4-20mA output channel.
        Calibration must be done in 2 points at min 10mA apart.

        Args:
            channel (int): Channel number
            value (float): Real(measured) amperage value
        """
        self._check_channel("i_out", channel)
        self._calib_set(CALIB.I_OUT_CH1 + channel, value)

    def get_rtd_res(self, channel):
        """Get RTD resistance in ohm.

        Args:
            channel (int): RTD channel number

        Returns:
            (float) RTD resistance value
        """
        self._check_channel("rtd", channel)
        return self._get_float(I2C_MEM.RTD_RES1_ADD + (channel - 1) * 4)
    def get_rtd_temp(self, channel):
        """Get RTD temperature in Celsius.

        Args:
            channel (int): RTD channel number

        Returns:
            (float) RTD Celsius value
        """
        self._check_channel("rtd", channel)
        return self._get_float(I2C_MEM.RTD_VAL1_ADD + (channel - 1) * 4)
    def cal_rtd_res(self, channel, value):
        """Calibrate rtd resistance.

        Args:
            channel (int): RTD channel number to calibrate
            value (float): Real(measured) resistance in ohm
        """
        self._check_channel("rtd", channel)
        self._calib_set(CALIB.RTD_CH1 + channel - 1, value)

    def get_led(self, led):
        """Get led state.

        Args:
            led (int): Led number

        Returns:
            0(OFF) or 1(ON)
        """
        self._check_channel("led", led)
        val = self._get_byte(I2C_MEM.LEDS)
        if (val & (1 << (led - 1))) != 0:
            return 1
        return 0
    def get_all_leds(self):
        """Get all leds state as bitmask.

        Returns:
            (int) Leds state bitmask
        """
        return self._get_byte(I2C_MEM.LEDS)
    def set_led(self, led, val):
        """Set led state.

        Args:
            led (int): Led number
            val: 0(OFF) or 1(ON)
        """
        self._check_channel("led", led)
        if val != 0:
            self._set_byte(I2C_MEM.LED_SET, led)
        else:
            self._set_byte(I2C_MEM.LED_CLR, led)
    def set_all_leds(self, val):
        """Set all leds states as bitmask.

        Args:
            val (int): Led bitmask
        """
        if(not (0 <= val and val <= (1 << CHANNEL_NO["led"]) - 1)):
            raise ValueError("Invalid led mask!")
        self._set_byte(I2C_MEM.LEDS, val)

    def wdt_reload(self):
        """Reload watchdog."""
        self._set_byte(I2C_MEM.WDT_RESET_ADD, data.WDT_RESET_SIGNATURE)
    def wdt_get_period(self):
        """Get watchdog period in seconds.

        Returns:
            (int) Watchdog period in seconds
        """
        return self._get_word(I2C_MEM.WDT_INTERVAL_GET_ADD)
    def wdt_set_period(self, period):
        """Set watchdog period.

        Args:
            period (int): Channel number
        """
        return self._set_word(I2C_MEM.WDT_INTERVAL_SET_ADD, period)
    def wdt_get_init_period(self):
        """Get watchdog initial period.

        Returns:
            (int) Initial watchdog period in seconds
        """
        return self._get_word(I2C_MEM.WDT_INIT_INTERVAL_GET_ADD)
    def wdt_set_init_period(self, period):
        """Set watchdog initial period.

        Args:
            period (int): Initial period in second
        """
        return self._set_word(I2C_MEM.WDT_INIT_INTERVAL_SET_ADD, period)

    def wdt_get_off_period(self):
        """Get watchdog off period in seconds.

        Returns:
            (int) Watchfog off period in seconds.
        """
        return self._get_i32(I2C_MEM.WDT_POWER_OFF_INTERVAL_GET_ADD)
    def wdt_set_off_period(self, period):
        """Set off period in seconds

        Args:
            period (int): Off period in seconds
        """
        return self._set_i32(I2C_MEM.WDT_POWER_OFF_INTERVAL_SET_ADD, period)
    def wdt_get_reset_count(self):
        """Get watchdog reset count.

        Returns:
            (int) Watchdog reset count
        """
        return self._get_word(I2C_MEM.WDT_RESET_COUNT_ADD)
    def wdt_clear_reset_count(self):
        """Clear watchdog counter. """
        return self._set_i32(I2C_MEM.WDT_CLEAR_RESET_COUNT_ADD, data.WDT_RESET_COUNT_SIGNATURE)

    def get_rtc(self):
        """Get rtc time.

        Returns:
            (tuple) date(year, month, day, hour, minute, second)
        """
        buf = self._get_block_data(I2C_MEM.RTC_YEAR_ADD, 6)
        buf[0] += 2000
        return tuple(buf)
    def set_rtc(self, year, month, day, hour, minute, second):
        """Set rtc time.

        Args:
            year (int): current year
            month (int): current month
            day (int): current day
            hour (int): current hour
            minute (int): current minute
            second (int): current second
        """
        if year > 2000:
            year -= 2000
        if(not(0 <= year and year <= 255)):
            raise ValueError("Invalid year!")
        datetime.datetime(
                year=2000+year, month=month, day=day,
                hour=hour, minute=minute, second=second)
        ba = bytearray(struct.pack(
            "6B B",
            year, month, day, hour, minute, second,
            data.CALIBRATION_KEY))
        self._set_block(I2C_MEM.RTC_SET_YEAR_ADD, ba)
    def get_opto(self, channel):
        """Get optocoupled input status. 

        Args:
            channel (int): Channel number

        Returns:
            (bool) Channel status
        """
        self._check_channel("opto", channel)
        opto_mask = self._get_byte(I2C_MEM.OPTO)
        if(opto_mask & (1 << (channel - 1))):
            return True
        else:
            return False
    def get_all_opto(self):
        """Get all optocoupled input status as a bitmask.

        Returns:
            (int) Optocoupled bitmask
        """
        return self._get_byte(I2C_MEM.OPTO)
    def get_opto_edge(self, channel):
        """Get optocoupled channel counting edges status.

        Args:
            channel (int): Channel number

        Returns:
            (int) Counting edge status
                0(none)/1(rising)/2(falling)/3(both)
        """
        self._check_channel("opto", channel)
        rising = self._get_byte(I2C_MEM.OPTO_IT_RISING_ADD)
        falling = self._get_byte(I2C_MEM.OPTO_IT_FALLING_ADD)
        channel_bit = 1 << (channel - 1)
        value = 0
        if(rising & channel_bit):
            value |= 1
        if(falling & channel_bit):
            value |= 2
        return value
    def set_opto_edge(self, channel, value):
        """Set optocoupled channel counting edges status.

        Args:
            channel (int): Channel number
            value (int): Counting edge status
                0(none)/1(rising)/2(falling)/3(both)
        """
        self._check_channel("opto", channel)
        rising = self._get_byte(I2C_MEM.OPTO_IT_RISING_ADD)
        falling = self._get_byte(I2C_MEM.OPTO_IT_FALLING_ADD)
        channel_bit = 1 << (channel - 1)
        if(value & 1):
            rising |= channel_bit
        else:
            rising &= ~channel_bit
        if(value & 2):
            falling |= channel_bit
        else:
            rising &= ~channel_bit
        self._set_byte(I2C_MEM.OPTO_IT_RISING_ADD, rising)
        self._set_byte(I2C_MEM.OPTO_IT_FALLING_ADD, falling)
    def get_opto_counter(self, channel):
        """Get optocoupled inputs edges counter for one channel.

        Args:
            channel (int): Channel number

        Returns:
            (int) opto counter
        """
        self._check_channel("opto", channel)
        return self._get_u32(I2C_MEM.OPTO_EDGE_COUNT_ADD + (channel - 1) * 4)
    def reset_opto_counter(self, channel):
        """Reset optocoupled inputs edges counter.

        Args:
            channel (int): Channel number
        """
        self._check_channel("opto", channel)
        return self._set_byte(I2C_MEM.OPTO_CNT_RST_ADD, channel)
    def get_opto_encoder_state(self, channel):
        """Get optocoupled quadrature encoder state.

        Args:
            channel (int): Encoded channel number

        Returns:
            (int) state 0(disabled)/1(enabled)
        """
        self._check_channel("opto_enc", channel)
        encoder_mask = self._get_byte(I2C_MEM.OPTO_ENC_ENABLE_ADD)
        channel_bit = 1 << (channel - 1)
        if(encoder_mask & channel_bit):
            return True
        else:
            return False
    def set_opto_encoder_state(self, channel, state):
        """Set optocoupled quadrature encoder state.

        Args:
            channel (int): Encoded channel number
            state (int): 0(disabled)/1(enabled)
        """
        self._check_channel("opto_enc", channel)
        encoder_mask = self._get_byte(I2C_MEM.OPTO_ENC_ENABLE_ADD)
        channel_bit = 1 << (channel - 1)
        if(state == 1):
            encoder_mask |= channel_bit
        elif(state == 0):
            encoder_mask &= ~channel_bit
        else:
            raise ValueError("Invalid value! Must be 0 or 1!")
        self._set_byte(I2C_MEM.OPTO_ENC_ENABLE_ADD, encoder_mask)
    def get_opto_encoder_counter(self, channel):
        """Get optocoupled encoder counter for one channel.

        Args:
            channel (int): Channel number

        Returns:
            (int) Opto encoder counter
        """
        self._check_channel("opto_enc", channel)
        return self._get_i32(I2C_MEM.OPTO_ENC_COUNT_ADD + (channel - 1) * 4)
    def reset_opto_encoder_counter(self, channel):
        """Reset optocoupled encoder counter for one channel.

        Args:
            channel (int): Channel number
        """
        self._check_channel("opto_enc", channel)
        self._set_byte(I2C_MEM.OPTO_ENC_CNT_RST_ADD, channel)

    def get_servo(self, channel):
        """Get servo position value in %.

        Args:
            channel (int): Channel number

        Returns:
            (float) Servo position value in % for specified channel.
        """
        self._check_channel("servo", channel)
        return self._get_i16(I2C_MEM.SERVO_VAL1 + (channel - 1) * 2) / 10
    def set_servo(self, channel, value):
        """Set servo position value in %.

        Args:
            channel (int): Channel number
            value (float): Servo position value in %
        """
        self._check_channel("servo", channel)
        if(not(-140 <= value and value <= 140)):
            raise ValueError("Servo value out of range! Must be [-140..140]")
        self._set_word(I2C_MEM.SERVO_VAL1 + (channel - 1) * 2, value * 10)

    def get_motor(self):
        """Get motor speed value in %.

        Returns:
            (float) Motor speed value in %
        """
        return self._get_word(I2C_MEM.MOT_VAL / 10)
    def set_motor(self, value):
        """Set motor speed value in %.

        Args:
            value (float): Speed value in %
        """
        if(not(-100 <= value and value <= 100)):
            raise ValueError("Motor value out of range! Must be [-100..100]")
        self._set_word(I2C_MEM.MOT_VAL, value * 10)

    def get_button(self):
        """Get button status.

        Returns:
            (bool) status
                True(ON)/False(OFF)
        """
        state = self._get_byte(I2C_MEM.BUTTON)
        if(state & 1):
            return True
        else:
            return False
    def get_button_latch(self):
        """Get button latch status.

        Returns:
            (bool) status
                True(ON)/False(OFF)
        """
        state = self._get_byte(I2C_MEM.BUTTON)
        if(state & 2):
            state &= ~2
            self._set_byte(I2C_MEM.BUTTON, state)
            return True
        else:
            return False
