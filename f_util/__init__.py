import functools
import time


def timer(func):
    """Used for measuring the execution time."""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"{func.__class__}.{func.__name__}: {elapsed_time:0.5f} seconds")
        return value

    return wrapper_timer


def replace_multiple(s, *args):
    """Usage:
    >>> replace_multiple('hello', ('h', 'j'), ('e', 'ee'))
    >>> 'jeello'
    >>> replace_multiple('hello', ('h', 'j'), ('l', '1', 1))
    >>> 'je1lo'
    """
    for arg in args:
        match arg:
            case [str(), str()] | [str(), str(), int()]:
                s = s.replace(*arg)
            case _:
                raise TypeError(repr(arg))
    return s
