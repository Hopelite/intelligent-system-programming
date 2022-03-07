import unittest
import data_storage
import models
from repository import Repository

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
    def __init__(self, id: int):
        self.id = id

    def __eq__(self, __o: object) -> bool:
        return self.id == __o.id
        
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
        
    def test_RepositoryTests_get_returns_data(self):
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

if __name__ == "__main__":
    unittest.main()