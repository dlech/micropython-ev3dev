"""LED module"""

try:
    import uerrno
except:
    import errno as uerrno

from uev3dev import sysfs
from uev3dev import util


def _led(name, color):
    try:
        path = '/sys/class/leds/{0}:{1}:brick-status'.format(name, color)
        led = {}
        led['trigger'] = sysfs.IntAttribute(path, 'trigger', 'r+')
        led['brightness'] = sysfs.IntAttribute(path, 'brightness', 'r+')
        led['max'] = sysfs.IntAttribute(path, 'max_brightness', 'r').read()
        return led
    except OSError as e:
        if e.args[0] == uerrno.ENOENT:
            return None
        raise


class LEDNotFoundError(Exception):
    """Exception that raised when an LED is not found"""
    def __init__(self, message):
        super(LEDNotFoundError, self).__init__(message)


LEDPattern = util.enum(OFF='none', ON='default-on', FLASH='heartbeat')
"""LED blink patterns"""

LEDName = util.enum(LED0='led0', LED1='led1')
"""Common LED names"""


LEDColor = util.enum(
    RED=(255, 0, 0),
    GREEN=(0, 255, 0),
    BLUE=(0, 0, 255),
    YELLOW=(255, 255, 0),
    CYAN=(0, 255, 255),
    MAGENTA=(255, 0, 255),
    BLACK=(0, 0, 0),
    WHITE=(255, 255, 255))
"""Common LED Colors

.. note: not all LEDs support all colors. For example, LEGO MINDSTORMS EV3 only
    has red and green (which can combine to make yellow).
"""


class LED():
    """Object that represents an LED"""

    def __init__(self, name):
        """Create a new instace of an LED.

        :param LEDName name: The name of the LED.
        """

        self._red = _led(name, 'red')
        self._green = _led(name, 'green')
        self._blue = _led(name, 'blue')

        if not self._red and not self._green and not self._blue:
            raise LEDNotFoundError('Could not find ' + name)

    def pattern(self, name, color=LEDColor.WHITE):
        """Sets the LED blink pattern.

        :param LEDPattern name: The pattern.
        :param tuple color: A tuple of RGB values.
        """

        def _scale(color, max):
            return int(color * max / 255)

        if name == LEDPattern.OFF:
            # the 'none' trigger doesn't turn LEDs off, so we have to use
            # the brightness value for that.
            color = LEDColor.BLACK

        if self._red:
            self._red['trigger'].write(name)
            self._red['brightness'].write(_scale(color[0], self._red['max']))
        if self._green:
            self._green['trigger'].write(name)
            self._green['brightness'].write(_scale(color[1], self._green['max']))
        if self._blue:
            self._blue['trigger'].write(name)
            self._blue['brightness'].write(_scale(color[2], self._blue['max']))


class StatusLight():
    def __init__(self):
        self._led0 = LED('led0')
        self._led1 = LED('led1')

    def off(self):
        self._led0.pattern(LEDPattern.OFF)
        self._led1.pattern(LEDPattern.OFF)
