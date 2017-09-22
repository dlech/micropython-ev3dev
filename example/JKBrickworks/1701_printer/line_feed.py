
from project import brick
from project import variables


def line_feed():
    """Feed the paper in by the height of one line, plus the line spacing,
    which should really be specified as a variable in the 'Initialize' MyBlock.
    """
    brick['motor']['B'].on_for_degrees(-20, variables['Seg4'])
    brick['motor']['B'].on_for_degrees(-20, 20)
