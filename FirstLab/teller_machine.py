from abc import abstractclassmethod
from decimal import Decimal, InvalidOperation
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

    def __str__(self) -> str:
        return self.value.__str__()

    def __lt__(self, other) -> bool:
        return self.value < other.value
        
    def __gt__(self, other) -> bool:
        return self.value > other.value
        
    def __eq__(self, other) -> bool:
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
    def __CARD_LENGTH(self) -> int:
        return 16
        
    @property
    def __CVC_LENGTH(self) -> int:
        return 3
        
    @property
    def __PASSWORD_LENGTH(self) -> int:
        return 4

    def __str__(self) -> str:
        return "Card number: " + self.card_number + \
               "\nExpiration date: " + self.expiration_date.year.__str__() + "/" + self.expiration_date.month.__str__() + \
               "\nUser name: " + self.username + \
               "\nCVC: " + self.cvc + \
               "\nPassword: " + self.password

    def __validate_card_number(self, card_number: str) -> str:        
        if len(card_number) != self.__CARD_LENGTH   :
            raise InvalidCardNumberException("Card number length must equal,", self.__CARD_LENGTH)
        if not card_number.isnumeric():
            raise InvalidCardNumberException("Card number must contain digits only.")

        return card_number

    def __validate_cvc(self, cvc: str) -> str:
        if len(cvc) != self.__CVC_LENGTH:
            raise InvalidCvcException("CVC length must equal", self.__CVC_LENGTH)
        if not cvc.isnumeric():
            raise InvalidCvcException("CVC must contain digits only.")

        return cvc

    def __validate_password(self, password: str) -> str:
        if len(password) != self.__PASSWORD_LENGTH:
            raise InvalidPasswordException("Password length must equal", self.__PASSWORD_LENGTH)
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
    def deposit_cash(self, cash: list[Banknote], card: BankCard) -> Decimal:
        pass

    @abstractclassmethod
    def pay_for_the_phone(self, phone_number: str, amount: Decimal, card: BankCard) -> None:
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

    def deposit_cash(self, cash: list[Banknote], card: BankCard) -> Decimal:
        self.__storage.deposit_banknotes(cash)
        amount = self.__calculate_cash_amount(cash)
        card.card_account.deposit_cash(amount)
        return amount

    def pay_for_the_phone(self, phone_number: str, amount: Decimal, card: BankCard) -> None:
        if self.get_card_balance(card) < amount:
            print("You haven't got enough money.")
        else:
            card.card_account.withdraw_cash(amount)
            print("Successfully paid for the phone.")

    def __calculate_cash_amount(self, banknotes: list[Banknote]) -> Decimal:
        cash = Decimal()
        for banknote in banknotes:
            cash += banknote.value

        return cash

# Contains methods for teller machine user interface
class ITellerMachineUI:
    @abstractclassmethod
    def insert_card(self, bank_card: BankCard) -> None:
        pass
    
    @abstractclassmethod
    def withdraw_card(self) -> BankCard:
        pass

    @abstractclassmethod
    def get_card_balance(self) -> None:
        pass

    @abstractclassmethod
    def withdraw_cash(self) -> list[Banknote]:
        pass

    @abstractclassmethod
    def deposit_cash(self) -> None:
        pass
    
    @abstractclassmethod
    def pay_for_the_phone(self) -> None:
        pass

# Implements teller machine user interface
class TellerMachineUI:
    def __init__(self, teller_machine: ITellerMachine) -> None:
        self.__teller_machine = teller_machine
        self.__card_inserted = None

    def insert_card(self, bank_card: BankCard) -> None:
        password = input("Enter the PIN: ")
        while bank_card.password != password:
            password = input("Invalid PIN. Try again: ")
        
        self.__card_inserted = bank_card
        print("Access granted!")

    def withdraw_card(self) -> BankCard:
        if self.__card_inserted == None:
            print("ATM has no card inserted.")

        card = self.__card_inserted
        self.__card_inserted = None
        return card

    def get_card_balance(self) -> None:
        if self.__card_inserted == None:
            print("ATM has no card inserted.")
        else:
            print("Your card balance: ", self.__teller_machine.get_card_balance(self.__card_inserted))

    def withdraw_cash(self) -> list[Banknote]:
        amount = Decimal(input("Enter the amount of cash you want to withdraw: "))
        if self.__card_inserted == None:
            print("ATM has no card inserted.")
            return []
        else:
            return self.__teller_machine.withdraw_cash(amount, self.__card_inserted)
    
    def deposit_cash(self) -> None:
        if self.__card_inserted == None:
            print("ATM has no card inserted.")
        else:
            banknotes_string = input("\nEnter the banknotes you want to deposit: ")
            try:
                banknotes = self.__str_to_banknotes(banknotes_string)
            except InvalidOperation:
                print("Invalid banknote value passed. Please, specify only numeric values.")
                return self.deposit_cash()
            except InvalidBanknoteValueException:
                print("Invalid banknote value passed. Please, specify only positive numeric values.")
                return self.deposit_cash()

            deposited = self.__teller_machine.deposit_cash(banknotes, self.__card_inserted)
            print("Successfully deposited", deposited)

    def pay_for_the_phone(self) -> None:
        if self.__card_inserted == None:
            print("ATM has no card inserted.")
        else:
            phone_number = input("Enter phone number: ")
            amount = Decimal(input("Enter the amount of cash you want to pay: "))
            self.__teller_machine.pay_for_the_phone(phone_number, amount, self.__card_inserted)

    def __str_to_banknotes(self, string: str) -> list[Banknote]:
        string_values = string.split()
        banknotes = []
        for value in string_values:
            banknotes.append(Banknote(Decimal(value)))

        return banknotes