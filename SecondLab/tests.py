import unittest
import data_storage
import models
from repository import EntityDoesNotExistException, EntityIsAlreadyInRepositoryException, Repository

class StorageTests(unittest.TestCase):
    def test_StorageTests_InMemoryStorage_save_storage_is_empty_saves_data(self):
        # Arrange
        storage = data_storage.InMemoryStorage[int]()
        expected = [1, 2, 3, 4, 5]

        # Act
        storage.save(expected)
        actual = storage.load()

        # Assert
        self.assertEqual(expected, actual)

    def test_StorageTests_InMemoryStorage_save_storage_contains_data_overwrites_data(self):
        # Arrange
        initial_data = [1, 2, 3, 4, 5]
        storage = data_storage.InMemoryStorage(initial_data)
        expected = [5, 6, 7, 8, 9]

        # Act
        storage.save(expected)
        actual = storage.load()

        # Assert
        self.assertEqual(expected, actual)

    def test_StorageTests_InMemoryStorage_load_storage_is_empty_raises_an_exception(self):
        # Arrange
        storage = data_storage.InMemoryStorage()

        # Act, Assert
        self.assertRaises(data_storage.StorageIsEmptyException, storage.load)

class TestModel(models.IIdentifiable):
    """Represents the test model."""
    def __init__(self, id: int, data: str = 'Test'):
        self.id = id
        self.data = data
        
    @property
    def data(self) -> str:
        return self.__data

    @data.setter
    def data(self, value: str):
        self.__data = value

    def __eq__(self, __o: object) -> bool:
        return self.id == __o.id and self.data == __o.data
        
class RepositoryTests(unittest.TestCase):
    def test_RepositoryTests_get_all_returns_data(self):
        # Arrange
        expected = [TestModel(1), TestModel(2), TestModel(3), TestModel(4), TestModel(5)]
        storage = data_storage.InMemoryStorage(expected)
        repository = Repository(storage)

        # Act
        actual = repository.get_all()

        # Assert
        self.assertEqual(expected, actual)
        
    def test_RepositoryTests_get_returns_entity(self):
        # Arrange
        expected = TestModel(2)
        data = [TestModel(1), expected, TestModel(3), TestModel(4), TestModel(5)]
        storage = data_storage.InMemoryStorage(data)
        repository = Repository(storage)

        # Act
        actual = repository.get(expected.id)

        # Assert
        self.assertEqual(expected, actual)
        
    def test_RepositoryTests_get_entity_does_not_exist_returns_None(self):
        # Arrange
        id = 2
        data = [TestModel(1), TestModel(3), TestModel(4), TestModel(5)]
        storage = data_storage.InMemoryStorage(data)
        repository = Repository(storage)

        # Act
        actual = repository.get(id)

        # Assert
        self.assertIsNone(actual)
        
    def test_RepositoryTests_add_adds_entity(self):
        # Arrange
        expected = TestModel(2)
        data = [TestModel(1), TestModel(3), TestModel(4), TestModel(5)]
        storage = data_storage.InMemoryStorage(data)
        repository = Repository(storage)

        # Act
        repository.add(expected)

        # Assert
        actual = repository.get(expected.id)
        self.assertEqual(expected, actual)
        
    def test_RepositoryTests_add_entity_already_exists_raises_an_exceptions(self):
        # Arrange
        expected = TestModel(2)
        data = [TestModel(1), expected, TestModel(3), TestModel(4), TestModel(5)]
        storage = data_storage.InMemoryStorage(data)
        repository = Repository(storage)

        # Act, Assert
        self.assertRaises(EntityIsAlreadyInRepositoryException, repository.add, expected)
        
    def test_RepositoryTests_delete_deletes_entity(self):
        # Arrange
        data_to_delete = TestModel(2)
        data = [TestModel(1), data_to_delete, TestModel(3), TestModel(4), TestModel(5)]
        storage = data_storage.InMemoryStorage(data)
        repository = Repository(storage)

        # Act
        repository.delete(data_to_delete.id)

        # Assert
        actual = repository.get(data_to_delete.id)
        self.assertIsNone(actual)
        
    def test_RepositoryTests_delete_entity_does_not_exist_raises_an_exceptions(self):
        # Arrange
        expected = TestModel(2)
        data = [TestModel(1), TestModel(3), TestModel(4), TestModel(5)]
        storage = data_storage.InMemoryStorage(data)
        repository = Repository(storage)

        # Act, Assert
        self.assertRaises(EntityDoesNotExistException, repository.delete, expected.id)
        
    def test_RepositoryTests_update_updates_entity(self):
        # Arrange
        data_to_update = TestModel(2)
        update = TestModel(data_to_update.id, "Updated data")
        data = [TestModel(1), data_to_update, TestModel(3), TestModel(4), TestModel(5)]
        storage = data_storage.InMemoryStorage(data)
        repository = Repository(storage)

        # Act
        repository.update(update)

        # Assert
        actual = repository.get(update.id)
        self.assertEqual(update, actual)
        
    def test_RepositoryTests_update_entity_does_not_exist_raises_an_exceptions(self):
        # Arrange
        expected = TestModel(2)
        data = [TestModel(1), TestModel(3), TestModel(4), TestModel(5)]
        storage = data_storage.InMemoryStorage(data)
        repository = Repository(storage)

        # Act, Assert
        self.assertRaises(EntityDoesNotExistException, repository.update, expected)

if __name__ == "__main__":
    unittest.main()