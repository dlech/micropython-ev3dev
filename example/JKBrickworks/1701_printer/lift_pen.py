
from project import motor


def lift_pen():
    """Lifts the pen off the page so that it can be moved without depositing
    ink.
    """
    motor['C'].on_for_degrees(25, 180)
