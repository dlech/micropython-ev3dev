"""LED module"""

from errno import ENOENT

from uev3dev._sysfs import IntAttribute
from uev3dev.util import Timeout


def _led(name, color):
    try:
        path = '/sys/class/leds/{0}:{1}:brick-status'.format(name, color)
        led = {}
        led['trigger'] = IntAttribute(path, 'trigger', 'r+')
        led['brightness'] = IntAttribute(path, 'brightness', 'r+')
        led['max'] = IntAttribute(path, 'max_brightness', 'r').read()
        return led
    except OSError as e:
        if e.args[0] == ENOENT:
            return None
        raise


class LEDNotFoundError(Exception):
    """Exception that raised when an LED is not found"""
    def __init__(self, message):
        super(LEDNotFoundError, self).__init__(message)


class _LED():
    """Object that represents an LED"""

    def __init__(self, name):
        """Create a new instace of an LED.

        Parameters:
            name (str): The name of the LED.
        """

        self._red = _led(name, 'red')
        self._green = _led(name, 'green')
        self._blue = _led(name, 'blue')

        if not any((self._red, self._green, self._blue)):
            raise LEDNotFoundError('Could not find ' + name)

    def set_brightness(self, rgb):
        """Sets the brightness

        Parameters:
            r: the red component
            g: the green component
            b: the blue component
        """

        def _scale(color, max):
            return int(color * max / 255)

        if self._red:
            self._red['trigger'].write('none')
            self._red['brightness'].write(_scale(rgb[0], self._red['max']))
        if self._green:
            self._green['trigger'].write('none')
            self._green['brightness'].write(_scale(rgb[1], self._green['max']))
        if self._blue:
            self._blue['trigger'].write('none')
            self._blue['brightness'].write(_scale(rgb[2], self._blue['max']))


class Color():
    """Colors to use in :py:meth:`StatusLight.on`"""
    GREEN = 0
    ORANGE = 1
    RED = 2

_COLOR_MAP = {
    Color.GREEN: (0, 255, 0),
    Color.ORANGE: (255, 255, 0),
    Color.RED: (255, 0, 0),
}


class StatusLight():
    """Object that represents the brick status light"""
    def __init__(self):
        self._leds = (_LED('led0'), _LED('led1'))
        self._timeout = Timeout(0, self._pulse, True)
        self._pulse_state = 0
        self._pulse_color = None

    def _off(self):
        for l in self._leds:
            l.set_brightness((0, 0, 0))

    def off(self):
        """Turn the lights off"""
        self._timeout.cancel()
        self._off()

    def _on(self, color):
        rgb = _COLOR_MAP[color]
        for l in self._leds:
            l.set_brightness(rgb)

    def on(self, color, pulse):
        """Turn the lights on

        Parameters:
            color (Color): The color
            pulse (bool): When ``True`` the lights will blink
        """
        if pulse:
            self._pulse_color = color
            self._timeout._interval = 0
            self._timeout.start()
        else:
            self._on(color)

    def _pulse(self):
        if self._pulse_state == 0:
            self._on(self._pulse_color)
            self._timeout._interval = 0.1
        elif self._pulse_state == 1:
            self._off()
            self._timeout._interval = 0.1
        elif self._pulse_state == 2:
            self._on(self._pulse_color)
            self._timeout._interval = 0.1
        elif self._pulse_state == 3:
            self._off()
            self._timeout._interval = 0.3
        self._pulse_state += 1
        if self._pulse_state >= 4:
            self._pulse_state = 0
