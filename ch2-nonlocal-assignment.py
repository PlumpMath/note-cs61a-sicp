"""Lecture 11: Non-local assignment examples."""


def make_withdraw(balance):
    """Return a withdraw function that draws down balance with each call.

    >>> w = make_withdraw(100)
    >>> w(25)
    75
    >>> w(25)
    50
    >>> w(60)
    'Insufficient funds'
    """

    def withdraw(amount):
        nonlocal balance  # Declare the name "balance" nonlocal
        if amount > balance:
            return 'Insufficient funds'
        balance -= amount  # Re-bind the existing balance name
        return balance

    return withdraw


def make_withdraw_broken(balance):
    """Return a withdraw function that draws down balance with each call."""

    def withdraw(amount):
        # Removed the nonlocal statement
        if amount > balance:
            return 'Insufficient funds'
        balance -= amount  # Error!  There's no balance!
        return balance

    return withdraw


def make_withdraw_useless(balance):
    """Return a withdraw function that draws down balance with each call."""

    def withdraw(amount):
        # Removed the nonlocal statement
        b = balance  # Create a local binding
        if amount > b:
            return 'Insufficient funds'
        b -= amount  # Re-bind the local binding
        return b

    return withdraw
