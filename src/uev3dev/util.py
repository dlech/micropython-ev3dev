"""Utility module"""

import sys
import time
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


class Timer():
    """Object that represents a timer"""
    def __init__(self):
        self._start_time = 0
        self.reset()

    def reset(self):
        self._start_time = time.perf_counter()

    def elapsed_time(self):
        now = time.perf_counter()
        return now - self._start_time

    def wait(self, compare, value):
        while not compare(self.elapsed_time(), 0.8):
            pass


def write_at_index(array, index, value):
    """Creates a copy of an array with the value at ``index`` set to
    ``value``. The array is extended if needed.

    Parameters:
        array (tuple): The input array
        index (int): The index in the array to write to
        value (value): The value to write

    Returns:
        A new tuple containing the modified array
    """
    l = list(array)
    extend = index - len(l) + 1
    if extend > 0:
        # FIXME: this could be a logic array, in which case we should use
        # False instead of 0. But, using zero is not likely to cause problems.
        l += [0] * extend
    l[index] = value
    return tuple(l)
