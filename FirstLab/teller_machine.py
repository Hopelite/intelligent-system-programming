from abc import abstractclassmethod
from decimal import Decimal
from datetime import datetime

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
    @abstractclassmethod
    def get_cash_available(self) -> Decimal:
        pass

    @abstractclassmethod
    def withdraw_banknotes(self, amount: Decimal) -> list[Banknote]:
        pass
    
    @abstractclassmethod
    def deposit_banknotes(self, banknotes: list[Banknote]) -> None:
        pass

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
            raise NotEnoughMoneyInStorageException("There is not enough money in storage to withdraw", amount)

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
class NotEnoughMoneyInStorageException(Exception):
    pass

# Contains methods for card account
class ICardAccount:
    @abstractclassmethod
    def withdraw_cash(self, amount: Decimal) -> None:
        pass

    @abstractclassmethod
    def deposit_cash(self, amount: Decimal) -> None:
        pass

    @abstractclassmethod
    def view_balance(self) -> Decimal:
        pass

# Represents the card account
class CardAccount(ICardAccount):
    def __init__(self) -> None:
        self.__balance = Decimal()

    @property
    def balance(self) -> Decimal:
        return self.__balance
    
    def withdraw_cash(self, amount: Decimal) -> None:
        if amount < 0:
            raise NegativeMoneyAmountException("Unable to withdraw negative amount of cash.")
        if self.balance - amount < 0:
            raise NotEnoughMoneyOnBalanceException("Card balance doesn't have", amount, "money to withdraw.")
        self.__balance -= amount

    def deposit_cash(self, amount: Decimal) -> None:
        if amount < 0:
            raise NegativeMoneyAmountException("Unable to deposit negative amount of cash.")
        self.__balance += amount

    def view_balance(self) -> Decimal:
        return self.__balance

# Exception raised when storage doesn't have enough money to withdraw
class NotEnoughMoneyOnBalanceException(Exception):
    pass

# Represents bank card model
class BankCard:
    def __init__(self, card_number: str, expiration_date: datetime, username: str, cvc: str, password: str, card_account: ICardAccount) -> None:
        self.__card_number = self.__validate_card_number(card_number)
        self.__expiration_date = expiration_date
        self.__username = username
        self.__cvc = self.__validate_cvc(cvc)
        self.__password = self.__validate_password(password)
        self.__card_account = card_account

    @property
    def card_number(self) -> str:
        return self.__card_number
        
    @property
    def expiration_date(self) -> datetime:
        return self.__expiration_date
        
    @property
    def username(self) -> str:
        return self.__username
        
    @property
    def cvc(self) -> str:
        return self.__cvc
        
    @property
    def password(self) -> str:
        return self.__password
        
    @property
    def card_account(self) -> CardAccount:
        return self.__card_account

    @property
    def CARD_LENGTH(self):
        return 16
        
    @property
    def CVC_LENGTH(self):
        return 3
        
    @property
    def PASSWORD_LENGTH(self):
        return 4

    def __validate_card_number(self, card_number: str) -> str:        
        if len(card_number) != self.CARD_LENGTH:
            raise InvalidCardNumberException("Card number length must equal,", self.CARD_LENGTH)
        if not card_number.isnumeric():
            raise InvalidCardNumberException("Card number must contain digits only.")

        return card_number

    def __validate_cvc(self, cvc: str) -> str:
        if len(cvc) != self.CVC_LENGTH:
            raise InvalidCvcException("CVC length must equal", self.CVC_LENGTH)
        if not cvc.isnumeric():
            raise InvalidCvcException("CVC must contain digits only.")

        return cvc

    def __validate_password(self, password: str) -> str:
        if len(password) != self.PASSWORD_LENGTH:
            raise InvalidPasswordException("Password length must equal", self.PASSWORD_LENGTH)
        if not password.isnumeric():
            raise InvalidPasswordException("Password must contain digits only.")

        return password

# Exception raised when trying to pass invalid card number
class InvalidCardNumberException(Exception):
    pass

# Exception raised when trying to pass invalid CVC
class InvalidCvcException(Exception):
    pass

# Exception raised when trying to pass invalid password
class InvalidPasswordException(Exception):
    pass

# Contains methods for teller machine
class ITellerMachine:
    @abstractclassmethod
    def get_card_balance(self, card: BankCard) -> Decimal:
        pass

    @abstractclassmethod
    def withdraw_cash(self, amount: Decimal, card: BankCard) -> list[Banknote]:
        pass

    @abstractclassmethod
    def deposit_cash(self, cash: list[Banknote], card: BankCard) -> None:
        pass

# Implements methods for operationing with teller machine
class TellerMachine(ITellerMachine):
    def __init__(self, initial_cash: list[Banknote] = []) -> None:
        self.__storage = BanknoteStorage(initial_cash)

    def get_card_balance(self, card: BankCard) -> Decimal:
        return card.card_account.view_balance()

    def withdraw_cash(self, amount: Decimal, card: BankCard) -> list[Banknote]:
        try:
            banknotes = self.__storage.withdraw_banknotes(amount)
            card.card_account.withdraw_cash(amount)
            return banknotes
        except NegativeMoneyAmountException:
            print("You cannot withdraw negative money amount")
        except NotEnoughMoneyInStorageException:
            print("Sorry, but this ATM doesn't have enough money in storage to withdraw. Please, request smaller amount.")
        except NotEnoughMoneyOnBalanceException:
            print("You haven't got enough money to withdraw.")

    def deposit_cash(self, cash: list[Banknote], card: BankCard) -> None:
        self.__storage.deposit_banknotes(cash)
        amount = self.__calculate_cash_amount(cash)
        card.card_account.deposit_cash(amount)

    def __calculate_cash_amount(self, banknotes: list[Banknote]) -> Decimal:
        cash = Decimal()
        for banknote in banknotes:
            cash += banknote.value

        return cash