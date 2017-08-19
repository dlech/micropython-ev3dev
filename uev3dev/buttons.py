"""LEGO MINDSTORMS EV3 buttons"""

from fcntl import ioctl


KEY_MAX = 0x2FF
KEY_BUF_LEN = int((KEY_MAX + 7) / 8)
EVIOCGKEY = (2 << (14 + 8 + 8) | KEY_BUF_LEN << (8 + 8) | ord('E') << 8 | 0x18)


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

    _lookup = {
        103: UP,
        108: DOWN,
        105: LEFT,
        106: RIGHT,
        28: CENTER,
        14: BACK,
    }

    def __init__(self):
        self._devnode = open('/dev/input/by-path/platform-gpio_keys-event')
        self._buffer = bytes(KEY_BUF_LEN)

    def pressed(self):
        """
        Returns list of names of pressed buttons.
        """
        ioctl(self._devnode.fileno(), EVIOCGKEY, self._buffer, mut=True)

        pressed = []
        for k, v in self._lookup.items():
            if _test_bit(self._buffer, k):
                pressed.append(v)
        return pressed
