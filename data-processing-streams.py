"""
Iterators allow for lazy generation, and are accessed only through next() method
instead of arbitrary element of the underlying sequence.
"""


# Iterators
class LetterIter:
    """
    An iterator over letters of the alphabet in ASCII order.
    >>> letter_iter = LetterIter()
    >>> letter_iter.__next__()
    'a'
    >>> letter_iter.__next__()
    'b'
    >>> next(letter_iter)
    'c'
    >>> letter_iter.__next__()
    'd'
    >>> letter_iter.__next__()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 24, in next
    StopIteration
    """

    def __init__(self, start='a', end='e'):
        self.next_letter = start
        self.end = end

    def __next__(self):
        if self.next_letter == self.end:
            raise StopIteration  # reached end of series
        letter = self.next_letter
        self.next_letter = chr(ord(letter) + 1)
        return letter


class Positives:
    """
    An iterator of infinite positive number sequence
    >>> p = Positives()
    >>> next(p)
    1
    >>> next(p)
    2
    >>> next(p)
    3
    """

    def __init__(self):
        self.next_positive = 1

    def __next__(self):
        result = self.next_positive
        self.next_positive += 1
        return result


# Iterables (An iterable returns an iterator when its __iter__ method is invoked.)
class Letters:
    """
    >>> b_to_k = Letters('b', 'k')
    >>> first_iterator = b_to_k.__iter__()
    >>> next(first_iterator)
    'b'
    >>> next(first_iterator)
    'c'
    """

    def __init__(self, start='a', end='e'):
        self.start = start
        self.end = end

    def __iter__(self):
        return LetterIter(self.start, self.end)


# The built-in `map` function takes iterable argument and return (lazy) iterators.
caps = map(lambda x: x.upper(), Letters('b', 'k'))
next(caps)

# The built-in `for` statement takes iterable object, invokes its __iter__ method,
# and then invokes __next__ method on the iterator until a StopIteration exception is raised.
for item in Letters('b', 'k'):
    print(item.upper())


# Generator (An generator is an iterator returned by a generator function which uses `yield` statement.)
def letters_generator():
    current = 'a'
    while current <= 'd'
        yield current
        current = chr(ord(current) + 1)


for l in letters_generator():
    print(l)


# Stream (A stream is a lazily computed linked list.)
# A stream stores 'how to compute the rest of the stream'.
class Stream:
    """A lazily computed linked list.
    >>> s = Stream(1, lambda : Stream(2+3, lambda : Stream(9)))
    >>> s.first
    1
    >>> s.rest.first
    5
    >>> s.rest
    Stream(5, <...>)
    """

    class empty:
        def __repr__(self):
            return 'Stream.empty'

    empty = empty()

    def __init__(self, first, compute_rest=lambda: empty):
        assert callable(compute_rest), 'compute_rest must be callable'
        self.first = first
        self._compute_rest = compute_rest
        self._rest = None

    @property
    def rest(self):
        """Return the rest of the stream, computing it if necessary."""
        if self._compute_rest is not None:
            self._rest = self._compute_rest()
            self._compute_rest = None
        return self._rest

    def __repr__(self):
        return 'Stream({0}, <...>)'.format(repr(self.first))


def integer_stream(first):
    """Represent increasing integers with stream
    >>> positives = integer_stream(1)
    >>> positives
    Stream(1, <...>)
    >>> positives.first
    1
    """
    def compute_rest():
        return integer_stream(first+1)
    return Stream(first, compute_rest)


def map_stream(fn, s):
    """Implement map on a lazily computed linked list."""
    if s is Stream.empty:
        return s
    def compute_rest():
        return map_stream(fn, s.rest)
    return Stream(fn(s.first), compute_rest)


def filter_stream(fn, s):
    """Implement filter on a lazily computed linked list."""
    if s is Stream.empty:
        return s
    def compute_rest():
        return filter_stream(fn, s.rest)
    if fn(s.first):
        return Stream(s.first, compute_rest)
    else:
        return compute_rest()

