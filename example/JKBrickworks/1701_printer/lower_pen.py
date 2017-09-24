
from project import motor


def lower_pen():
    """Lowers the pen on the page so that it will deposit ink when it is moved.
    """
    motor['C'].on_for_degrees(25, -180)
