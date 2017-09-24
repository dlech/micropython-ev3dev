
from uev3dev.button import CENTER

from project import buttons
from project import variables

# My Blocks
from print_letter import print_letter


def print_queue():
    """This will print all the letters in the queue and exit when there are no
    more letters.

    Use this block when you are printing text you have coded into the program.
    For example, the PrintTestPage program uses this block to print each pieces
    of text.
    """
    variables['EStop'] = False
    while True:
        if len(variables['Queue']) > variables['QPosition']:
            print_letter(variables['Queue'][variables['QPosition']])
            variables['QPosition'] = variables['QPosition'] + 1
        else:
            variables['EStop'] = True
        if buttons.read() == CENTER:
            variables['EStop'] = True
        if variables['EStop']:
            break
