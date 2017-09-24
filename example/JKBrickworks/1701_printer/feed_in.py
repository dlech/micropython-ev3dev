
from project import motor
from project import sensor


def feed_in():
    """This will feed the paper in until it covers the light sensor. This
    should be done before printing anything.
    """

    while True:
        motor['B'].on(-50)
        if sensor['4'].read_reflected() > 4:
            break
    motor['B'].off()
