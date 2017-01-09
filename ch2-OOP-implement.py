"""Lecture 16 examples: Implementing OOP"""


def make_instance(cls):
    """Return a new object instance."""

    def get_value(name):
        if name in attributes:
            return attributes[name]
        else:
            value = cls['get'](name)
            return bind_method(value, instance)

    def set_value(name, value):
        attributes[name] = value

    attributes = {}
    instance = {'get': get_value, 'set': set_value}
    return instance


def bind_method(value, instance):
    """Return value or a bound method if value is callable."""
    if callable(value):
        def method(*args):
            return value(instance, *args)

        return method
    else:
        return value


def make_class(attributes, base_class=None):
    """Return a new class.

    attributes -- class attributes
    base_class -- a dispatch dictionary representing a class
    """

    def get_value(name):
        if name in attributes:
            return attributes[name]
        elif base_class is not None:
            return base_class['get'](name)

    def set_value(name, value):
        attributes[name] = value

    def new(*args):
        return init_instance(cls, *args)

    cls = {'get': get_value, 'set': set_value, 'new': new}
    return cls


def init_instance(cls, *args):
    """Return a new instance of cls, initialized with args."""
    instance = make_instance(cls)
    init = cls['get']('__init__')
    if init:
        init(instance, *args)
    return instance


def make_account_class():
    """Return the Account class, which has deposit and withdraw methods.

    >>> jim_acct = Account['new']('Jim')
    >>> jim_acct['get']('holder')
    'Jim'
    >>> jim_acct['get']('interest')
    0.02
    >>> jim_acct['get']('deposit')(20)
    20
    >>> jim_acct['get']('withdraw')(5)
    15

    >>> jim_acct['get']('balance')
    15
    >>> jim_acct['set']('interest', 0.08)
    >>> Account['get']('interest')
    0.02
    >>> jim_acct['get']('interest')
    0.08
    """

    def __init__(self, account_holder):
        self['set']('holder', account_holder)
        self['set']('balance', 0)

    def deposit(self, amount):
        """Increase the account balance by amount and return the new balance."""
        new_balance = self['get']('balance') + amount
        self['set']('balance', new_balance)
        return self['get']('balance')

    def withdraw(self, amount):
        """Decrease the account balance by amount and return the new balance."""
        balance = self['get']('balance')
        if amount > balance:
            return 'Insufficient funds'
        self['set']('balance', balance - amount)
        return self['get']('balance')

    return make_class({'__init__': __init__,
                       'deposit': deposit,
                       'withdraw': withdraw,
                       'interest': 0.02})


Account = make_account_class()


def make_checking_account_class():
    """Return the CheckingAccount class, which imposes a $1 withdrawal fee.

    >>> jack_acct = CheckingAccount['new']('Jack')
    >>> jack_acct['get']('interest')
    0.01
    >>> jack_acct['get']('deposit')(20)
    20
    >>> jack_acct['get']('withdraw')(5)
    14
    """

    def withdraw(self, amount):
        return Account['get']('withdraw')(self, amount + 1)

    return make_class({'withdraw': withdraw, 'interest': 0.01}, Account)


CheckingAccount = make_checking_account_class()