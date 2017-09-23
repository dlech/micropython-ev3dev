"""Utility module"""

import sys
import _thread


def _enum(**enums):
    """Create a new type that is used as an enum

    :param enums: keyword arguments giving the enum members and values
    """
    # micropython doesn't seem to have the enum(enum34) package
    # https://stackoverflow.com/a/1695250/1976323
    return type('Enum', (), enums)


def debug_print(*args, sep=' ', end='\n'):
    """Print on stderr for debugging

    Parameters:
        args: One or more arguments to print
        sep (str): Separator inserted between arguments
        end (str): Appended after the last argument
    """
    print(*args, sep=sep, end=end, file=sys.stderr)


def _thread_runner(lock, function):
    if not lock.locked():
        raise RuntimeError('Must hold lock before starting thread')
    try:
        function()
    finally:
        lock.release()


def fork(*functions):
    """Run functions in separate threads.

    This does not return until all threads have ended.

    Parameters:
        functions: one or more functions to run
    """
    locks = []
    for f in functions:
        lock = _thread.allocate_lock()
        lock.acquire()
        _thread.start_new_thread(_thread_runner, (lock, f))
        locks.append(lock)
    for l in locks:
        l.acquire()
        l.release()
