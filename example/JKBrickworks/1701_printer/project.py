"""Common project information"""

from uev3dev.button import Buttons
from uev3dev.leds import StatusLight
from uev3dev.motors import LargeMotor
from uev3dev.motors import MediumMotor
from uev3dev.motors import Tank
from uev3dev.sensors import EV3ColorSensor

brick = {
    'motor': {
        'A': LargeMotor('A'),
        'B': LargeMotor('B'),
        'C': MediumMotor('C'),
        'D': None,
        'A+B': Tank('A', 'B'),
    },
    'sensor': {
        '1': None,
        '2': None,
        '3': None,
        '4': EV3ColorSensor('4'),
    },
    'buttons': Buttons(),
    'light': StatusLight(),
}

# comes from the Variables tab in Project Properties
variables = {
    'LinePosition': 0,
    'Seg1': 0,
    'Seg2': 0,
    'Seg3': 0,
    'Seg4': 0,
    'Queue': [],
    'QPosition': 0,
    'QCount': 0,
    'LastLW': 0,
    'LastLetterWidth': 0,
    'HelloWorld': [],
    'Mindstorms': [],
    'alphabet': [],
    'JKBrickworks': [],
    'TestLetters': [],
    'CodeIndex': 0,
    'code_value': 0,
    'Encoding': False,
    'NewCharacter': 0,
    'EStop': False,
    'LineWidth': 0,
    'LetterSpacing': 0,
    'QuickFox': [],
    'KeepBuilding': [],
}
