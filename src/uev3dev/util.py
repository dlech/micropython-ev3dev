"""Internal utility module"""


def enum(**enums):
    """Create a new type that is used as an enum

    :param enums: keyword arguments giving the enum members and values
    """
    # micropython doesn't seem to have the enum(enum34) package
    # https://stackoverflow.com/a/1695250/1976323
    return type('Enum', (), enums)
