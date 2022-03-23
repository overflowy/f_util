import functools
import logging
import sys
import time
from configparser import ConfigParser


def get_config(config_path):
    config = ConfigParser(allow_no_value=True)
    config.read(config_path)
    return config


def setup_logging(log_path, level=logging.DEBUG, except_hook=False):
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s::%(levelname)s::%(module)s::%(funcName)s::%(message)s",
        handlers=[logging.FileHandler(log_path, mode="a"), stdout_handler],
    )

    def handle_exception(exc_type, exc_value, exc_traceback):
        logger = logging.getLogger(__name__)
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    if except_hook:
        sys.excepthook = handle_exception


def timer(func):
    """Used for measuring the execution time."""

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"{func.__class__}.{func.__name__}: {elapsed_time:0.5f} seconds")
        return value

    return wrapped


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
