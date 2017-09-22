
from project import brick


def lift_pen():
    """Lifts the pen off the page so that it can be moved without depositing
    ink.
    """
    brick['motor']['C'].on_for_degrees(25, 180)
