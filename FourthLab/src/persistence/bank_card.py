import json
from enum import Enum
from datetime import datetime
from decimal import Decimal
from src.persistence.card_account import ICardAccount, CardAccount

class BankCardValidator:
    """Contains validation methods for BankCard."""
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

class CardState(Enum):
    BLOCKED = 1
    OPENED = 2
    CLOSED = 3

class BankCard:
    """Represents bank card model."""
    NUMBER_OF_ATTEMPS = 3
    __attemps_count: int

    def __init__(self, card_number: str, expiration_date: datetime, username: str, cvc: str, password: str, card_account: ICardAccount) -> None:
        self.__card_number = BankCardValidator.validate_card_number(card_number)
        self.__expiration_date = expiration_date
        self.__username = username
        self.__cvc = BankCardValidator.validate_cvc(cvc)
        self.__password = BankCardValidator.validate_password(password)
        self.__card_account = card_account
        self.__attemps_count = 0 
        self.__state = CardState.CLOSED

    @staticmethod
    def load_from_file(card_file_path: str):
        with open(card_file_path) as file:
            return json.load(file, object_hook=BankCard.from_json)

    def save_to_file(self, card_file_path: str) -> None:
        with open(card_file_path, "w") as file:
            json.dump(self.to_json(), file, indent=4)

    def get_card_balance(self) -> Decimal:
        return self.card_account.balance

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
    def attempts_left(self) -> str:
        return (self.NUMBER_OF_ATTEMPS - self.__attemps_count).__str__()
        
    @property
    def state(self) -> CardState:
        return self.__state

    def is_access_gained(self) -> bool:
        return self.state == CardState.OPENED

    def gain_access(self, password: str) -> CardState:
        if self.__state == CardState.BLOCKED:
            return self.__state

        if password == self.password:
            self.__state = CardState.OPENED
        else:
            self.__attemps_count += 1
            if self.__attemps_count == self.NUMBER_OF_ATTEMPS:
                self.__state = CardState.BLOCKED
            else:
                self.__state = CardState.CLOSED

        return self.__state
            
    def withdraw_cash(self, amount: Decimal) -> None:
        self.card_account.withdraw_cash(amount)
        
    def deposit_cash(self, amount: Decimal) -> None:
        self.card_account.deposit_cash(amount)

    @staticmethod
    def from_json(json_dct):
        account = CardAccount()
        account.deposit_cash(Decimal(json_dct['balance']))
        return BankCard(json_dct['card_number'],
                        datetime.strptime(json_dct['expiration_date'], '%d-%m-%Y').date(),
                        json_dct['username'],
                        json_dct['cvc'],
                        json_dct['password'],
                        account)
                        
    def __iter__(self):
        yield from {
            "card_number": self.card_number,
            "expiration_date": self.expiration_date.strftime('%d-%m-%Y'),
            "username": self.username,
            "cvc": self.cvc,
            "password": self.password,
            "balance": self.card_account.balance.__str__()
        }.items()

    def to_json(self):
        return dict(self)

    def __str__(self) -> str:
        return "Card number: " + self.card_number + \
               "\nExpiration date: " + self.expiration_date.year.__str__() + "/" + self.expiration_date.month.__str__() + \
               "\nUser name: " + self.username + \
               "\nCVC: " + self.cvc + \
               "\nPassword: " + self.password

class InvalidCardNumberException(Exception):
    """Exception raised when trying to pass invalid card number."""
    pass

class InvalidCvcException(Exception):
    """Exception raised when trying to pass invalid CVC."""
    pass

class InvalidPasswordException(Exception):
    """Exception raised when trying to pass invalid password."""
    pass