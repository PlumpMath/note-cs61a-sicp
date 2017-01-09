# example 1, convert a word to its pig latin
def pig_latin(w):
    """returns pig latin of the word w"""
    if starts_with_vowel(w):
        return w + 'ay'
    return pig_latin(w[1:] + w[0])


def starts_with_vowel(w):
    """returns true if w starts with a vowel"""
    return True if w[0].lower() in 'aeiou' else False


# example 2, factorial
def fact_iter(n):
    """iterative implementation of factorial"""
    total, k = 1, 1
    while k <= n:
        total, k = total * k, k + 1
    return total


def fact(n):
    """recursive implementation of factorial"""
    return 1 if n == 1 else n * fact(n-1)


# example 3, Fibonacci
def fib_iter(n):
    """iterative implementation of Fibonacci"""
    curr, nxt = 0, 1
    for _ in range(n-1):
        curr, nxt = nxt, curr + nxt
    return curr


def fib(n):
    """recursive implementation of Fibonacci"""
    return n-1 if n in (1, 2) else fib(n-1) + fib(n-2)


def memo(f):
    """Return a memorized version of single-argument function f."""
    cache = {}

    def memorized(n):
        if n not in cache:
            cache[n] = f(n)
        return cache[n]
    return memorized


fib = memo(fib)
assert fib(40) == 63245986


# example 4, counting change
def count_change(a, kinds=(50, 25, 10, 5, 1)):
    """Return the number of ways to change amount a using coin kinds."""
    if a == 0:
        return 1
    elif a < 0 or len(kinds) == 0:
        return 0
    d = kinds[0]
    return count_change(a, kinds[1:]) + count_change(a - d, kinds)

assert count_change(100) == 292


# example 5, exponentiation
def exp_iter(b, n):
    """iterative implementation of exponential"""
    total = 1
    for _ in range(n-1):
        total *= b
    return total


def exp(b, n):
    """recursive implementation of exponential"""
    return 1 if n == 0 else b * exp(b, n-1)


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
