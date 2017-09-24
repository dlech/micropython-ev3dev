
from project import motor
from project import variables

# My Blocks
from lower_pen import lower_pen
from lift_pen import lift_pen


def print_y(size):
    seg2 = variables['Seg2']
    lower_pen()
    motor['A+B'].on_for_degrees(20, -20, seg2)
    motor['B'].on_for_degrees(-20, seg2)
    motor['B'].on_for_degrees(20, seg2)
    motor['A+B'].on_for_degrees(20, 20, seg2)
    lift_pen()
