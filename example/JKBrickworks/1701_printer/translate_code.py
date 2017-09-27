from os import path
from time import sleep

from uev3dev.led import Color
from uev3dev.sound import PlayType
from uev3dev.util import write_at_index

from project import display
from project import sound
from project import sounds
from project import status_light
from project import variables


def translate_code():
    """Analyse the array of dots and dashes (the 'Code' array) and convert it
    into a numeric value.
    """

    code = variables['Code']
    code_index = variables['CodeIndex']
    len(code)
    variables['CodeValue'] = code_index * 32
    sleep(0)
    count = 0
    while True:
        variables['CodeValue'] = (code[count] * (2 ** count) +
                                  variables['CodeValue'])
        count += 1
        if count >= code_index:
            break
    # Convert the computed code value into a letter index. If it is a known
    # letter, display it on the screen as well, otherwise display the raw
    # numeric value on the screen.
    code_value = variables['CodeValue']
    if code_value == 66:
        display.text_pixels('A', True, 0, 0, False, 2)
        variables['NewCharacter'] = 0
    elif code_value == 129:
        display.text_pixels('B', True, 0, 0, False, 2)
        variables['NewCharacter'] = 1
    elif code_value == 133:
        display.text_pixels('C', True, 0, 0, False, 2)
        variables['NewCharacter'] = 2
    elif code_value == 97:
        display.text_pixels('D', True, 0, 0, False, 2)
        variables['NewCharacter'] = 3
    elif code_value == 32:
        display.text_pixels('E', True, 0, 0, False, 2)
        variables['NewCharacter'] = 4
    elif code_value == 132:
        display.text_pixels('F', True, 0, 0, False, 2)
        variables['NewCharacter'] = 5
    elif code_value == 99:
        display.text_pixels('G', True, 0, 0, False, 2)
        variables['NewCharacter'] = 6
    elif code_value == 128:
        display.text_pixels('H', True, 0, 0, False, 2)
        variables['NewCharacter'] = 7
    elif code_value == 64:
        display.text_pixels('I', True, 0, 0, False, 2)
        variables['NewCharacter'] = 8
    elif code_value == 142:
        display.text_pixels('J', True, 0, 0, False, 2)
        variables['NewCharacter'] = 9
    elif code_value == 101:
        display.text_pixels('K', True, 0, 0, False, 2)
        variables['NewCharacter'] = 10
    elif code_value == 130:
        display.text_pixels('L', True, 0, 0, False, 2)
        variables['NewCharacter'] = 11
    elif code_value == 67:
        display.text_pixels('M', True, 0, 0, False, 2)
        variables['NewCharacter'] = 12
    elif code_value == 65:
        display.text_pixels('N', True, 0, 0, False, 2)
        variables['NewCharacter'] = 13
    elif code_value == 103:
        display.text_pixels('O', True, 0, 0, False, 2)
        variables['NewCharacter'] = 14
    elif code_value == 134:
        display.text_pixels('P', True, 0, 0, False, 2)
        variables['NewCharacter'] = 15
    elif code_value == 139:
        display.text_pixels('Q', True, 0, 0, False, 2)
        variables['NewCharacter'] = 16
    elif code_value == 98:
        display.text_pixels('R', True, 0, 0, False, 2)
        variables['NewCharacter'] = 17
    elif code_value == 96:
        display.text_pixels('S', True, 0, 0, False, 2)
        variables['NewCharacter'] = 18
    elif code_value == 33:
        display.text_pixels('T', True, 0, 0, False, 2)
        variables['NewCharacter'] = 19
    elif code_value == 100:
        display.text_pixels('U', True, 0, 0, False, 2)
        variables['NewCharacter'] = 20
    elif code_value == 136:
        display.text_pixels('V', True, 0, 0, False, 2)
        variables['NewCharacter'] = 21
    elif code_value == 102:
        display.text_pixels('W', True, 0, 0, False, 2)
        variables['NewCharacter'] = 22
    elif code_value == 137:
        display.text_pixels('X', True, 0, 0, False, 2)
        variables['NewCharacter'] = 23
    elif code_value == 141:
        display.text_pixels('Y', True, 0, 0, False, 2)
        variables['NewCharacter'] = 24
    elif code_value == 131:
        display.text_pixels('Z', True, 0, 0, False, 2)
        variables['NewCharacter'] = 25
    elif code_value == 138:
        display.text_pixels('Space', True, 0, 0, False, 2)
        variables['NewCharacter'] = 26
    elif code_value == 143:
        display.text_pixels('Return', True, 0, 0, False, 2)
        variables['NewCharacter'] = 27
    else:
        display.text_pixels(variables['CodeValue'], True, 0, 0, False, 2)
        variables['NewCharacter'] = -1

    # If it is a valid letter, add it to the letter queue for processing,
    # otherwise play and error sound.
    if variables['NewCharacter'] == -1:
        status_light.on(Color.ORANGE, False)
        sound.play_file(sounds['General alert'], 5, PlayType.WAIT)
        status_light.off()
    else:
        queue = variables['Queue']
        variables['Queue'] = write_at_index(queue, len(queue),
                                            variables['NewCharacter'])
