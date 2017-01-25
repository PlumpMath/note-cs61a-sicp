"""Example of Classes and Objects."""


class Account:
    # class names are conventionally written using the CapWords convention
    """A bank account."""
    # class attribute, shared among all instances
    # attribute lookup priorities: 1. instance attributes, 2. class attributes, 3. class methods
    interest = 0.02

    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return "insufficient balance"
        else:
            self.balance -= amount
            return self.balance


class CheckingAccount(Account):
    """A bank account that charges for withdrawals."""
    withdraw_charge = 1
    interest = 0.01

    # method lookup priorities: 1. in the class, 2. in the base class
    def withdraw(self, amount):
        return Account.withdraw(self, amount + self.withdraw_charge)  # calling ancestors


def checking_account_test():
    checking = CheckingAccount('Sam')
    checking.deposit(10)
    assert checking.withdraw(5) == 4
    assert checking.interest == 0.01


class SavingsAccount(Account):
    """A bank account that charges for deposits"""
    deposit_charge = 2

    def deposit(self, amount):
        return Account.deposit(self, amount - self.deposit_charge)


class AsSeenOnTVAccount(CheckingAccount, SavingsAccount):
    """multi-inheritance from 2 subclasses of Account"""
    def __init__(self, account_holder):
        self.holder = account_holder
        self.balance = 1  # A free dollar!


def as_seen_on_tv_account_test():
    such_a_deal = AsSeenOnTVAccount("John")
    assert such_a_deal.balance == 1
    # print scanning order: AsSeenOnTVAccount, CheckingAccount, SavingsAccount, Account
    print([c.__name__ for c in AsSeenOnTVAccount.mro()])
    assert such_a_deal.deposit(20) == 19
    assert such_a_deal.withdraw(5) == 13

