from abc import abstractmethod
from decimal import Decimal
from src.persistence.banknote_storage import AmountValidator, NegativeMoneyAmountException

class ICardAccount:
    """Contains methods for the card account."""
    @abstractmethod
    def withdraw_cash(self, amount: Decimal) -> None:
        pass

    @abstractmethod
    def deposit_cash(self, amount: Decimal) -> None:
        pass

    @abstractmethod
    def view_balance(self) -> Decimal:
        pass

class CardAccount(ICardAccount):
    """Represents the card account."""
    def __init__(self) -> None:
        self.__balance = Decimal()

    @property
    def balance(self) -> Decimal:
        return self.__balance
    
    def withdraw_cash(self, amount: Decimal) -> None:
        AmountValidator.validate_amount(amount)
        if self.balance - amount < 0:
            raise NotEnoughMoneyOnBalanceException("Card balance doesn't have", amount, "money to withdraw.")
        self.__balance -= amount

    def deposit_cash(self, amount: Decimal) -> None:
        if amount < 0:
            raise NegativeMoneyAmountException("Unable to deposit negative amount of cash.")
        self.__balance += amount

    def view_balance(self) -> Decimal:
        return self.__balance

class NotEnoughMoneyOnBalanceException(Exception):
    """Exception raised when storage doesn't have enough money to withdraw."""
    pass