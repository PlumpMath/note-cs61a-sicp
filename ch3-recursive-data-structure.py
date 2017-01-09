# example 1, recursive list
class Rlist(object):
    """
    A recursive list consisting of a first element and the rest.
    >>> s = Rlist(1, Rlist(2, Rlist(3)))
    >>> s.rest
    Rlist(2, Rlist(3))
    >>> len(s)
    3
    >>> s[1]
    2
    """

    class EmptyList(object):
        def __len__(self):
            return 0

    empty = EmptyList()

    def __init__(self, first, rest=empty):
        self.first = first
        self.rest = rest

    def __repr__(self):
        args = repr(self.first)
        if self.rest is not Rlist.empty:
            args += ', {0}'.format(repr(self.rest))
        return 'Rlist({0})'.format(args)

    def __len__(self):
        return 1 + len(self.rest)

    def __getitem__(self, i):
        if i == 0:
            return self.first
        return self.rest[i - 1]


def extend_rlist(s1, s2):
    """
    >>> s = Rlist(1, Rlist(2, Rlist(3)))
    >>> extend_rlist(s.rest, s)
    Rlist(2, Rlist(3, Rlist(1, Rlist(2, Rlist(3)))))
    """
    if s1 is Rlist.empty:
        return s2
    return Rlist(s1.first, extend_rlist(s1.rest, s2))


def map_rlist(s, fn):
    """
    >>> s = Rlist(1, Rlist(2, Rlist(3)))
    >>> map_rlist(s, square)
    Rlist(1, Rlist(4, Rlist(9)))
    """
    if s is Rlist.empty:
        return s
    return Rlist(fn(s.first), map_rlist(s.rest, fn))


def filter_rlist(s, fn):
    """
    >>> s = Rlist(1, Rlist(2, Rlist(3)))
    >>> filter_rlist(s, lambda x: x % 2 == 1)
    Rlist(1, Rlist(3))
    """
    if s is Rlist.empty:
        return s
    rest = filter_rlist(s.rest, fn)
    if fn(s.first):
        return Rlist(s.first, rest)
    return rest


# example 2, nested tree structure
def count_leaves(tree):
    """
    count the leave nodes of a tree structure
    >>> t = ((1, 2), 3, 4)
    >>> count_leaves(t)
    4
    >>> big_tree = ((t, t), 5)
    >>> big_tree
    ((((1, 2), 3, 4), ((1, 2), 3, 4)), 5)
    >>> count_leaves(big_tree)
    9
    """
    if type(tree) != tuple:
        return 1
    return sum(map(count_leaves, tree))


def map_tree(tree, fn):
    """
    apply function to all nodes of a tree
    >>> t = ((1, 2), 3, 4)
    >>> big_tree = ((t, t), 5)
    >>> map_tree(big_tree, square)
    ((((1, 4), 9, 16), ((1, 4), 9, 16)), 25)
    """
    if type(tree) != tuple:
        return fn(tree)
    return tuple(map_tree(branch, fn) for branch in tree)


class Tree(object):
    """a binary tree"""
    def __init__(self, entry, left=None, right=None):
        self.entry = entry
        self.left = left
        self.right = right

    def __repr__(self):
        args = repr(self.entry)
        if self.left or self.right:
            args += ', {0}, {1}'.format(repr(self.left), repr(self.right))
        return 'Tree({0})'.format(args)


def fib_tree(n):
    """
    Return a binary tree that represents a recursive Fibonacci calculation.
    >>> fib_tree(5)
    Tree(3, Tree(1, Tree(0), Tree(1)), Tree(2, Tree(1), Tree(1, Tree(0), Tree(1))))
    """
    if n == 1:
        return Tree(0)
    if n == 2:
        return Tree(1)
    left = fib_tree(n - 2)
    right = fib_tree(n - 1)
    return Tree(left.entry + right.entry, left, right)


# example 3, implementing set using unordered sequences
def empty(s):
    return s is Rlist.empty


def set_contains(s, v):
    """
    >>> s = Rlist(1, Rlist(2, Rlist(3)))
    >>> set_contains(s, 2)
    True
    >>> set_contains(s, 5)
    False
    """
    if empty(s):
        return False
    elif s.first == v:
        return True
    return set_contains(s.rest, v)


def adjoin_set(s, v):
    """
    >>> s = Rlist(1, Rlist(2, Rlist(3)))
    >>> t = adjoin_set(s, 4)
    Rlist(4, Rlist(1, Rlist(2, Rlist(3))))
    """
    return s if set_contains(s, v) else Rlist(v, s)


def intersect_set(set1, set2):
    """
    >>> s = Rlist(1, Rlist(2, Rlist(3)))
    >>> t = adjoin_set(s, 4)
    >>> intersect_set(t, map_rlist(s, lambda x: x * x))
    Rlist(4, Rlist(1))
    """
    return filter_rlist(set1, lambda v: set_contains(set2, v))


def union_set(set1, set2):
    """
    >>> s = Rlist(1, Rlist(2, Rlist(3)))
    >>> t = adjoin_set(s, 4)
    >>> union_set(t, s)
    Rlist(4, Rlist(1, Rlist(2, Rlist(3))))
    """
    set1_not_set2 = filter_rlist(set1, lambda v: not set_contains(set2, v))
    return extend_rlist(set1_not_set2, set2)


