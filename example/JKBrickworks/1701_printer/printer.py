#!/usr/bin/env micropython
"""The main printer program. There are three thread that are run
simultaneously, which are described below.
"""

from uev3dev.util import fork
from uev3dev.util import write_at_index

from project import messaging
from project import motor
from project import variables

from carriage_move import carriage_move
from feed_in import feed_in
from feed_out import feed_out
from initialize import initialize
from process_queue import process_queue
from read_code import read_code


def printer():
    initialize()
    feed_in()

    def thread1():
        """Continuously process the queue of letters."""
        motor['C'].on_for_rotations(50, -2.5)
        carriage_move(0)
        process_queue()
        carriage_move(525)

        def thread1_1():
            motor['C'].on_for_rotations(50, 2.5)

        def thread1_2():
            feed_out()

        fork(thread1_1, thread1_2)

    def thread2():
        """Continuously monitor the touch sensor and convert the Morse code
        sequence into a letter index which gets added to the letter queue.
        """
        read_code()

    def thread3():
        """This will wait for any bluetooth letter messages, and add them to
        the letter queue. This is only relevent if you are using 2 EV3 units to
        have a separate transmitter and receiver.
        """
        while True:
            letter = messaging.wait_update('Letter')
            queue = variables['Queue']
            variables['Queue'] = write_at_index(queue, len(queue), letter)

    fork(thread1, thread2, thread3)

if __name__ == '__main__':
    printer()
