
from project import brick
from project import variables

# My Blocks
from lower_pen import lower_pen
from lift_pen import lift_pen


def print_f(size):
    seg2 = variables['Seg2']
    seg3 = variables['Seg3']
    seg4 = variables['Seg4']
    brick['motor']['A'].on_for_degrees(20, seg4)
    brick['motor']['A'].on_for_degrees(20, -10)
    lower_pen()
    brick['motor']['A'].on_for_degrees(-20, seg4)
    brick['motor']['B'].on_for_degrees(-20, seg2)
    brick['motor']['A'].on_for_degrees(20, seg3)
    brick['motor']['A'].on_for_degrees(-20, seg3)
    brick['motor']['B'].on_for_degrees(-20, seg2)
    lift_pen()
    brick['motor']['A'].on_for_degrees(20, 10)
    brick['motor']['A'].on_for_degrees(20, seg4)
    brick['motor']['B'].on_for_degrees(20, seg4)
