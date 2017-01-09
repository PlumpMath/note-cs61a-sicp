from math import gcd
from operator import getitem

# Arithmetic


def add_rat(x, y):
    """Add rational numbers x and y."""
    nx, dx = numer(x), denom(x)
    ny, dy = numer(y), denom(y)
    return make_rat(nx * dy + ny * dx, dx * dy)


def mul_rat(x, y):
    """Multiply rational numbers x and y."""
    return make_rat(numer(x) * numer(y), denom(x) * denom(y))


def eq_rat(x, y):
    """Return whether rational numbers x and y are equal."""
    return numer(x) * denom(y) == numer(y) * denom(x)


# Constructor and selectors


def make_rat(n, d):
    """Construct a rational number x that represents n/d."""
    return n, d


def numer(x):
    """Return the numerator of rational number x."""
    return getitem(x, 0)


def denom(x):
    """Return the denominator of rational number x."""
    return getitem(x, 1)


# String conversion

def str_rat(x):
    """Return a string 'n/d' for numerator n and denominator d."""
    return '{0}/{1}'.format(numer(x), denom(x))


# Improved constructor


def make_rat(n, d):
    """Construct a rational number x that represents n/d in lowest terms."""
    g = gcd(n, d)
    return n // g, d // g


# Functional pair

def make_pair(x, y):
    """Return a functional pair."""

    def dispatch(m):
        if m == 0:
            return x
        elif m == 1:
            return y

    return dispatch


def getitem_pair(p, i):
    """Return the element at index i of pair p."""
    return p(i)
