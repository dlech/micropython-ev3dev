
from project import motor
from project import variables

# My Blocks
from lower_pen import lower_pen
from lift_pen import lift_pen


def print_g(size):
    seg1 = variables['Seg1']
    seg2 = variables['Seg2']
    seg3 = variables['Seg3']
    seg4 = variables['Seg4']
    motor['B'].on_for_degrees(-20, seg1)
    motor['A'].on_for_degrees(20, seg4)
    motor['A'].on_for_degrees(20, -10)
    lower_pen()

    motor['A+B'].on_for_degrees(-10, 10, seg1)
    motor['A'].on_for_degrees(-20, seg2)
    motor['A+B'].on_for_degrees(-10, -10, seg1)
    motor['B'].on_for_degrees(-20, seg2)
    motor['A+B'].on_for_degrees(10, -10, seg1)
    motor['A'].on_for_degrees(20, seg2)
    motor['A+B'].on_for_degrees(10, 10, seg1)
    motor['B'].on_for_degrees(-20, seg1)
    motor['B'].on_for_degrees(20, seg2)
    motor['A'].on_for_degrees(-20, seg2)
    lift_pen()

    motor['B'].on_for_degrees(20, seg2)
    motor['A'].on_for_degrees(20, seg3)
    motor['A'].on_for_degrees(20, 10)
