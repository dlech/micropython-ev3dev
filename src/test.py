#!/usr/bin/env micropython
"""Test program for testing whatever"""

import os
import time

from uev3dev.display import Display
from uev3dev.display import ImageFile
from uev3dev.util import debug_print

display = Display()

img = ImageFile(display, '/usr/share/images/ev3dev/mono/eyes/neutral.png')

display.image(img, True, 0, 0)
display.image(img, False, 50, 50)

time.sleep(5)
