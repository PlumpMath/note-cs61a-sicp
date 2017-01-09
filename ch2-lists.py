"""Examples from lecture 12: mutable containers"""


def make_container(contents):
    """Make a container that is manipulated by two functions.

    >>> get, put = make_container('Hello')
    >>> get()
    'Hello'
    >>> put('Goodbye')
    >>> get()
    'Goodbye'
    """

    def get():
        return contents

    def put(value):
        nonlocal contents
        contents = value

    return get, put


def make_container_dispatch(contents):
    """Make a container that is manipulated by two functions.

    >>> container = make_container_dispatch('Hello')
    >>> container('get')
    'Hello'
    >>> container('put', 'Goodbye')
    >>> container('get')
    'Goodbye'
    """

    def dispatch(message, value=None):
        nonlocal contents
        if message == 'get':
            return contents
        if message == 'put':
            contents = value

    return dispatch


# Recursive list abstract data type

empty_rlist = None


def make_rlist(first, rest):
    """Make a recursive list from its first element and the rest."""
    return (first, rest)


def first(s):
    """Return the first element of a recursive list s."""
    return s[0]


def rest(s):
    """Return the rest of the elements of a recursive list s."""
    return s[1]


# Some recursive lists

counts = make_rlist(1, make_rlist(2, make_rlist(3, make_rlist(4, empty_rlist))))
alts = make_rlist(1, make_rlist(2, make_rlist(1, make_rlist(2, make_rlist(1, empty_rlist)))))


# Implementing the sequence abstraction for recursive lists

def len_rlist(s):
    """Return the length of recursive list s."""
    length = 0
    while s != empty_rlist:
        s, length = rest(s), length + 1
    return length


def getitem_rlist(s, i):
    """Return the element at index i of recursive list s."""
    while i > 0:
        s, i = rest(s), i - 1
    return first(s)


# Mutable recursive lists

def make_mutable_rlist():
    """Return a functional implementation of a mutable recursive list."""
    contents = empty_rlist

    def dispatch(message, value=None):
        nonlocal contents
        if message == 'len':
            return len_rlist(contents)
        elif message == 'getitem':
            return getitem_rlist(contents, value)
        elif message == 'push_first':
            contents = make_rlist(value, contents)
        elif message == 'pop_first':
            f = first(contents)
            contents = rest(contents)
            return f
        elif message == 'str':
            return str(contents)

    return dispatch
