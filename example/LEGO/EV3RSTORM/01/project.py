from os import path

from uev3dev.display import Display
from uev3dev.display import ImageFile
from uev3dev.motor import LargeMotor
from uev3dev.motor import Steer


motor = {
    'A': None,
    'B': LargeMotor('B'),
    'C': LargeMotor('C'),
    'D': None,
    'B+C': Steer('B', 'C'),
}

display = Display()

IMAGE_DIR = '/usr/share/images/ev3dev/mono/'

images = {
    'Middle left': ImageFile(path.join(IMAGE_DIR, 'eyes/middle_left.png'),
                             display),
    'Middle right': ImageFile(path.join(IMAGE_DIR, 'eyes/middle_right.png'),
                              display),
    'Neutral': ImageFile(path.join(IMAGE_DIR, 'eyes/neutral.png'), display),
}
