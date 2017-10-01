#!/usr/bin/env micropython

from project import display
from project import images
from project import motor


def program():
    display.image(images['Neutral'], True, 0, 0)
    motor['B+C'].on_for_rotations(0, 75, 5, True)
    display.image(images['Middle left'], True, 0, 0)
    motor['B+C'].on_for_rotations(50, 75, 5, True)
    display.image(images['Neutral'], True, 0, 0)
    motor['B+C'].on_for_rotations(0, 75, 5, True)
    display.image(images['Middle right'], True, 0, 0)
    motor['B+C'].on_for_rotations(-50, 75, 5, True)

if __name__ == '__main__':
    program()
