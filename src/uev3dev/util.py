"""Internal utility module"""

import sys


def enum(**enums):
    """Create a new type that is used as an enum

    :param enums: keyword arguments giving the enum members and values
    """
    # micropython doesn't seem to have the enum(enum34) package
    # https://stackoverflow.com/a/1695250/1976323
    return type('Enum', (), enums)


def debug_print(*args, **kwargs):
    """Print on stderr for debugging"""
    print(*args, **kwargs, file=sys.stderr)
