from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from src.persistence.models import IIdentifiable
from src.persistence.data_storage import IStorage

T = TypeVar('T', bound=IIdentifiable)

class IRepository(ABC, Generic[T]):
    """Contains methods for operating with specific type data."""
    @abstractmethod
    def get(self, id: int) -> T:
        """Gets data from repository."""
        pass

    @abstractmethod
    def get_all(self) -> list[T]:
        """Gets all data from repository."""
        pass

    @abstractmethod
    def add(self, entity: T) -> None:
        """Adds the entity to repository."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> None:
        """Removes entity from repository by it's ID."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> None:
        """Updates entity in repository."""
        pass

class Repository(IRepository[T]):
    def __init__(self, storage: IStorage[list[T]]) -> None:
        self.__storage = storage

    def get(self, id: int) -> T:
        entities = self.__storage.load()
        for entity in entities:
            if entity.id == id:
                return entity

        return None

    def get_all(self) -> list[T]:
        return self.__storage.load()

    def add(self, entity: T) -> None:
        if self.__contains(entity.id):
            raise EntityIsAlreadyInRepositoryException("Unable to add entity: an entity with the same ID already exists in this repository.")

        entities = self.get_all()
        entities.append(entity)
        self.__storage.save(entities)

    def delete(self, entity_id: int) -> None:
        if not self.__contains(entity_id):
            raise EntityDoesNotExistException("Unable to delete entity: an entity with this ID does not exist in this repository.")
        
        entities = [entity for entity in self.get_all() if entity.id != entity_id]
        self.__storage.save(entities)

    def update(self, entity: T) -> None:
        if not self.__contains(entity.id):
            raise EntityDoesNotExistException("Unable to update entity: an entity with this ID does not exist in this repository.")
        
        self.delete(entity.id)
        self.add(entity)

    def __contains(self, id: int) -> bool:
        return any(id == e.id for e in self.get_all())

class EntityIsAlreadyInRepositoryException(Exception):
    pass

class EntityDoesNotExistException(Exception):
    pass