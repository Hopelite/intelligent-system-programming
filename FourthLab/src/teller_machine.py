from abc import ABC, abstractmethod
from decimal import Decimal
from src.persistence.banknote import Banknote
from src.persistence.bank_card import BankCard

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

class IUserInterface:
    """Base class for the user interface."""
    @abstractmethod
    def run(self):
        pass