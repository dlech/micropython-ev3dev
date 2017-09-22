
from utime import sleep

from project import brick

# My Blocks
from lower_pen import lower_pen
from lift_pen import lift_pen


def print_ev3_logo(size):
    """Prints the EV3 Logo.

    The input paramater was intended to be used to specify the size of the
    logo, but it is currently unused.
    """
    brick['motor']['B'].on_for_degrees(-25, 70)
    brick['motor']['A'].on_for_degrees(50, 200)
    sleep(0.1)
    lower_pen()
    brick['motor']['B'].on_for_degrees(25, 10)
    sleep(0.1)
    brick['motor']['A+B'].on_for_degrees(25, 17, 90)
    sleep(0.1)
    brick['motor']['A'].on_for_degrees(25, 90)
    sleep(0.1)
    brick['motor']['A+B'].on_for_degrees(25, -17, 90)
    brick['motor']['B'].on_for_degrees(-25, 10)
    brick['motor']['A'].on_for_degrees(-25, 75)
    brick['motor']['B'].on_for_degrees(25, 30)
    brick['motor']['A'].on_for_degrees(-25, 120)
    brick['motor']['B'].on_for_degrees(-25, 30)
    brick['motor']['A'].on_for_degrees(-25, 75)
    lift_pen()
    brick['motor']['B'].on_for_degrees(-25, 20)

    lower_pen()
    brick['motor']['B'].on_for_degrees(-25, 10)
    sleep(0.1)
    brick['motor']['A+B'].on_for_degrees(25, -17, 90)
    sleep(0.1)
    brick['motor']['A'].on_for_degrees(25, 90)
    sleep(0.1)
    brick['motor']['A+B'].on_for_degrees(25, 17, 90)
    brick['motor']['B'].on_for_degrees(25, 10)
    brick['motor']['A'].on_for_degrees(-25, 75)
    brick['motor']['B'].on_for_degrees(-25, 30)
    brick['motor']['A'].on_for_degrees(-25, 120)
    brick['motor']['B'].on_for_degrees(25, 30)
    brick['motor']['A'].on_for_degrees(-25, 75)
    lift_pen()

    brick['motor']['A'].on_for_degrees(25, 120)
    brick['motor']['B'].on_for_degrees(25, 30)
    lower_pen()
    brick['motor']['A'].on_for_degrees(25, 60)
    brick['motor']['B'].on_for_degrees(-25, 40)
    brick['motor']['A'].on_for_degrees(-25, 60)
    brick['motor']['B'].on_for_degrees(25, 40)
    lift_pen()
    brick['motor']['A'].on_for_degrees(-25, 120)
    brick['motor']['B'].on_for_degrees(-25, 100)
    brick['motor']['A'].on_for_degrees(-50, 200)
