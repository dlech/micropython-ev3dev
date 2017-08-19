"""Motors"""

import uev3dev.sysfs as sysfs
import uev3dev.util as util

OutputPort = util.enum(A='ev3-ports:outA', B='ev3-ports:outB',
                       C='ev3-ports:outC', D='ev3-ports:outD')

StopAction = util.enum(COAST='coast', BRAKE='brake', HOLD='hold')


class MotorNotFoundError(Exception):
    """Exception thrown when a motor is not found"""
    def __init__(self, name, port):
        msg = name + ' not found on port ' + port
        super(MotorNotFoundError, self).__init__(msg)


class TachoMotor():
    """Object that represents a motor with position feedback."""

    EV3_LARGE = 'lego-ev3-l-motor'
    """LEGO EV3 Large Motor"""

    EV3_MEDIUM = 'lego-ev3-m-motor'
    """LEGO EV3 Medium Motor"""

    def __init__(self, port, driver):
        node = sysfs.find_node('tacho-motor', port, driver)
        if not node:
            raise MotorNotFoundError(self.__class__.__name__, port)
        self._command = sysfs.Attribute(node, 'command', 'w')
        self._commands = sysfs.Attribute(node, 'commands', 'r').read().split(' ')
        self._count_per_rot = sysfs.IntAttribute(node, 'count_per_rot', 'r').read()
        self._driver_name = sysfs.Attribute(node, 'driver_name', 'r').read()
        self._duty_cycle = sysfs.IntAttribute(node, 'duty_cycle', 'r')
        self._duty_cycle_sp = sysfs.IntAttribute(node, 'duty_cycle_sp', 'r+')
        self._max_speed = sysfs.IntAttribute(node, 'max_speed', 'r').read()
        self._position = sysfs.IntAttribute(node, 'position', 'r')
        self._position_sp = sysfs.IntAttribute(node, 'position_sp', 'r+')
        self._speed_sp = sysfs.IntAttribute(node, 'speed_sp', 'r+')
        self._state = sysfs.Attribute(node, 'state', 'r')
        self._stop_action = sysfs.Attribute(node, 'stop_action', 'r+')
        self._stop_actions = sysfs.Attribute(node, 'stop_actions', 'r').read().split(' ')
        self._time_sp = sysfs.IntAttribute(node, 'time_sp', 'r+')
        self.port = port
        self.reset()

    @property
    def max_speed(self):
        """Gets the maximum speed of the motor under ideal conditions (no
        load at 9V).

        The actual obtainable maximum speed will depend on the load of the
        motor and battery voltage.

        :return int: the speed in degrees/second
        """
        return self._count_per_rot * 360 / self._max_speed

    def run_regulated(self, speed):
        """Run the motor at the specified speed.

        The motor will continue to run at this speed until another command is
        given.

        :param int speed: The target speed in degrees/second
        """
        self._set_speed_sp(int(speed * self._count_per_rot / 360))
        self._command.write('run-forever')

    def run_unregulated(self, duty_cycle):
        """Run the motor using the specified duty cycle.

        The motor will continue to run with this duty cycle another command is
        given.

        :param int duty_cycle: the duty cycle, -100 to 100 percent
        """
        self._set_duty_cycle_sp(duty_cycle)
        self._command.write('run-direct')

    def run_timed(self, speed, time, stop_action=StopAction.COAST):
        """Run the motor at the target speed for a fixed duration.

        The motor will run until the time expires or another command is given.

        :param int speed: The target speed in degrees/second.
        :param float time: The time for the motor to run in seconds.
        :param StopAction stop_action: The stop action to perform at the end
            of the time period.
        """
        self._set_speed_sp(int(speed * self._count_per_rot / 360))
        self._set_time_sp(int(time * 1000))
        self._set_stop_action(stop_action)
        self._command.write('run-timed')

    def stop(self, action=StopAction.COAST):
        self._set_stop_action(action)
        self._command.write('stop')

    def reset(self):
        self._command.write('reset')

    def _set_duty_cycle_sp(self, duty_cycle):
        if duty_cycle < -100 or duty_cycle > 100:
            raise ValueError('duty cycle is out of range')
        self._duty_cycle_sp.write(duty_cycle)

    def _set_speed_sp(self, speed):
        if speed < -self._max_speed or speed > self._max_speed:
            raise ValueError('speed is out of range')
        self._speed_sp.write(speed)

    def _set_time_sp(self, time):
        if time < 0:
            raise ValueError('time is out of range')
        self._time_sp.write(time)

    def _set_stop_action(self, action):
        if action not in self._stop_actions:
            raise ValueError('Invalid stop action')
        self._stop_action.write(action)


class LargeMotor(TachoMotor):
    """Object that represents a LEGO EV3 Large motor."""

    def __init__(self, port):
        """Create a new instace of a large motor.

        :param OutputPort port: The output port the motor is connected to.
        """
        super(LargeMotor, self).__init__(port, TachoMotor.EV3_LARGE)


class MediumMotor(TachoMotor):
    """Object that represents a LEGO EV3 Medium motor."""

    def __init__(self, port):
        """Create a new instace of a medium motor.

        :param OutputPort port: The output port the motor is connected to.
        """
        super(MediumMotor, self).__init__(port, TachoMotor.EV3_MEDIUM)
