from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from json import JSONEncoder
import json

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

class JsonFileStorage(IStorage[T]):
    """Represents data storage based on JSON file."""
    def __init__(self, path: str) -> None:
        self.__path = path

    def save(self, data: T) -> None:
        serialized_data = json.dumps(data, indent=4, cls=JsonEncoder)
        with open(self.__path, 'w') as file:
            file.write(serialized_data)

    def load(self) -> T:
        with open(self.__path, 'r') as file:
            deserialized_data = json.load(file)

        return deserialized_data

class JsonEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__