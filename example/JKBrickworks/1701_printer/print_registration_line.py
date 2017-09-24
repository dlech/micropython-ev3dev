
from project import motor

# My Blocks
from lower_pen import lower_pen
from lift_pen import lift_pen


def print_registration_line():
    """Print two boxes, one on the left side of the page and one on the right
    side of the page.
    """
    lower_pen()
    motor['A'].on_for_degrees(20, 75)
    motor['B'].on_for_degrees(-20, 50)
    motor['A'].on_for_degrees(-20, 75)
    motor['B'].on_for_degrees(20, 50)
    motor['A'].on_for_degrees(20, 75)
    motor['B'].on_for_degrees(-20, 50)
    motor['A'].on_for_degrees(-20, 75)
    motor['B'].on_for_degrees(20, 50)
    lift_pen()
    motor['A'].on_for_degrees(50, 1050)

    lower_pen()
    motor['A'].on_for_degrees(-20, 75)
    motor['B'].on_for_degrees(-20, 50)
    motor['A'].on_for_degrees(20, 75)
    motor['B'].on_for_degrees(20, 50)
    motor['A'].on_for_degrees(-20, 75)
    motor['B'].on_for_degrees(-20, 50)
    motor['A'].on_for_degrees(20, 75)
    motor['B'].on_for_degrees(20, 50)
    lift_pen()
    motor['A'].on_for_degrees(50, -1050)
    motor['A'].on_for_degrees(20, 10)
    motor['B'].on_for_degrees(-20, 70)
