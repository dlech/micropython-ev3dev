
from project import motor
from project import variables


def carriage_move(position):
    """Moves the pen to the specified horizontal position on the line.

    It calculates how much to move the pen based on its current position
    (LinePosition) and the requested new position.
    """
    motor['A'].on_for_degrees(50, position - variables['LinePosition'])
    variables['LinePosition'] = position

    # If we are moving the pen to the left side of the page, 'overshoot'
    # the movement and then come back a bit. This is in an effort to take
    # up the backlash in the motors.
    if position == 1:
        pass
    else:
        motor['A'].on_for_degrees(-20, 10)
        motor['A'].on_for_degrees(20, 10)
