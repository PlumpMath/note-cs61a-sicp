"""Constructing an abstraction for rational number."""

from math import gcd


# Define operations
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


# Construct a rational with a tuple
def make_rat(n, d):
    """Construct a rational number x that represents n/d."""
    return n, d


def numer(x):
    """Return the numerator of rational number x."""
    return x[0]


def denom(x):
    """Return the denominator of rational number x."""
    return x[1]


# Print function
def print_rat(x):
    """Return a string 'n/d' for numerator n and denominator d."""
    print(numer(x), '/', denom(x))


# Improved constructor
def make_rat(n, d):
    """Construct a rational number x that represents n/d in lowest terms."""
    g = gcd(n, d)
    return n // g, d // g


# Functional pair
def make_pair(x, y):
    """Return a function that represents a pair."""

    def get(m):
        if m == 0:
            return x
        elif m == 1:
            return y

    return get


def select(p, i):
    """Return the element at index i of pair p."""
    return p(i)
