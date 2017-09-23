
# project
from project import brick


def feed_in():
    """This will feed the paper in until it covers the light sensor. This
    should be done before printing anything.
    """

    while True:
        brick['motor']['B'].on(-50)
        if brick['sensor']['4'].read_reflected() > 4:
            break
    brick['motor']['B'].off()
