#!/usr/bin/env micropython

from utime import sleep

from uev3dev import fork

from project import brick
from project import variables

# myblocks
from initialize import initialize
from carriage_move import carriage_move


def calibrate():
    initialize()
    brick['motor']['C'].on_for_rotations(25, -2.5)

    def thread1():
        while True:
            sleep(0.25)
            carriage_move(0)
            variables['LinePosition'] = 0
            sleep(0.25)
            line_width = variables['LineWidth']
            carriage_move(line_width)
            variables['LinePosition'] = line_width
            if brick['buttons'].compare((brick['buttons'].CENTER,), 'bumped'):
                break
        carriage_move(525)
        brick['motor']['C'].on_for_rotations(25, 3)

    def thread2():
        while True:
            brick['buttons'].wait((brick['buttons'].UP,
                                   brick['buttons'].CENTER,
                                   brick['buttons'].DOWN), 'pressed')
            button = brick['buttons'].read()
            if button == brick['buttons'].UP:
                brick['motor']['C'].on_for_degrees(25, 5)
            elif button == brick['buttons'].DOWN:
                brick['motor']['C'].on_for_degrees(-25, 5)
            elif button == brick['buttons'].CENTER:
                # This is not in the EV3-G program, but is needed in order for
                # the program to exit, otherwise this thread keeps running.
                raise SystemExit

    fork(thread1, thread2)

if __name__ == '__main__':
    calibrate()
