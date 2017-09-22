
from project import brick
from project import variables

# myblocks
from lower_pen import lower_pen
from lift_pen import lift_pen


def print_y(size):
    seg2 = variables['Seg2']
    lower_pen()
    brick['motor']['A+B'].on_for_degrees(20, -20, seg2)
    brick['motor']['B'].on_for_degrees(-20, seg2)
    brick['motor']['B'].on_for_degrees(20, seg2)
    brick['motor']['A+B'].on_for_degrees(20, 20, seg2)
    lift_pen()
