"""Common project information"""

from os import path

from uev3dev.button import Buttons
from uev3dev.display import Display
from uev3dev.led import StatusLight
from uev3dev.messaging import Messaging
from uev3dev.motor import LargeMotor
from uev3dev.motor import MediumMotor
from uev3dev.motor import Tank
from uev3dev.sensors import EV3ColorSensor
from uev3dev.sensors import EV3TouchSensor
from uev3dev.sound import Sound
from uev3dev.sound import SoundFile
from uev3dev.util import Timer


_project_dir = path.dirname(__file__)


# Brick hardware configuration

motor = {
    'A': LargeMotor('A'),
    'B': LargeMotor('B'),
    'C': MediumMotor('C'),
    'D': None,
    'A+B': Tank('A', 'B'),
}

sensor = {
    '1': EV3TouchSensor('1'),
    '2': None,
    '3': None,
    '4': EV3ColorSensor('4'),
}

buttons = Buttons()
display = Display()
sound = Sound()
status_light = StatusLight()

messaging = Messaging()

timer = {
    1: Timer(),
    2: Timer(),
    3: None,
    4: None,
    5: None,
    6: None,
    7: None,
}

# Stuff from Project Properties tab

sounds = {
    'General alert': SoundFile(path.join(_project_dir, 'general_alert.wav'))
}

variables = {
    'LinePosition': 0,
    'Seg1': 0,
    'Seg2': 0,
    'Seg3': 0,
    'Seg4': 0,
    'Queue': (),
    'QPosition': 0,
    'QCount': 0,
    'LastLW': 0,
    'LastLetterWidth': 0,
    'HelloWorld': (),
    'Mindstorms': (),
    'Alphabet': (),
    'JKBrickworks': (),
    'TestLetters': (),
    'CodeIndex': 0,
    'CodeSignal': 0,
    'Code': (),
    'CodeValue': 0,
    'Encoding': False,
    'NewCharacter': 0,
    'EStop': False,
    'LineWidth': 0,
    'LetterSpacing': 0,
    'QuickFox': (),
    'KeepBuilding': (),
}
