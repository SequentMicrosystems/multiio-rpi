# Welcome to multiio’s documentation!

# Install

```bash
sudo pip install multiio
```

or

```bash
sudo pip3 install multiio
```

# Update

```bash
sudo pip install multiio -U
```

or

```bash
sudo pip3 install multiio -U
```

# Initiate class

```console
$ python
Python 3.9.2 (default, Feb 28 2021, 17:03:44)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import multiio.SMmultiio as m
>>> multiio = m()
>>>
```

# Documentation

<a id="module-multiio"></a>

### *class* multiio.SMmultiio(stack=0, i2c=1)

Bases: `object`

Python class to control the Multiio Card for Raspberry Pi.

* **Parameters:**
  * **stack** (*int*) – Stack level/device number.
  * **i2c** (*int*) – i2c bus number

#### cal_i_in(channel, value)

Calibrate 4-20mA input channel.
Calibration must be done in 2 points at min 10mA apart.

* **Parameters:**
  * **channel** (*int*) – Channel number
  * **value** (*float*) – Real(measured) amperage value

#### cal_i_out(channel, value)

Calibrate 4-20mA output channel.
Calibration must be done in 2 points at min 10mA apart.

* **Parameters:**
  * **channel** (*int*) – Channel number
  * **value** (*float*) – Real(measured) amperage value

#### cal_rtd_res(channel, value)

Calibrate rtd resistance.

* **Parameters:**
  * **channel** (*int*) – RTD channel number to calibrate
  * **value** (*float*) – Real(measured) resistance in ohm

#### cal_u_in(channel, value)

Calibrate 0-10V input channel.
Calibration must be done in 2 points at min 5V apart.

* **Parameters:**
  * **channel** (*int*) – Channel number
  * **value** (*int*) – Voltage value

#### cal_u_out(channel, value)

Calibrate 0-10V output channel.
Calibration must be done in 2 points at min 5V apart.

* **Parameters:**
  * **channel** (*int*) – Channel number
  * **value** (*float*) – Real(measured) voltage value

#### calib_status()

Get current calibration status of device.

* **Returns:**
  (int) Calib status

#### get_all_leds()

Get all leds state as bitmask.

* **Returns:**
  (int) Leds state bitmask

#### get_all_opto()

Get all optocoupled input status as a bitmask.

* **Returns:**
  (int) Optocoupled bitmask

#### get_all_relays()

Get all relays state as bitmask.

* **Returns:**
  (int) Relays state bitmask

#### get_button()

Get button status.

* **Returns:**
  (bool) status
  : True(ON)/False(OFF)

#### get_button_latch()

Get button latch status.

* **Returns:**
  (bool) status
  : True(ON)/False(OFF)

#### get_i_in(channel)

Get 4-20mA input channel value in mA.

* **Parameters:**
  **channel** (*int*) – Channel number
* **Returns:**
  (float) 4-20mA input channel value in mA

#### get_i_out(channel)

Get 4-20mA output channel value in mA.

* **Parameters:**
  **channel** (*int*) – Channel number
* **Returns:**
  (float) 4-20mA output value in mA

#### get_led(led)

Get led state.

* **Parameters:**
  **led** (*int*) – Led number
* **Returns:**
  0(OFF) or 1(ON)

#### get_motor()

Get motor speed value in %.

* **Returns:**
  (float) Motor speed value in %

#### get_opto(channel)

Get optocoupled input status.

* **Parameters:**
  **channel** (*int*) – Channel number
* **Returns:**
  (bool) Channel status

#### get_opto_counter(channel)

Get optocoupled inputs edges counter for one channel.

* **Parameters:**
  **channel** (*int*) – Channel number
* **Returns:**
  (int) opto counter

#### get_opto_edge(channel)

Get optocoupled channel counting edges status.

* **Parameters:**
  **channel** (*int*) – Channel number
* **Returns:**
  (int) Counting edge status
  : 0(none)/1(rising)/2(falling)/3(both)

#### get_opto_encoder_counter(channel)

Get optocoupled encoder counter for one channel.

* **Parameters:**
  **channel** (*int*) – Channel number
* **Returns:**
  (int) Opto encoder counter

#### get_opto_encoder_state(channel)

Get optocoupled quadrature encoder state.

* **Parameters:**
  **channel** (*int*) – Encoded channel number
* **Returns:**
  (int) state 0(disabled)/1(enabled)

#### get_relay(relay)

Get relay state.

* **Parameters:**
  **relay** (*int*) – Relay number
* **Returns:**
  (int) Relay state

#### get_rtc()

Get rtc time.

* **Returns:**
  (tuple) date(year, month, day, hour, minute, second)

#### get_rtd_res(channel)

Get RTD resistance in ohm.

* **Parameters:**
  **channel** (*int*) – RTD channel number
* **Returns:**
  (float) RTD resistance value

#### get_rtd_temp(channel)

Get RTD temperature in Celsius.

* **Parameters:**
  **channel** (*int*) – RTD channel number
* **Returns:**
  (float) RTD Celsius value

#### get_servo(channel)

Get servo position value in %.

* **Parameters:**
  **channel** (*int*) – Channel number
* **Returns:**
  (float) Servo position value in % for specified channel.

#### get_u_in(channel)

Get 0-10V input channel value in volts.

* **Parameters:**
  **channel** (*int*) – Channel number
* **Returns:**
  (float) Input value in volts

#### get_u_out(channel)

Get 0-10V output channel value in volts.

* **Parameters:**
  **channel** (*int*) – Channel number
* **Returns:**
  (float) 0-10V output value

#### get_version()

Get firmware version.

Returns: (int) Firmware version number

#### reset_opto_counter(channel)

Reset optocoupled inputs edges counter.

* **Parameters:**
  **channel** (*int*) – Channel number

#### reset_opto_encoder_counter(channel)

Reset optocoupled encoder counter for one channel.

* **Parameters:**
  **channel** (*int*) – Channel number

#### set_all_leds(val)

Set all leds states as bitmask.

* **Parameters:**
  **val** (*int*) – Led bitmask

#### set_all_relays(val)

Set all relays states as bitmask.

* **Parameters:**
  **val** (*int*) – Relay bitmask

#### set_i_out(channel, value)

Set 4-20mA output channel value in mA.

* **Parameters:**
  * **channel** (*int*) – Channel number
  * **value** (*float*) – Amperage value in mA

#### set_led(led, val)

Set led state.

* **Parameters:**
  * **led** (*int*) – Led number
  * **val** – 0(OFF) or 1(ON)

#### set_motor(value)

Set motor speed value in %.

* **Parameters:**
  **value** (*float*) – Speed value in %

#### set_opto_edge(channel, value)

Set optocoupled channel counting edges status.

* **Parameters:**
  * **channel** (*int*) – Channel number
  * **value** (*int*) – Counting edge status
    0(none)/1(rising)/2(falling)/3(both)

#### set_opto_encoder_state(channel, state)

Set optocoupled quadrature encoder state.

* **Parameters:**
  * **channel** (*int*) – Encoded channel number
  * **state** (*int*) – 0(disabled)/1(enabled)

#### set_relay(relay, val)

Set relay state.

* **Parameters:**
  * **relay** (*int*) – Relay number
  * **val** – 0(OFF) or 1(ON)

#### set_rtc(year, month, day, hour, minute, second)

Set rtc time.

* **Parameters:**
  * **year** (*int*) – current year
  * **month** (*int*) – current month
  * **day** (*int*) – current day
  * **hour** (*int*) – current hour
  * **minute** (*int*) – current minute
  * **second** (*int*) – current second

#### set_servo(channel, value)

Set servo position value in %.

* **Parameters:**
  * **channel** (*int*) – Channel number
  * **value** (*float*) – Servo position value in %

#### set_u_out(channel, value)

Set 0-10V output channel value in volts.

* **Parameters:**
  * **channel** (*int*) – Channel number
  * **value** (*float*) – Voltage value

#### wdt_clear_reset_count()

Clear watchdog counter.

#### wdt_get_init_period()

Get watchdog initial period.

* **Returns:**
  (int) Initial watchdog period in seconds

#### wdt_get_off_period()

Get watchdog off period in seconds.

* **Returns:**
  (int) Watchfog off period in seconds.

#### wdt_get_period()

Get watchdog period in seconds.

* **Returns:**
  (int) Watchdog period in seconds

#### wdt_get_reset_count()

Get watchdog reset count.

* **Returns:**
  (int) Watchdog reset count

#### wdt_reload()

Reload watchdog.

#### wdt_set_init_period(period)

Set watchdog initial period.

* **Parameters:**
  **period** (*int*) – Initial period in second

#### wdt_set_off_period(period)

Set off period in seconds

* **Parameters:**
  **period** (*int*) – Off period in seconds

#### wdt_set_period(period)

Set watchdog period.

* **Parameters:**
  **period** (*int*) – Channel number

<!-- vi:se ts=4 sw=4 et: -->
