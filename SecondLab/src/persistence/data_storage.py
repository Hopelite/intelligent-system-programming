from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class IStorage(ABC, Generic[T]):
    """Contains methods for storing and loading data of any type."""
    @abstractmethod
    def save(self, data: T) -> None:
        """Saves data to storage."""
        pass

    @abstractmethod
    def load(self) -> T:
        """Loads data from storage."""
        pass

class InMemoryStorage(IStorage[T]):
    """Stores data in memory as a field."""
    def __init__(self, data: T = None) -> None:
        self.__data = data

    def save(self, data: T) -> None:
        self.__data = data
        
    def load(self) -> T:
        if self.__data == None:
            raise StorageIsEmptyException("Unable to load data from in-memory storage: storage is empty.")

        return self.__data

class StorageIsEmptyException(Exception):
    pass