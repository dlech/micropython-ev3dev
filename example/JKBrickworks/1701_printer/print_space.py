
from project import motor
from project import variables

# My Blocks
from lower_pen import lower_pen
from lift_pen import lift_pen


def print_space(size):
    seg4 = variables['Seg4']
    motor['A'].on_for_degrees(25, seg4)
