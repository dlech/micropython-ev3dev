
from project import motor
from project import variables

# My Blocks
from lower_pen import lower_pen
from lift_pen import lift_pen


def print_h(size):
    seg2 = variables['Seg2']
    seg4 = variables['Seg4']
    lower_pen()
    motor['B'].on_for_degrees(-20, seg4)
    motor['B'].on_for_degrees(20, seg2)
    motor['A'].on_for_degrees(20, seg4)
    motor['B'].on_for_degrees(-20, seg2)
    motor['B'].on_for_degrees(20, seg4)
    lift_pen()
