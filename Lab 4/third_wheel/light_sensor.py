"""
Reads overall room brightness from the APDS-9960 and smooths it.

The sensor reports red, green, blue and "clear" channels. Clear is the
total amount of light hitting it, which is all we need to tell whether
the lights have been dimmed.
"""

import time
from collections import deque

import board
from adafruit_apds9960.apds9960 import APDS9960

import config


class LightSensor:
    def __init__(self, window=config.SMOOTHING_WINDOW):
        try:
            self.apds = APDS9960(board.I2C())
        except (ValueError, RuntimeError, OSError) as err:
            raise RuntimeError(
                "Couldn't find the APDS-9960 light sensor (I2C address 0x39). "
                "Check its Qwiic cable, then run: i2cdetect -y 1"
            ) from err

        self.apds.enable_color = True
        self.apds.color_gain = config.COLOR_GAIN
        self.apds.color_integration_time = config.INTEGRATION_TIME

        # Highest value the sensor can report at this integration time.
        self.max_count = min(65535, 1024 * config.INTEGRATION_TIME + 1)
        self.readings = deque(maxlen=window)

    def read_raw(self):
        """Wait for a fresh measurement and return the clear (brightness) value."""
        while not self.apds.color_data_ready:
            time.sleep(0.005)
        _, _, _, clear = self.apds.color_data
        return clear

    def update(self):
        """Take one reading, add it to the smoothing window, and return it."""
        value = self.read_raw()
        self.readings.append(value)
        return value

    def reset(self):
        """Forget old readings, e.g. after the figure moves and changes the shadows."""
        self.readings.clear()

    @property
    def average(self):
        if not self.readings:
            return 0.0
        return sum(self.readings) / len(self.readings)

    @property
    def is_ready(self):
        """True once the window is full, so one odd reading can't trigger a turn."""
        return len(self.readings) == self.readings.maxlen

    def is_saturated(self, value):
        return value >= self.max_count
