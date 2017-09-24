
from project import motor
from project import variables

# My Blocks
from lower_pen import lower_pen
from lift_pen import lift_pen


def print_z(size):
    seg4 = variables['Seg4']
    lower_pen()
    motor['A'].on_for_degrees(20, seg4)
    motor['A+B'].on_for_degrees(-20, -20, seg4)
    motor['A'].on_for_degrees(20, seg4)
    lift_pen()
    motor['B'].on_for_degrees(20, seg4)
