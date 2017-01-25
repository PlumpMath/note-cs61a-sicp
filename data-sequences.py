"""Tree and Linked list data structures."""


# Construct a tree with built-in lists
def tree(root, branches=[]):
    """Construct a tree, usually by nested expressions
    >>> t = tree(3, [tree(1), tree(2, [tree(1), tree(1)])])
    >>> t
    [3, [1], [2, [1], [1]]]
    >>> root(t)
    3
    >>> is_leaf(t)
    False
    """
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [root] + list(branches)


def root(tree):
    return tree[0]


def branches(tree):
    return tree[1:]


def is_tree(tree):
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True


def is_leaf(tree):
    """Checks whether or not a tree has branches."""
    return not branches(tree)


def count_leaves(tree):
    """Count leaves of a tree."""
    return 1 if is_leaf(tree) else sum([count_leaves(b) for b in branches(tree)])


# Linked lists
# Define linked lists
empty = 'empty'


def is_link(s):
    """s is a linked list if it is empty or a (first, rest) pair."""
    return s == empty or (len(s) == 2 and is_link(s[1]))


def link(first, rest):
    """Construct a linked list."""
    assert is_link(rest)
    return [first, rest]


def first(s):
    """Return the first element of a linked list s."""
    assert is_link(s)
    assert s != empty
    return s[0]


def rest(s):
    """Return the rest of a linked list s."""
    assert is_link(s)
    assert s != empty
    return s[1]


# Attributes / Methods of linked lists
def len_link(s):
    """Return the length of linked list s."""
    assert is_link(s)
    return 0 if s == empty else 1 + len_link(s.rest)


def getitem_link(s, i):
    """Return the element at index i of linked list s."""
    return first(s) if i == 0 else getitem_link(rest(s), i - 1)


def extend_link(s, t):
    """Append linked list t to linked list s."""
    assert is_link(s) and is_link(t)
    if s == empty:
        return t
    else:
        return link(first(s), extend_link(rest(s), t))


def apply_to_all_link(fn, s):
    """Apply function fn to all elements of linked list s."""
    assert is_link(s)
    if s == empty:
        return s
    else:
        return link(fn(s), apply_to_all_link(fn, rest(s)))


def keep_if_link(fn, s):
    """Apply filter fn to all elements of linked list s."""
    assert is_link(s)
    if s == empty:
        return s
    elif fn(s.first):
        return link(first(s), keep_if_link(fn, rest(s)))
    else:
        return keep_if_link(fn, rest(s))


def join_link(s, sep):
    """Return a string concatenating all elements of linked list s."""
    assert is_link(s)
    if s == empty:
        return ""
    elif rest(s) == empty:
        return str(s)
    else:
        return str(first(s)) + sep + join_link(rest(s), sep)


def link_test():
    four = link(1, link(2, link(3, link(4, empty))))
    assert first(four) == 1
    assert rest(four) == [2, [3, [4, 'empty']]]
    assert len_link(four) == 4
    assert getitem_link(four, 1) == 2
    assert extend_link(four, four) == [1, [2, [3, [4, [1, [2, [3, [4, 'empty']]]]]]]]
    assert apply_to_all_link(lambda x: x * x, four) == [1, [4, [9, [16, 'empty']]]]
    assert keep_if_link(lambda x: x % 2 == 0, four) == [2, [4, 'empty']]
    assert join_link(four, ',') == '1, 2, 3, 4'
