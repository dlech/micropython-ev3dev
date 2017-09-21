"""LEGO MINDSTORMS EV3 buttons"""

import signal  # causes keyboard interupt to go to main thread
import _thread

from collections import OrderedDict
from errno import EINTR
from fcntl import ioctl

from uctypes import addressof
from uctypes import sizeof
from uctypes import struct
from uctypes import UINT16
from uctypes import INT32
from uctypes import UINT64

_EV_KEY = 0x01
_KEY_MAX = 0x2FF
_KEY_BUF_LEN = (_KEY_MAX + 7) // 8
_EVIOCGKEY = 2 << (14 + 8 + 8) | _KEY_BUF_LEN << (8 + 8) | ord('E') << 8 | 0x18

_input_event = {
        'time': UINT64 | 0,  # struct timeval
        'type': UINT16 | 8,
        'code': UINT16 | 10,
        'value': INT32 | 12,
}


def _test_bit(buf, index):
    byte = buf[int(index >> 3)]
    bit = byte & (1 << (index % 8))
    return bool(bit)


class Buttons():
    """Object that represents the buttons on the EV3"""
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    CENTER = 'enter'
    BACK = 'backspace'

    _lookup = OrderedDict()
    _lookup[103] = UP
    _lookup[28] = CENTER
    _lookup[108] = DOWN
    _lookup[106] = RIGHT
    _lookup[105] = LEFT
    _lookup[14] = BACK

    def __init__(self):
        self._devnode = open('/dev/input/by-path/platform-gpio_keys-event', 'b')
        self._fd = self._devnode.fileno()
        self._buffer = bytearray(_KEY_BUF_LEN)
        self._lock = _thread.allocate_lock()
        self._state = {
            self.UP: 0,
            self.DOWN: 0,
            self.LEFT: 0,
            self.RIGHT: 0,
            self.CENTER: 0,
            self.BACK: 0,
        }
        self._bumped = {
            self.UP: False,
            self.DOWN: False,
            self.LEFT: False,
            self.RIGHT: False,
            self.CENTER: False,
            self.BACK: False,
        }
        # taking advantage of the fact that micropython kills thread on exit
        _thread.start_new_thread(self._read_event, ())

    def _read_event(self):
        data = bytearray(sizeof(_input_event))
        event = struct(addressof(data), _input_event)
        while True:
            try:
                self._devnode.readinto(data)
            except OSError as err:
                if err.args[0] == EINTR:
                    continue
                raise err
            if event.type != _EV_KEY:
                continue
            key = self._lookup.get(event.code)
            if key:
                with self._lock:
                    self._state[key] = event.value
                    if not event.value:
                        # key was released, so we have bump
                        self._bumped[key] = True

    def read(self):
        """Returns a button if any button is pressed.

        If more than one button is pressed, the order of precedence is
        UP, CENTER, DOWN, RIGHT, LEFT, BACK.
        """
        with self._lock:
            ioctl(self._fd, _EVIOCGKEY, self._buffer, mut=True)

            for k, v in self._lookup.items():
                if _test_bit(self._buffer, k):
                    return v

            return None

    def compare(self, buttons, state):
        """Compares a list of buttons to a state.

        Parameters:
            buttons (tuple): List of buttons to check
            state (str): The state: 'released', 'pressed' or 'bumped'

        Returns:
            The button with the given state, otherwise ``None``.
        """
        if state not in ('released', 'pressed', 'bumped'):
            raise ValueError('Invalid state')
        with self._lock:
            if state == 'released':
                for b in buttons:
                    if not self._state[b]:
                        return b
            elif state == 'pressed':
                for b in buttons:
                    if self._state[b]:
                        return b
            else:
                for b in buttons:
                    if self._bumped[b]:
                        self._bumped[b] = False
                        return b
            return None

    def wait(self, buttons, state):
        """Waits until a button matches a state.

        Parameters:
            buttons (tuple): List of buttons to check
            state (str): The state: 'released', 'pressed' or 'bumped'

        Returns:
            The button with the given state, otherwise ``None``.
        """
        while not self.compare(buttons, state):
            pass

    def _pressed(self):
        """Returns list of names of pressed buttons.
        """
        ioctl(self._fd, _EVIOCGKEY, self._buffer, mut=True)

        pressed = []
        for k, v in self._lookup.items():
            if _test_bit(self._buffer, k):
                pressed.append(v)
        return pressed
