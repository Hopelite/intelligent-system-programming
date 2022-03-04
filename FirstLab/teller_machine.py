from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation
from datetime import datetime
from teller_machine_exceptions import InvalidBanknoteValueException, InvalidCardNumberException, InvalidCvcException, InvalidPasswordException, NegativeMoneyAmountException, NotEnoughMoneyInStorageException, NotEnoughMoneyOnBalanceException
from data_storage import IStorage, JsonFileStorage

class Banknote:
    """Represents the banknote model."""
    def __init__(self, value: Decimal) -> None:
        self.__value = BanknoteValidator.validate_value(value)

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

class BanknoteValidator:
    @staticmethod
    def validate_value(value: Decimal) -> Decimal:
        if value <= 0:
            raise InvalidBanknoteValueException("Unable to create a banknote with value that is negative or equals zero.")
        return value

class IBanknoteStorage(ABC):
    """Contains methods for banknote storage."""
    @abstractmethod
    def get_cash_available(self) -> Decimal:
        pass

    @abstractmethod
    def withdraw_banknotes(self, amount: Decimal) -> list[Banknote]:
        pass
    
    @abstractmethod
    def deposit_banknotes(self, banknotes: list[Banknote]) -> None:
        pass

class BanknoteStorage(IBanknoteStorage):
    """Implements methods for operationing with banknotes storage."""
    def __init__(self, storage: IStorage[list[Banknote]]) -> None:
        self.__storage = storage
        
    def get_cash_available(self) -> Decimal:
        """Calculates the sum of all banknotes values in storage."""
        banknotes_dictionary = self.__storage.load()
        banknotes = self.convert_dict_to_banknotes(banknotes_dictionary)

        amount = Decimal()
        for banknote in banknotes:
            amount += banknote.value

        return amount

    def withdraw_banknotes(self, amount: Decimal) -> list[Banknote]:
        """Withdraws banknotes from storage with an amount equal specified or the closest available to it, if storage doesn't have small enough values."""
        AmountValidator.validate_amount(amount)
        if amount == 0:
            return list[Banknote]
        cash_available = self.get_cash_available()
        if cash_available < amount:
            raise NotEnoughMoneyInStorageException("There is not enough money in storage to withdraw", amount)

        banknotes_available_dictionary = self.__storage.load()
        banknotes_available = self.convert_dict_to_banknotes(banknotes_available_dictionary)

        banknotes_withdrawed = self.__make_change_algorithm(banknotes_available, amount)
        self.__storage.save(banknotes_available)
        return banknotes_withdrawed

    def __make_change_algorithm(self, banknotes_available: list[Banknote], amount: Decimal) -> list[Banknote]:
        sorted_Banknotes = sorted(banknotes_available, reverse=True)
        banknotes_withdrawed = []
        current_amount = Decimal()
        while current_amount != amount and len(sorted_Banknotes) > 0:
            current_banknote = sorted_Banknotes.pop(0)
            if current_amount + current_banknote.value <= amount:
                current_amount += current_banknote.value
                banknotes_withdrawed.append(current_banknote)
                banknotes_available.remove(current_banknote)

        return banknotes_withdrawed

    def deposit_banknotes(self, banknotes: list[Banknote]) -> None:
        """Deposits banknotes to storage."""
        banknotes_available = self.convert_dict_to_banknotes(self.__storage.load())
        banknotes_available.extend(banknotes)
        self.__storage.save(banknotes_available)

    def convert_dict_to_banknotes(self, dict) -> list[Banknote]:
        banknotes = []
        for data in dict:
            banknotes.append(Banknote(int(data)))

        return banknotes

class AmountValidator:
    @staticmethod
    def validate_amount(amount: Decimal) -> None:
        if amount < 0:
            raise NegativeMoneyAmountException("Unable to withdraw negative amount of cash.")

class ICardAccount:
    """Contains methods for card account."""
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

class BankCardValidator:
    """Contains validation methods for the BankCard."""
    @staticmethod
    def __CARD_LENGTH() -> int:
        return 16
        
    @staticmethod
    def __CVC_LENGTH() -> int:
        return 3
        
    @staticmethod
    def __PASSWORD_LENGTH() -> int:
        return 4

    @staticmethod
    def validate_card_number(card_number: str) -> str:        
        if len(card_number) != BankCardValidator.__CARD_LENGTH():
            raise InvalidCardNumberException("Card number length must equal,", BankCardValidator.__CARD_LENGTH)
        if not card_number.isnumeric():
            raise InvalidCardNumberException("Card number must contain digits only.")

        return card_number

    @staticmethod
    def validate_cvc(cvc: str) -> str:
        if len(cvc) != BankCardValidator.__CVC_LENGTH():
            raise InvalidCvcException("CVC length must equal", BankCardValidator.__CVC_LENGTH())
        if not cvc.isnumeric():
            raise InvalidCvcException("CVC must contain digits only.")

        return cvc

    @staticmethod
    def validate_password(password: str) -> str:
        if len(password) != BankCardValidator.__PASSWORD_LENGTH():
            raise InvalidPasswordException("Password length must equal", BankCardValidator.__PASSWORD_LENGTH())
        if not password.isnumeric():
            raise InvalidPasswordException("Password must contain digits only.")

        return password

class BankCard:
    """Represents bank card model."""
    def __init__(self, card_number: str, expiration_date: datetime, username: str, cvc: str, password: str, card_account: ICardAccount) -> None:
        self.__card_number = BankCardValidator.validate_card_number(card_number)
        self.__expiration_date = expiration_date
        self.__username = username
        self.__cvc = BankCardValidator.validate_cvc(cvc)
        self.__password = BankCardValidator.validate_password(password)
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

    def __str__(self) -> str:
        return "Card number: " + self.card_number + \
               "\nExpiration date: " + self.expiration_date.year.__str__() + "/" + self.expiration_date.month.__str__() + \
               "\nUser name: " + self.username + \
               "\nCVC: " + self.cvc + \
               "\nPassword: " + self.password

class ITellerMachine(ABC):
    """Contains methods for teller machine."""
    @abstractmethod
    def get_card_balance(self, card: BankCard) -> Decimal:
        pass
    
    @abstractmethod
    def withdraw_cash(self, amount: Decimal, card: BankCard) -> list[Banknote]:
        pass

    @abstractmethod
    def deposit_cash(self, cash: list[Banknote], card: BankCard) -> Decimal:
        pass

    @abstractmethod
    def pay_for_the_phone(self, phone_number: str, amount: Decimal, card: BankCard) -> None:
        pass

class TellerMachine(ITellerMachine):
    """Implements methods for operationing with teller machine."""
    def __init__(self) -> None:
        json_file_storage = JsonFileStorage[list[Banknote]]("atm_data.json")
        self.__storage = BanknoteStorage(json_file_storage)

    def get_card_balance(self, card: BankCard) -> Decimal:
        return card.card_account.view_balance()

    def withdraw_cash(self, amount: Decimal, card: BankCard) -> list[Banknote]:
        try:
            if amount < 0:
                print("You cannot withdraw negative money amount")
                return
            if card.card_account.view_balance() < amount:
                print("You haven't got enough money to withdraw.")
                return
            banknotes = self.__storage.withdraw_banknotes(amount)
            card.card_account.withdraw_cash(amount)
            return banknotes
        except NotEnoughMoneyInStorageException:
            print("Sorry, but this ATM doesn't have enough money in storage to withdraw. Please, request smaller amount.")

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

class ITellerMachineUI:
    """Contains methods for teller machine user interface."""
    @abstractmethod
    def insert_card(self, bank_card: BankCard) -> bool:
        pass
    
    @abstractmethod
    def withdraw_card(self) -> BankCard:
        pass

    @abstractmethod
    def get_card_balance(self) -> None:
        pass

    @abstractmethod
    def withdraw_cash(self) -> list[Banknote]:
        pass

    @abstractmethod
    def deposit_cash(self) -> None:
        pass
    
    @abstractmethod
    def pay_for_the_phone(self) -> None:
        pass

class TellerMachineUI:
    """Implements teller machine user interface."""
    def __init__(self, teller_machine: ITellerMachine) -> None:
        self.__teller_machine = teller_machine
        self.__card_inserted = None

    def __leave_character(self) -> str:
        return "q"

    def insert_card(self, bank_card: BankCard) -> bool:
        password = input("Enter the PIN: ")
        while bank_card.password != password:
            password = input("Invalid PIN. Try again. Enter 'q' to leave: ")
            if password == self.__leave_character():
                return False
        
        self.__card_inserted = bank_card
        print("Access granted!")
        return True

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
            banknotes_string = input("\nEnter the banknotes you want to deposit. Enter 'q' to leave: ")
            if banknotes_string == self.__leave_character():
                return
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