# String manipulation
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
