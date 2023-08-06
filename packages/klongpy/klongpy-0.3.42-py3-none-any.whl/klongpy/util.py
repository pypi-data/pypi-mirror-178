
import numpy as np


def die(m):
    raise RuntimeError(m)


def is_empty(a):
    return is_iterable(a) and len(a) == 0


def is_list(x):
    return isinstance(x,(list, np.ndarray))


def is_iterable(x):
    return is_list(x) or isinstance(x,str)


def to_list(a):
    return a if isinstance(a, list) else a.tolist() if isinstance(a, np.ndarray) else [a]


def is_float(x):
    try:
        b = isinstance(x, (np.floating, float))
        if not b:
            float(x)
            b = True
        return b
    except:
        return False


def is_integer(x):
    try:
        b = isinstance(x, (np.integer, int))
        if not b:
            int(x)
            b = True
        return b
    except:
        return False


def is_number(a):
    return is_integer(a) or is_float(a)


def in_map(x, v):
    try:
        return x in v
    except:
        return False


def is_alpha(x):
    return isinstance(x, str) and x.isalpha()


def is_char(x):
    # TODO: add KGChar
    return isinstance(x, str) and len(x) == 1


def cpeek(t, i,c):
    return t[i] == c if i < len(t) else False


def cmatch(t, i, c):
    return i < len(t) and t[i] == c


def cexpect(t, i, c):
    assert cmatch(t, i, c)
    return i + 1


def safe_eq(a,b):
    return isinstance(a,type(b)) and a == b
