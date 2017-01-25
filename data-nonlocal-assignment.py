"""Introduction to mutable data and non-local state"""


# nonlocal state
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
        # balance will be bound to the first frame in which balance was already defined
        # if balance has not previously been bound to a value, the nonlocal call gives an error
        nonlocal balance
        if amount > balance:
            return 'Insufficient funds'
        # no nonlocal statement is required to access a non-local name,
        # but only after a nonlocal statement can a function change the binding of names in these frames
        balance -= amount
        return balance

    return withdraw


def make_withdraw_useless(balance):
    """Only change the local state."""

    def withdraw(amount):
        # Removed the nonlocal statement
        b = balance  # Create a local binding
        if amount > b:
            return 'Insufficient funds'
        b -= amount  # Re-bind the local binding
        return b

    return withdraw
