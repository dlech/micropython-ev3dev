
from project import brick


def feed_out():
    """Call when you are finished printing to feed the paper out."""
    while True:
        brick['motor']['B'].on(50)
        if brick['sensor']['4'].read_reflected() < 2:
            break
    brick['motor']['B'].off()
    brick['motor']['B'].on_for_degrees(50, 600)
