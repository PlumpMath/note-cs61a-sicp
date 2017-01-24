"""Any recursive function is composed of a base case and one or more recursive calls"""


# example, sum of digits
def sum_digits(x):
    """Return sum of the digits of a positive integer x"""
    return x if x < 10 else x % 10 + sum_digits(x // 10)


# example, factorial
def fact_iter(n):
    """Iterative algorithm for factorial"""
    total, k = 1, 1
    while k <= n:
        total, k = total * k, k + 1
    return total


def fact(n):
    """Recursive algorithm for factorial"""
    return 1 if n in (0, 1) else n * fact(n - 1)


# example, even / odd
def is_even(n):
    """Return True if n is even"""
    if n == 0:
        return True
    else:
        if (n - 1) == 0:
            return False
        else:
            return is_even((n - 2))


# example, Fibonacci
def fib_iter(n):
    """Iterative algorithm for Fibonacci"""
    curr, nex = 0, 1
    for _ in range(n - 1):
        curr, nex = nex, curr + nex
    return curr


def fib(n):
    """Recursive algorithm for Fibonacci"""
    # the definition is compact, however order of growth ~ O(1.6^n)
    return (n - 1) if n in (1, 2) else fib(n - 1) + fib(n - 2)


def memo(fn):
    """Return a memorized version of function fn"""
    cache = {}

    def memorized(n):
        if n not in cache:
            cache[n] = fn(n)
        return cache[n]

    return memorized

fib = memo(fib)  # the recursive called function
assert fib(40) == 63245986


# example, counting change
def count_change(a, kinds=(50, 25, 10, 5, 1)):
    """Return the number of ways to change amount a using coin kinds"""
    if a == 0:
        return 1
    elif a < 0 or len(kinds) == 0:
        return 0
    d = kinds[0]
    return count_change(a, kinds[1:]) + count_change(a - d, kinds)

assert count_change(100) == 292


# example, exponentiation
def square(x):
    return x * x


def fast_exp(b, n):
    """exponential with O(log n) order of growth"""
    if n == 0:
        return 1
    if n % 2 == 0:
        return square(fast_exp(b, n/2))
    else:
        return b * fast_exp(b, n-1)
