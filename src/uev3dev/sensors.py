"""Sensors"""

from uev3dev import sysfs
from uev3dev import util


InputPort = util.enum(N1='ev3-ports:in1', N2='ev3-ports:in2',
                      N3='ev3-ports:in3', N4='ev3-ports:in4')


class SensorNotFoundError(Exception):
    """Exception thrown when a sensor is not found"""
    def __init__(self, name, port):
        msg = name + ' not found on port ' + port
        super(SensorNotFoundError, self).__init__(msg)


class Sensor():
    """Object that represents a sensor."""

    def __init__(self, port, driver):
        node = sysfs.find_node('lego-sensor', port, driver)
        if not node:
            raise SensorNotFoundError(self.__class__.__name__, port)

        try:
            self._command = sysfs.Attribute(node, 'command', 'w')
            self._commands = sysfs.Attribute(node, 'commands', 'r').read().split(' ')
        except OSError:
            # some sensors do no support commands
            pass

        self._decimals = sysfs.IntAttribute(node, 'decimals', 'r')
        self._mode = sysfs.Attribute(node, 'mode', 'r+')
        self._modes = sysfs.Attribute(node, 'modes', 'r').read().split(' ')
        self._num_values = sysfs.IntAttribute(node, 'num_values', 'r')
        self._units = sysfs.Attribute(node, 'units', 'r')
        self._value = (sysfs.IntAttribute(node, 'value0', 'r'),
                       sysfs.IntAttribute(node, 'value1', 'r'),
                       sysfs.IntAttribute(node, 'value2', 'r'),
                       sysfs.IntAttribute(node, 'value3', 'r'),
                       sysfs.IntAttribute(node, 'value4', 'r'),
                       sysfs.IntAttribute(node, 'value5', 'r'),
                       sysfs.IntAttribute(node, 'value6', 'r'),
                       sysfs.IntAttribute(node, 'value7', 'r'))
        self._cached_decimals = None
        self._cached_num_values = None
        self._cached_units = None

    @property
    def units(self):
        """Gets the units of measurement for the current mode.

        :returns str: The units.
        """
        if self._cached_units is None:
            self._cached_units = self._units.read()
        return self._cached_units

    @property
    def num_values(self):
        """Gets the number of data values for the current mode.

        :returns str: The number of values.
        """
        if self._cached_num_values is None:
            self._cached_num_values = self._num_values.read()
        return self._cached_num_values

    @property
    def _decimals_(self):
        if self._cached_decimals is None:
            self._cached_decimals = self._decimals.read()
        return self._cached_decimals

    def set_mode(self, mode):
        """Sets the mode of the sensor.

        :param str mode: The name of the mode.
        """
        if mode not in self._modes:
            raise ValueError('Invalid mode: ' + mode)
        self._mode.write(mode)
        self._cached_decimals = None
        self._cached_num_values = None
        self._cached_units = None

    def value(self, index):
        """Gets a sensor data value.

        :param int index: The index of the value (0 to 7).
        :returns: the value read
        """
        if index < 0 or index >= self.num_values:
            raise ValueError('Index is out of range')
        value = self._value[index].read()
        decimals = self._decimals_
        if decimals:
            value /= 10 ** decimals
            value = round(value, decimals)
        return value


class Ev3ColorSensor(Sensor):
    """Object that represents a LEGO EV3 Color sensor"""

    _COLORS = (None, 'black', 'blue', 'green', 'yellow', 'red', 'white',
               'brown')

    def __init__(self, port):
        """Create a new instance of a color sensor.

        :param InputPort port: The input port the sensor is connected to.
        """
        super(Ev3ColorSensor, self).__init__(port, 'lego-ev3-color')
        self._current_mode = self._modes.index(self._mode.read())

    def read_reflected(self):
        """Reads the current reflected light value of the sensor.

        Also has the effect of setting the LED to red.

        :return int: A percentage value.
        """
        if self._current_mode != self._modes[0]:
            self.set_mode(self._modes[0])
        return self.value(0)

    def read_ambient(self):
        """Reads the current ambient light value of the sensor.

        Also has the effect of setting the LED to dim blue.

        :return int: A percentage value.
        """
        if self._current_mode != self._modes[1]:
            self.set_mode(self._modes[1])
        return self.value(0)

    def read_color(self):
        """Reads the current color value from the sensor.

        Also has the effect of setting the LED to white.

        :return str: One of None, 'black', 'blue', 'green', 'yellow', 'red',
            'white', or 'brown'
        """
        if self._current_mode != self._modes[2]:
            self.set_mode(self._modes[2])
        return self._COLORS[int(self.value(0))]

    def read_raw_rgb(self):
        """Reads the current raw red, green, and blue reflected light values.

        Also has the effect of setting the LED to white.

        :return int, int, int: the red, green, and blue component values.
        """
        if self._current_mode != self._modes[4]:
            self.set_mode(self._modes[4])
        return self.value(0), self.value(1), self.value(2)


class Ev3UltrasonicSensor(Sensor):
    """Object that represents the LEGO EV3 Ultrasonic Sensor"""
    def __init__(self, port):
        """Create a new instance of an ultrasonic sensor.

        :param InputPort port: The input port the sensor is connected to.
        """
        super(Ev3UltrasonicSensor, self).__init__(port, 'lego-ev3-us')
        self._current_mode = self._modes.index(self._mode.read())

    def read_cm(self):
        """Reads the current distance measured by the sensor in centimeters.

        Also has the effect of setting the LED to red.

        :return float: The distance.
        """
        if self._current_mode != self._modes[0]:
            self.set_mode(self._modes[0])
        return self.value(0)

    def read_in(self):
        """Reads the current distance measured by the sensor in inches.

        Also has the effect of setting the LED to red.

        :return float: The distance.
        """
        if self._current_mode != self._modes[1]:
            self.set_mode(self._modes[1])
        return self.value(0)

    def listen(self):
        """Reads the current distance measured by the sensor in inches.

        Also has the effect making the LED blink red.

        :return bool: ``True`` if another ultrasonic sensor was detected,
            otherwise ``False``.
        """
        if self._current_mode != self._modes[2]:
            self.set_mode(self._modes[2])
        return bool(self.value(0))
