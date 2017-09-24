#!/usr/bin/env micropython
"""This will print a full test page. It will do an entire print process and
test various parts of the program.
"""

from uev3dev.util import fork

from project import motor
from project import variables

# My Blocks
from carriage_move import carriage_move
from feed_in import feed_in
from feed_out import feed_out
from initialize import initialize
from line_feed import line_feed
from print_ev3_logo import print_ev3_logo
from print_queue import print_queue
from print_registration_line import print_registration_line
from text_size import text_size


def print_test_page():
    """This will print a full test page. It will do an entire print process and
    test various parts of the program.
    """

    # Initialize, feed in the paper, lower the pen and draw a registration
    # line.
    initialize()
    feed_in()
    motor['C'].on_for_rotations(50, -2.5)
    carriage_move(0)
    print_registration_line()

    # Set the test size and draw the 'Quick brown fox...' text.
    text_size(10)
    line_feed()
    variables['Queue'] = variables['QuickFox']
    print_queue()
    line_feed()

    # Print 'Mindstorms' several times, each at a different text size and on
    # its own line.
    variables['Queue'] = variables['Mindstorms']
    variables['QPosition'] = 0
    print_queue()
    text_size(12)
    variables['QPosition'] = 0
    print_queue()
    text_size(14)
    variables['QPosition'] = 0
    print_queue()
    text_size(16)
    variables['QPosition'] = 0
    print_queue()

    # Print the EV3 Logo.
    text_size(10)
    line_feed()
    print_ev3_logo(1)

    # Print 'JK Brickworks' and 'Keep on Building'
    line_feed()
    variables['Queue'] = variables['JKBrickworks']
    variables['QPosition'] = 0
    print_queue()
    line_feed()
    variables['Queue'] = variables['KeepBuilding']
    variables['QPosition'] = 0
    print_queue()
    line_feed()
    print_registration_line()

    # Move the pen back to the middle, lift it and feed out the paper.
    carriage_move(525)

    def thread1():
        motor['C'].on_for_rotations(50, 2.5)

    def thread2():
        feed_out()

    fork(thread1, thread2)


if __name__ == '__main__':
    print_test_page()
