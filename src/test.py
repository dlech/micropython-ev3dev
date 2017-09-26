#!/usr/bin/env micropython
"""Test program for testing whatever"""

import time

from uev3dev.sound import PlayType
from uev3dev.sound import Sound
from uev3dev.util import debug_print

sound = Sound()

debug_print('enter')
sound.play_note('C4', 0.1, 20, PlayType.WAIT)
sound.play_note('D4', 0.1, 20, PlayType.WAIT)
sound.play_note('E4', 0.1, 20, PlayType.WAIT)
sound.play_note('F4', 0.1, 20, PlayType.WAIT)
sound.play_note('G4', 0.1, 20, PlayType.WAIT)
sound.play_note('A5', 0.1, 20, PlayType.WAIT)
sound.play_note('B5', 0.1, 20, PlayType.WAIT)
sound.play_note('C5', 0.1, 20, PlayType.WAIT)
debug_print('exit')

debug_print('enter')
sound.play_file('/usr/share/sounds/alsa/Front_Right.wav', 100, PlayType.REPEAT)
debug_print('exit')

time.sleep(5)
