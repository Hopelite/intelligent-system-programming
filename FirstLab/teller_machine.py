from decimal import Decimal

# Represents the banknote model
class Banknote:
    def __init__(self, value: Decimal) -> None:
        if value <= 0:
            raise InvalidBanknoteValueException("Unable to create a banknote with value that is negative or equals zero.")
        self.__value = value

    @property
    def value(self) -> Decimal:
        return self.__value

    def __lt__(self, other):
        return self.value < other.value
        
    def __gt__(self, other):
        return self.value > other.value
        
    def __eq__(self, other):
        return self.value == other.value

# Exception raised when trying to pass invalid banknote value
class InvalidBanknoteValueException(Exception):
    pass

# Contains methods for banknote storage
class IBanknoteStorage:
    def __subclasscheck__(self, __subclass: type) -> bool:
        return (hasattr(__subclass, "get_cash_available") and callable(__subclass.get_cash_available) \
        and hasattr(__subclass, "withdraw_banknotes") and callable(__subclass.withdraw_banknotes) \
        and hasattr(__subclass, "deposit_banknotes") and callable(__subclass.deposit_banknotes))

# Implements methods for operationing with banknotes storage
class BanknoteStorage(IBanknoteStorage):
    def __init__(self, banknotes: list[Banknote] = []) -> None:
        self.__banknotes = banknotes
        
    # Calculates the sum of all banknotes values in storage 
    def get_cash_available(self) -> Decimal:
        amount = Decimal()
        for banknote in self.__banknotes:
            amount += banknote.value

        return amount

    # Withdraws banknotes from storage with an amount equal specified or the nearest available to it, if storage doesn't have small enough values
    def withdraw_banknotes(self, amount: Decimal) -> list[Banknote]:
        if amount < 0:
            raise NegativeMoneyAmountException("Unable to withdraw negative amount of cash.")
        if amount == 0:
            return list[Banknote]
        cash_available = self.get_cash_available()
        if cash_available < amount:
            raise NotEnoughMoneyException("There is not enough money in storage to withdraw", amount)

        sorted_Banknotes = sorted(self.__banknotes, reverse=True)
        banknotes_withdrawed = []
        current_amount = Decimal()
        while current_amount != amount and len(sorted_Banknotes) > 0:
            current_banknote = sorted_Banknotes.pop(0)
            if current_amount + current_banknote.value <= amount:
                current_amount += current_banknote.value
                banknotes_withdrawed.append(current_banknote)
                self.__banknotes.remove(current_banknote)
        
        return banknotes_withdrawed

    # Deposits banknotes to storage
    def deposit_banknotes(self, banknotes: list[Banknote]) -> None:
        self.__banknotes.extend(banknotes)

# Exception raised when trying to pass negative money amount       
class NegativeMoneyAmountException(Exception):
    pass

# Exception raised when storage doesn't have enough money to withdraw
class NotEnoughMoneyException(Exception):
    pass