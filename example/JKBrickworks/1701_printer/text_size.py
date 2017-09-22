
from project import variables


def text_size(size):
    """This sets the text size to the input value specified."""
    variables['Seg1'] = size
    variables['Seg2'] = variables['Seg1'] * 2
    variables['Seg3'] = variables['Seg1'] * 3
    variables['Seg4'] = variables['Seg1'] * 4
