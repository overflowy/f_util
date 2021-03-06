import functools
import logging
import sys
import time
from configparser import ConfigParser
from pathlib import Path
from shutil import rmtree


def get_config(config_path):
    config = ConfigParser(allow_no_value=True)
    config.read(config_path)
    return config


def setup_logging(log_path, level=logging.DEBUG, except_hook=False, mode="a", stdout=False):
    handlers = [logging.FileHandler(log_path, mode=mode)]
    if stdout:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        handlers.append(stdout_handler)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s::%(levelname)s::%(module)s::%(funcName)s::%(message)s",
        handlers=handlers,
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


def remove_path(path):
    logger = logging.getLogger(__name__)
    path = Path(path)
    if path.is_file() or path.is_symlink():
        path.unlink()
        logger.info(f"Removed {path.absolute}")
    elif path.is_dir():
        rmtree(path)
        logger.info(f"Removed {path.absolute}")
    else:
        raise RuntimeError("Could not remove path.")


def remove_older_than(path, days=3):
    logger = logging.getLogger(__name__)
    path = Path(path)
    if not path.is_dir():
        raise TypeError("Path must directory.")
    to_compare = time.time() - days * 86400
    for item in path.iterdir():
        if item.stat().st_mtime < to_compare:
            remove_path(item)
            logger.info(f"Removed {item}")


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


def replace_in_file(path, *args):
    with open(path, "r") as f:
        text = f.read()
    for arg in args:
        match arg:
            case [str(), str()] | [str(), str(), int()]:
                text = text.replace(*arg)
            case _:
                raise TypeError(repr(arg))
    with open(path, "w") as f:
        f.write(text)


def sort_and_prioritize(lst, to_prioritize):
    """Usage:
    >>> sort_and_prioritize(["B", "C", "D", "A", "F", "E"], ["C", "D"])
    >>> ['C', 'D', 'A', 'B', 'E', 'F']
    """
    queue = [lst.pop(lst.index(item)) for item in to_prioritize]
    lst = sorted(lst)
    for item in sorted(queue, reverse=True):
        lst.insert(0, item)
    return lst


def flip_dict(d):
    flipped = {}

    for k, v in d.items():
        if v not in flipped:
            flipped[v] = [k]
        else:
            flipped[v].append(k)

    return flipped


def get_duplicate_values_from_dict(d):
    return {k: v for k, v in flip_dict(d).items() if len(v) > 1}
