def make_dict():
    """Return a functional implementation of a dictionary.

    >>> d = make_dict()
    >>> d('setitem', 'I', 1)
    >>> d('setitem', 'V', 5)
    >>> d('setitem', 'X', 10)
    >>> d('getitem', 'V')
    5
    >>> d('setitem', 'V', 'five')
    >>> d('getitem', 'V')
    'five'
    >>> len(d('keys'))
    3
    >>> 5 in d('values')
    False
    >>> 'five' in d('values')
    True
    """
    records = []

    def getitem(key):
        for k, v in records:
            if k == key:
                return v

    def setitem(key, value):
        for item in records:
            if item[0] == key:
                item[1] = value
                return
        records.append([key, value])

    def dispatch(message, key=None, value=None):
        if message == 'getitem':
            return getitem(key)
        elif message == 'setitem':
            setitem(key, value)
        elif message == 'keys':
            return tuple(k for k, _ in records)
        elif message == 'values':
            return tuple(v for _, v in records)

    return dispatch
