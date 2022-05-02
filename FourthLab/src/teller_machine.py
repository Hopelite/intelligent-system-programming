from abc import ABC, abstractmethod
from decimal import Decimal
from src.persistence.banknote_storage import IBanknoteStorage
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

class TellerMachine(ITellerMachine):
    """Implements methods for operationing with teller machine."""
    def __init__(self, banknote_storage: IBanknoteStorage) -> None:
        self.__storage = banknote_storage

    def get_card_balance(self, card: BankCard) -> Decimal:
        return card.card_account.view_balance()

    def withdraw_cash(self, amount: Decimal, card: BankCard) -> list[Banknote]:
        banknotes = self.__storage.withdraw_banknotes(amount)
        card.card_account.withdraw_cash(amount)
        return banknotes

    def deposit_cash(self, cash: list[Banknote], card: BankCard) -> Decimal:
        self.__storage.deposit_banknotes(cash)
        amount = self.__calculate_cash_amount(cash)
        card.card_account.deposit_cash(amount)
        return amount

    def pay_for_the_phone(self, phone_number: str, amount: Decimal, card: BankCard) -> None:
        card.card_account.withdraw_cash(amount)

    def __calculate_cash_amount(self, banknotes: list[Banknote]) -> Decimal:
        cash = Decimal()
        for banknote in banknotes:
            cash += banknote.value

        return cash