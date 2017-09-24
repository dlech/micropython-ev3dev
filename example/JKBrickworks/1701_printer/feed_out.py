
from project import motor
from project import sensor


def feed_out():
    """Call when you are finished printing to feed the paper out."""
    while True:
        motor['B'].on(50)
        if sensor['4'].read_reflected() < 2:
            break
    motor['B'].off()
    motor['B'].on_for_degrees(50, 600)
