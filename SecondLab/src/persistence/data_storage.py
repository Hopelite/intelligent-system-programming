from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from src.persistence.models import ViewAppointment
from src.persistence.xml_parsers import XMLReader, XMLWriter

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

class XMLStorage(IStorage[list[ViewAppointment]]):
    def __init__(self, file_path: str) -> None:
        self.__reader = XMLReader(file_path)
        self.__writer = XMLWriter(file_path)

    def save(self, data: list[ViewAppointment]) -> None:
        self.__writer.write(data)

    def load(self) -> list[ViewAppointment]:
        return self.__reader.read()