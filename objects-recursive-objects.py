"""Implement classes of recursive data structure."""


def link_expression(s):
    if s.rest is Link.empty:
        rest = ''
    else:
        rest = ', ' + link_expression(s.rest)
    return 'Link({0}{1})'.format(s.first, rest)


class Link:
    """
    >>> s = Link(3, Link(4, Link(5)))
    >>> len(s)
    3
    >>> s[1]
    4
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __getitem__(self, i):
        if i == 0:
            return self.first
        else:
            return self.rest[i - 1]

    def __len__(self):
        return 1 + len(self.rest)

    def __repr__(self):
        return link_expression(self)


def extend_link(s, t):
    if s is Link.empty:
        return t
    else:
        return Link(s.first, extend_link(s.rest, t))


def map_link(f, s):
    if s is Link.empty:
        return s
    else:
        return Link(f(s.first), map_link(f, s.rest))


def filter_link(f, s):
    if s is Link.empty:
        return s
    elif f(s):
        return Link(f(s.first), filter_link(f, s.rest))
    else:
        return filter_link(f, s.rest)


def join_link(s, sep):
    if s is Link.empty:
        return ''
    elif s.rest is Link.empty:
        return str(s.first)
    else:
        return str(s.first) + sep + join_link(s.rest, sep)



