
from project import brick
from project import variables

# myblocks
from lower_pen import lower_pen
from lift_pen import lift_pen


def print_b(size):
    seg1 = variables['Seg1']
    seg3 = variables['Seg3']
    seg4 = variables['Seg4']
    lower_pen()
    brick['motor']['B'].on_for_degrees(-20, seg4)
    brick['motor']['A'].on_for_degrees(20, seg3)
    brick['motor']['A+B'].on_for_degrees(20, 20, seg1)
    brick['motor']['A+B'].on_for_degrees(-20, 20, seg1)
    brick['motor']['A'].on_for_degrees(-20, seg3)
    brick['motor']['A'].on_for_degrees(20, seg3)
    brick['motor']['A+B'].on_for_degrees(20, 20, seg1)
    brick['motor']['A+B'].on_for_degrees(-20, 20, seg1)
    brick['motor']['A'].on_for_degrees(-20, seg3)
    lift_pen()
    brick['motor']['A'].on_for_degrees(20, seg4)
