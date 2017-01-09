"""Examples of sequences as conventional interfaces."""


def fib(k):
    """Compute the kth Fibonacci number.

    >>> fib(1)
    0
    >>> fib(2)
    1
    >>> fib(11)
    55
    """
    prev, curr = 1, 0  # curr is the first Fibonacci number.
    for _ in range(1, k):
        prev, curr = curr, prev + curr
    return curr


def iseven(n):
    return n % 2 == 0


def sum_even_fibs(n):
    """Sum the first n even Fibonacci numbers.

    >>> sum_even_fibs(11)
    44
    """
    return sum(filter(iseven, map(fib, range(1, n + 1))))


def first(s):
    return s[0]


def iscap(s):
    return len(s) > 0 and s[0].isupper()


def acronym(name):
    """Return a tuple of the letters that form the acronym for name.

    >>> acronym('University of California Berkeley')
    ('U', 'C', 'B')
    """
    return tuple(map(first, filter(iscap, name.split())))


def sum_even_fibs_gen(n):
    """Sum the first n even Fibonacci numbers.

    >>> sum_even_fibs_gen(11)
    44
    """
    return sum(fib(k) for k in range(1, n + 1) if fib(k) % 2 == 0)


def acronym_gen(name):
    """Return a tuple of the letters that form the acronym for name.

    >>> acronym_gen('University of California Berkeley')
    ('U', 'C', 'B')
    """
    return tuple(w[0] for w in name.split() if iscap(w))
