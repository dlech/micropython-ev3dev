
from project import brick
from project import variables

# myblocks
from lower_pen import lower_pen
from lift_pen import lift_pen


def print_v(size):
    seg4 = variables['Seg4']
    lower_pen()
    brick['motor']['A+B'].on_for_degrees(10, -20, seg4)
    brick['motor']['A+B'].on_for_degrees(10, 20, seg4)
    lift_pen()
