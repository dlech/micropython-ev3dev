
from uev3dev.button import CENTER
from uev3dev.button import State
from uev3dev.util import fork

from project import buttons
from project import variables

from print_letter import print_letter


def process_queue():
    """This will print all the letters in the queue and then keep processing
    letters as they are added to the queue.

    Use this block when you are printing text that the user is encoding using
    Morse code via the touch sensor. For example, the Printer program uses this
    block to continually process the user input.

    You can stop this block from processing text by hitting the center button
    on the EV3.
    """

    def thread1():
        while True:
            if len(variables['Queue']) > variables['QPosition']:
                qposition = variables['QPosition']
                print_letter(variables['Queue'][qposition])
                variables['QPosition'] = qposition + 1
            if variables['EStop']:
                break

    def thread2():
        buttons.wait((CENTER,), State.PRESSED)
        variables['EStop'] = True

    fork(thread1, thread2)
