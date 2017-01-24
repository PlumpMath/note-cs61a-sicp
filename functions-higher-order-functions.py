"""Definition: functions that accept other functions as arguments, or return functions as values"""


# functions as arguments
def summation(n, term):
    """Sum of terms defined by function argument"""
    return sum(term(k) for k in range(1, n + 1))


def cube(x):
    return x ** 3


def identity(x):
    return x


def pi_term(x):
    return 8 / ((4 * x - 3) * (4 * x - 1))


def sum_cubes(n):
    return summation(n, cube)


def sum_identity(n):
    return summation(n, identity)


def sum_pi(n):
    return summation(n, pi_term)


# functions as general methods
def improve(update, close, guess=1):
    """A template of iterative improvement algorithm"""
    while not close(guess):
        guess = update(guess)
    return guess


def golden_update(guess):
    return 1 / guess + 1


def square_close_to_successor(guess):
    return approx_eq(guess ** 2, guess + 1)


def approx_eq(x, y, tolerance=1e-15):
    return abs(x - y) < tolerance


def improve_test():
    """Validation with an exact closed-form solution"""
    from math import sqrt
    phi = 1 / 2 + sqrt(5) / 2
    approx_phi = improve(golden_update, square_close_to_successor)
    assert approx_eq(phi, approx_phi)


def sqrt_approx(a):
    """Square root implemented with improve algorithm"""

    def sqrt_update(x):
        return (x + a) / 2

    def sqrt_close(x):
        return approx_eq(x * x, a)

    return improve(sqrt_update, sqrt_close)


# functions as returned values
def compose1(f, g):
    """Composing 2 functions by defining a new function"""

    def h(x):
        return f(g(x))

    return h


def newton_update(f, df):
    """Return an update function of Newton's Method"""

    def update(x):
        return x - f(x) / df(x)

    return update


def find_zero(f, df):
    """Return the root of function f, with df as its derivative function"""

    def near_zero(x):
        return approx_eq(f(x), 0)

    return improve(newton_update(f, df), near_zero)


def square_root_newton(a):
    """Find the root of x*x"""

    def f(x):
        return x * x - a

    def df(x):
        return 2 * x

    return find_zero(f, df)


def nth_root_of_a(n, a):
    """Find the root of power"""

    def f(x):
        return x ** n - a

    def df(x):
        return n * x ** (n - 1)

    return find_zero(f, df)


# Lambda expressions
def compose(f, g):
    return lambda x: f(g(x))


# Function decorators
def trace(fn):
    def wrapped(x):
        print('-> ', fn, '(', x, ')')
        return fn(x)

    return wrapped


# the name triple is bound to the returned function value of calling trace on the
# newly created triple function, which is equivalent to triple = trace(triple)
@trace
def triple(x):
    return 3 * x


triple(12)
