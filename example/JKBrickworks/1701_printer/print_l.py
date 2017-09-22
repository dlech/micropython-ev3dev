
from project import brick
from project import variables

# myblocks
from lower_pen import lower_pen
from lift_pen import lift_pen


def print_l(size):
    seg4 = variables['Seg4']
    lower_pen()
    brick['motor']['B'].on_for_degrees(-20, seg4)
    brick['motor']['A'].on_for_degrees(20, seg4)
    lift_pen()
    brick['motor']['B'].on_for_degrees(20, seg4)
