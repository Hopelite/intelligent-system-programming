from abc import ABC, abstractmethod
from src.persistence.data_storage import IStorage, JsonFileStorage
from decimal import Decimal
from src.persistence.banknote import Banknote 

class IBanknoteStorage(ABC):
    """Contains methods for banknote storage."""
    @abstractmethod
    def get_cash_available(self) -> Decimal:
        """Calculates the sum of all banknotes values in storage."""
        pass

    @abstractmethod
    def withdraw_banknotes(self, amount: Decimal) -> list[Banknote]:
        """Withdraws banknotes from storage with an amount equal specified or the closest available to it, if storage doesn't have small enough values."""
        pass
    
    @abstractmethod
    def deposit_banknotes(self, banknotes: list[Banknote]) -> None:
        """Deposits banknotes to storage."""
        pass
    
class JsonFileBanknoteStorage(IStorage[list[Banknote]]):
    """Decorates JsonFileStorage so it's able to convert string to banknotes."""
    def __init__(self, storage: JsonFileStorage[list[Banknote]]) -> None:
        self.__storage = storage

    def save(self, data: list[Banknote]) -> None:
        self.__storage.save(data)

    def load(self) -> Decimal:
        banknotes_dictionary = self.__storage.load()
        return self.__convert_dict_to_banknotes(banknotes_dictionary)
        
    def __convert_dict_to_banknotes(self, dict) -> list[Banknote]:
        banknotes = []
        for data in dict:
            banknotes.append(Banknote(int(data)))

        return banknotes

class BanknoteStorage(IBanknoteStorage):
    """Implements methods for operationing with banknotes storage."""
    def __init__(self, storage: IStorage[list[Banknote]]) -> None:
        self.__storage = storage
        
    def get_cash_available(self) -> Decimal:        
        banknotes = self.__storage.load()

        amount = Decimal()
        for banknote in banknotes:
            amount += banknote.value

        return amount

    def withdraw_banknotes(self, amount: Decimal) -> list[Banknote]:
        AmountValidator.validate_amount(amount)
        if amount == 0:
            return list[Banknote]

        cash_available = self.get_cash_available()
        if cash_available < amount:
            raise NotEnoughMoneyInStorageException("There is not enough money in storage to withdraw", amount)

        banknotes_available = self.__storage.load()

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
        banknotes_available = self.__storage.load()
        banknotes_available.extend(banknotes)
        self.__storage.save(banknotes_available)
        
class AmountValidator:
    @staticmethod
    def validate_amount(amount: Decimal) -> None:
        if amount < 0:
            raise NegativeMoneyAmountException("Unable to withdraw negative amount of cash.")
       
class NegativeMoneyAmountException(Exception):
    """Exception raised when trying to pass negative money amount."""
    pass

class NotEnoughMoneyInStorageException(Exception):
    """Exception raised when storage doesn't have enough money to withdraw."""
    pass