
from utime import sleep

from project import brick
from project import variables

# myblocks
from lower_pen import lower_pen
from lift_pen import lift_pen


def print_m(size):
    seg2 = variables['Seg2']
    seg4 = variables['Seg4']
    brick['motor']['B'].on_for_degrees(-25, seg4)
    lower_pen()
    brick['motor']['B'].on_for_degrees(25, seg4)
    brick['motor']['A+B'].on_for_degrees(10, -10, seg2)
    sleep(0.05)
    brick['motor']['A+B'].on_for_degrees(10, 10, seg2)
    brick['motor']['B'].on_for_degrees(-25, seg4)
    lift_pen()
    brick['motor']['B'].on_for_degrees(25, seg4)
