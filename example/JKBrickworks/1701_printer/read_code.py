import operator

from uev3dev.sensors import EV3TouchSensor
from uev3dev.sound import PlayType
from uev3dev.util import fork
from uev3dev.util import write_at_index

from project import sensor
from project import sound
from project import timer
from project import variables

from translate_code import translate_code

# FIXME: operator is not implemented in micropython-lib
operator.gt = lambda x, y: x > y


def read_code():
    """This block is responsible for analysing the timing between pushes of the
    touch sensor to convert a Morse code signal into a letter.
    """
    # The top loop continuously measures the length of successive button
    # presses and builds an array of dots and dashes (shorts and longs, or 0s
    # and 1s) to represent the letter that is encoded.

    # The bottom loop waits until a length of time has passed without the
    # button being pressed (using the second timer, which is reset after every
    # button press in the top loop), indicating that coding the letter is now
    # complete. When that happens, the 'TranslateCode' block is called to
    # analyse the 'Code' array to see what letter was encoded.

    variables['CodeIndex'] = 0

    def thread1():
        while True:
            # Wait for the touch sensor to be depressed. When that happens
            # start the first timer and start playing the tone.
            # Wait for the touch sensor to be released. When that happens
            # measure how long the first timer has been on and stop playing the
            # tone.
            sensor['1'].wait(EV3TouchSensor.PRESSED)
            sound.play_tone(440, 1, 5, PlayType.ONCE)
            timer[1].reset()
            sensor['1'].wait(EV3TouchSensor.RELEASED)
            sound.stop()
            timer[2].reset()
            variables['Encoding'] = True
            if timer[1].elapsed_time() < 0.2:
                variables['CodeSignal'] = 0
            else:
                variables['CodeSignal'] = 1
            # Depending on the length of the press, we will get a 0 or 1.
            # Append that value to the 'Code' array.
            code_index = variables['CodeIndex']
            variables['Code'] = write_at_index(variables['Code'], code_index,
                                               variables['CodeSignal'])
            variables['CodeIndex'] = code_index + 1

    def thread2():
        while True:
            if variables['Encoding']:
                timer[2].wait(operator.gt, 0.8)
                variables['Encoding'] = False
                translate_code()
                variables['CodeIndex'] = 0

    fork(thread1, thread2)
