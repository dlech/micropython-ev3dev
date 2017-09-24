
from utime import sleep

from project import motor

# My Blocks
from lower_pen import lower_pen
from lift_pen import lift_pen


def print_ev3_logo(size):
    """Prints the EV3 Logo.

    The input paramater was intended to be used to specify the size of the
    logo, but it is currently unused.
    """
    motor['B'].on_for_degrees(-25, 70)
    motor['A'].on_for_degrees(50, 200)
    sleep(0.1)
    lower_pen()
    motor['B'].on_for_degrees(25, 10)
    sleep(0.1)
    motor['A+B'].on_for_degrees(25, 17, 90)
    sleep(0.1)
    motor['A'].on_for_degrees(25, 90)
    sleep(0.1)
    motor['A+B'].on_for_degrees(25, -17, 90)
    motor['B'].on_for_degrees(-25, 10)
    motor['A'].on_for_degrees(-25, 75)
    motor['B'].on_for_degrees(25, 30)
    motor['A'].on_for_degrees(-25, 120)
    motor['B'].on_for_degrees(-25, 30)
    motor['A'].on_for_degrees(-25, 75)
    lift_pen()
    motor['B'].on_for_degrees(-25, 20)

    lower_pen()
    motor['B'].on_for_degrees(-25, 10)
    sleep(0.1)
    motor['A+B'].on_for_degrees(25, -17, 90)
    sleep(0.1)
    motor['A'].on_for_degrees(25, 90)
    sleep(0.1)
    motor['A+B'].on_for_degrees(25, 17, 90)
    motor['B'].on_for_degrees(25, 10)
    motor['A'].on_for_degrees(-25, 75)
    motor['B'].on_for_degrees(-25, 30)
    motor['A'].on_for_degrees(-25, 120)
    motor['B'].on_for_degrees(25, 30)
    motor['A'].on_for_degrees(-25, 75)
    lift_pen()

    motor['A'].on_for_degrees(25, 120)
    motor['B'].on_for_degrees(25, 30)
    lower_pen()
    motor['A'].on_for_degrees(25, 60)
    motor['B'].on_for_degrees(-25, 40)
    motor['A'].on_for_degrees(-25, 60)
    motor['B'].on_for_degrees(25, 40)
    lift_pen()
    motor['A'].on_for_degrees(-25, 120)
    motor['B'].on_for_degrees(-25, 100)
    motor['A'].on_for_degrees(-50, 200)
