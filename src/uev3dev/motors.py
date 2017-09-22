"""Motors"""

try:
    import utime
except:
    import time as utime

import uev3dev.sysfs as sysfs
import uev3dev.util as util

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
        if len(port) == 1:
            port = 'ev3-ports:out' + port
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
        self._ramp_up_sp = sysfs.IntAttribute(node, 'ramp_up_sp', 'r+')
        self._ramp_down_sp = sysfs.IntAttribute(node, 'ramp_down_sp', 'r+')
        self._speed_sp = sysfs.IntAttribute(node, 'speed_sp', 'r+')
        self._state = sysfs.Attribute(node, 'state', 'r')
        self._stop_action = sysfs.Attribute(node, 'stop_action', 'r+')
        self._stop_actions = sysfs.Attribute(node, 'stop_actions', 'r').read().split(' ')
        self._time_sp = sysfs.IntAttribute(node, 'time_sp', 'r+')
        self.port = port
        self.RPM = 100 * self._max_speed / self._count_per_rot / 60
        self.DPS = self.RPM / 6
        self._command.write('reset')
        # ramping seems to be broken in the kernel drivers
        # self._ramp_up_sp.write(100)
        # self._ramp_down_sp.write(100)

    def run(self, speed):
        """Run the motor at the specified speed.

        The motor will continue to run at this speed until another command is
        given.

        :param int speed: The target speed in percent [-100..100].
        """
        self._set_speed_sp(speed)
        self._command.write('run-forever')

    def on_for_degrees(self, speed, degrees, brake=True, wait=True):
        """Run the motor at the target speed for the specified number of
        degrees.

        The motor will run until the new position is reached or another command
        is given.

        Parameters:
            speed (int): The target speed in percent [-100..100].
            degrees (int): The number of degrees to turn the motor.
            brake (bool): ``True`` cases the motor to hold it's position when
                          when it is reached. ``False`` will let the motor
                          coast to a stop.
            wait (bool): When ``True``, this method will not return until the
                         time has run out. When ``False`` this method will
                         return immediately.
        """
        # driver uses absolute value of speed, so we have to invert degrees
        # to make it work as expected
        if speed < 0:
            degrees *= -1
        if brake:
            stop_action = StopAction.HOLD
        else:
            stop_action = StopAction.COAST
        self._set_speed_sp(speed)
        self._set_stop_action(stop_action)
        self._set_position_sp(degrees)
        self._command.write('run-to-rel-pos')
        while wait:
            state = self._state.read().split(' ')
            if 'running' not in state or 'holding' in state:
                wait = False

    def on_for_rotations(self, speed, rotations, brake=True, wait=True):
        """Run the motor at the target speed for the specified number of
        rotations.

        The motor will run until the new position is reached or another command
        is given.

        Parameters:
            speed (int): The target speed in percent [-100..100].
            rotations (float): The number of rotations to turn the motor.
            brake (bool): ``True`` cases the motor to hold it's position when
                          when it is reached. ``False`` will let the motor
                          coast to a stop.
            wait (bool): When ``True``, this method will not return until the
                         time has run out. When ``False`` this method will
                         return immediately.
        """
        self.on_for_degrees(speed, rotations * 360, brake, wait)

    def on_for_time(self, speed, time, brake=True, wait=True):
        """Run the motor at the target speed for a fixed duration.

        The motor will run until the time expires or another command is given.

        :param int speed: The target speed in percent [-100..100].
        :param float time: The time for the motor to run in seconds.
        :param bool brake: ``True`` cases the motor to hold it's position when
            when it is reached. ``False`` will let the motor coast to a stop.
        :param bool wait: When ``True``, this method will not return until the
            time has run out. When ``False`` this method will return immediately.
        """
        if brake:
            stop_action = StopAction.HOLD
        else:
            stop_action = StopAction.COAST
        self._set_speed_sp(speed)
        self._set_time_sp(int(time * 1000))
        self._set_stop_action(stop_action)
        if wait:
            self._command.write('run-forever')
            utime.sleep(time)
            self._command.write('stop')
        else:
            self._command.write('run-timed')

    def run_unregulated(self, duty_cycle):
        """Run the motor using the specified duty cycle.

        The motor will continue to run with this duty cycle another command is
        given.

        :param int duty_cycle: the duty cycle, -100 to 100 percent
        """
        self._set_duty_cycle_sp(duty_cycle)
        self._command.write('run-direct')

    def off(self, brake=True):
        """Stop the motor

        :param bool brake: ``True`` cases the motor to hold it's position when
            when it is reached. ``False`` will let the motor coast to a stop.
        """
        if brake:
            stop_action = StopAction.HOLD
        else:
            stop_action = StopAction.COAST
        self._set_stop_action(stop_action)
        self._command.write('stop')

    def _set_duty_cycle_sp(self, duty_cycle):
        if duty_cycle < -100 or duty_cycle > 100:
            raise ValueError('duty cycle is out of range')
        self._duty_cycle_sp.write(duty_cycle)

    def _set_speed_sp(self, speed):
        # convert speed from % to tacho counts per second
        if speed < -100 or speed > 100:
            raise ValueError('speed is out of range')
        speed = int(speed * self._max_speed / 100)
        self._speed_sp.write(speed)

    def _set_position_sp(self, degrees):
        # convert rotations to tacho counts
        counts = int(self._count_per_rot * degrees / 360)
        self._position_sp.write(counts)

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

        :param string port: The output port the motor is connected to.
        """
        super(LargeMotor, self).__init__(port, TachoMotor.EV3_LARGE)


class MediumMotor(TachoMotor):
    """Object that represents a LEGO EV3 Medium motor."""

    def __init__(self, port):
        """Create a new instace of a medium motor.

        :param string port: The output port the motor is connected to.
        """
        super(MediumMotor, self).__init__(port, TachoMotor.EV3_MEDIUM)


class Steer():
    def __init__(self, left_port, right_port):
        self._left_motor = LargeMotor(left_port)
        self._right_motor = LargeMotor(right_port)

    def on_for_degrees(self, steering, speed, degrees, brake=True):
        if steering > 100 or steering < -100:
            raise ValueError('steering is out of range')
        if speed < 0:
            speed = abs(speed)
            degrees *= -1
        left_speed = right_speed = speed
        left_degrees = right_degrees = int(degrees)
        if steering < 0:
            steering = (50 + steering) * 2
            left_speed = speed * steering / 100
            left_degrees = degrees * steering / 100
        elif steering > 0:
            steering = (50 - steering) * 2
            right_speed = speed * steering / 100
            right_degrees = degrees * steering / 100

        if brake:
            stop_action = StopAction.HOLD
        else:
            stop_action = StopAction.COAST

        self._left_motor._set_speed_sp(left_speed)
        self._left_motor._set_position_sp(left_degrees)
        self._left_motor._set_stop_action(stop_action)
        self._right_motor._set_speed_sp(right_speed)
        self._right_motor._set_position_sp(right_degrees)
        self._right_motor._set_stop_action(stop_action)

        if left_degrees:
            self._left_motor._command.write('run-to-rel-pos')
        else:
            self._left_motor._command.write('stop')

        if right_degrees:
            self._right_motor._command.write('run-to-rel-pos')
        else:
            self._right_motor._command.write('stop')

        while True:
            state = self._left_motor._state.read().split(' ')
            if 'running' not in state or 'holding' in state:
                break

        while True:
            state = self._right_motor._state.read().split(' ')
            if 'running' not in state or 'holding' in state:
                break

    def on_for_rotations(self, steering, speed, rotations, brake=True):
        self.on_for_degrees(steering, speed, rotations * 360, brake)


class Tank():
    def __init__(self, left_port, right_port):
        self._steer = Steer(left_port, right_port)

    def on_for_degrees(self, left_speed, right_speed, degrees, brake=True):
        if left_speed < -100 or left_speed > 100:
            raise ValueError('left_speed is out of range')
        if right_speed < -100 or right_speed > 100:
            raise ValueError('right_speed is out of range')

        # algorithm based on EV3-G tank block
        if degrees < 0:
            left_speed *= -1
            right_speed *= -1
            degrees = abs(degrees)
        if abs(left_speed) > abs(right_speed):
            speed = left_speed
        else:
            speed = right_speed

        if speed:
            turn = 50 * (left_speed - right_speed) / speed
        else:
            turn = 0

        self._steer.on_for_degrees(turn, speed, degrees, brake)

    def on_for_rotations(self, left_speed, right_speed, rotations, brake=True):
        self.on_for_degrees(left_speed, right_speed, rotations * 360, brake)
