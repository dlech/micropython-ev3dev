#!/usr/bin/env micropython

from utime import sleep

from uev3dev.button import State
from uev3dev.button import CENTER
from uev3dev.button import DOWN
from uev3dev.button import UP
from uev3dev.util import fork

from project import buttons
from project import motor
from project import variables

# My Blocks
from initialize import initialize
from carriage_move import carriage_move


def calibrate():
    initialize()
    motor['C'].on_for_rotations(25, -2.5)

    def thread1():
        while True:
            sleep(0.25)
            carriage_move(0)
            variables['LinePosition'] = 0
            sleep(0.25)
            line_width = variables['LineWidth']
            carriage_move(line_width)
            variables['LinePosition'] = line_width
            if buttons.test((CENTER,), State.BUMPED):
                break
        carriage_move(525)
        motor['C'].on_for_rotations(25, 3)

    def thread2():
        while True:
            buttons.wait((UP, CENTER, DOWN), State.PRESSED)
            button = buttons.read()
            if button == UP:
                motor['C'].on_for_degrees(25, 5)
            elif button == DOWN:
                motor['C'].on_for_degrees(-25, 5)
            elif button == CENTER:
                # This is not in the EV3-G program, but is needed in order for
                # the program to exit, otherwise this thread keeps running.
                raise SystemExit

    fork(thread1, thread2)

if __name__ == '__main__':
    calibrate()
