

from uev3dev._sysfs import find_node
from uev3dev._sysfs import Attribute
from uev3dev._sysfs import ListAttribute


class PortNotFoundError(Exception):
    """Exception thrown when a port is not found"""
    def __init__(self, name, port):
        msg = name + ' not found on port ' + port
        super(PortNotFoundError, self).__init__(msg)


class Port():
    """Object that represents a port.
    """

    def __init__(self, port, driver):
        """Create a new instance of a port.

        :param string port: The name of the port.
        :param string driver: The name of the kernel driver.
        """
        node = find_node('lego-port', port, driver)
        if not node:
            raise PortNotFoundError(self.__class__.__name__, port)
        self._mode = Attribute(node, 'mode', 'r+')
        self._modes = ListAttribute(node, 'modes', 'r').read()
        self._set_device = Attribute(node, 'set_device', 'w')
        self._status = Attribute(node, 'status', 'r')

    @property
    def status(self):
        """Gets the current status of the port."""
        return self._status.read()

    def _get_mode(self):
        """Gets or sets the current mode of the port."""
        return self._mode.read()

    def _set_mode(self, mode):
        if mode not in self._modes:
            raise ValueError('Invalid mode')
        self._mode.write(mode)

    mode = property(_get_mode, _set_mode)
    """Gets or sets the current mode of the port."""

    @property
    def modes(self):
        """Get a list of modes supported by this port."""
        return self._modes

    def set_device(self, driver):
        """Sets the device attached to the port.

        This only works for certain modes. Consult the driver documentation
        for your device.

        :param string driver: The name of the kernel driver.
        """
        self._set_device.write(driver)


class EV3InputPort(Port):
    """Object that represents an EV3 input port.
    """

    def __init__(self, port):
        """Create a new instance of a port.

        :param string port: The name of the port.
        """
        if len(port) == 1:
            port = 'ev3-ports:in' + port
        super(EV3InputPort, self).__init__(port, 'ev3-input-port')


class EV3OutputPort(Port):
    """Object that represents an EV3 output port.
    """

    def __init__(self, port):
        """Create a new instance of a port.

        :param string port: The name of the port.
        """
        if len(port) == 1:
            port = 'ev3-ports:out' + port
        super(EV3OutputPort, self).__init__(port, 'ev3-output-port')
