import unittest
import sys
sys.path.append("..") # Used to be able to call tests from the tests folder
from datetime import date
from src.persistence.data_storage import InMemoryStorage, StorageIsEmptyException
from src.persistence.models import ViewAppointment, IIdentifiable
from src.persistence.repository import EntityDoesNotExistException, EntityIsAlreadyInRepositoryException, Repository
from src.services.services import AppointmentsService

class StorageTests(unittest.TestCase):
    def test_StorageTests_InMemoryStorage_save_storage_is_empty_saves_data(self):
        # Arrange
        storage = InMemoryStorage[int]()
        expected = [1, 2, 3, 4, 5]

        # Act
        storage.save(expected)
        actual = storage.load()

        # Assert
        self.assertEqual(expected, actual)

    def test_StorageTests_InMemoryStorage_save_storage_contains_data_overwrites_data(self):
        # Arrange
        initial_data = [1, 2, 3, 4, 5]
        storage = InMemoryStorage(initial_data)
        expected = [5, 6, 7, 8, 9]

        # Act
        storage.save(expected)
        actual = storage.load()

        # Assert
        self.assertEqual(expected, actual)

    def test_StorageTests_InMemoryStorage_load_storage_is_empty_raises_an_exception(self):
        # Arrange
        storage = InMemoryStorage()

        # Act, Assert
        self.assertRaises(StorageIsEmptyException, storage.load)

class TestModel(IIdentifiable):
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
        storage = InMemoryStorage(expected)
        repository = Repository(storage)

        # Act
        actual = repository.get_all()

        # Assert
        self.assertEqual(expected, actual)
        
    def test_RepositoryTests_get_returns_entity(self):
        # Arrange
        expected = TestModel(2)
        data = [TestModel(1), expected, TestModel(3), TestModel(4), TestModel(5)]
        storage = InMemoryStorage(data)
        repository = Repository(storage)

        # Act
        actual = repository.get(expected.id)

        # Assert
        self.assertEqual(expected, actual)
        
    def test_RepositoryTests_get_entity_does_not_exist_returns_None(self):
        # Arrange
        id = 2
        data = [TestModel(1), TestModel(3), TestModel(4), TestModel(5)]
        storage = InMemoryStorage(data)
        repository = Repository(storage)

        # Act
        actual = repository.get(id)

        # Assert
        self.assertIsNone(actual)
        
    def test_RepositoryTests_add_adds_entity(self):
        # Arrange
        expected = TestModel(2)
        data = [TestModel(1), TestModel(3), TestModel(4), TestModel(5)]
        storage = InMemoryStorage(data)
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
        storage = InMemoryStorage(data)
        repository = Repository(storage)

        # Act, Assert
        self.assertRaises(EntityIsAlreadyInRepositoryException, repository.add, expected)
        
    def test_RepositoryTests_delete_deletes_entity(self):
        # Arrange
        data_to_delete = TestModel(2)
        data = [TestModel(1), data_to_delete, TestModel(3), TestModel(4), TestModel(5)]
        storage = InMemoryStorage(data)
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
        storage = InMemoryStorage(data)
        repository = Repository(storage)

        # Act, Assert
        self.assertRaises(EntityDoesNotExistException, repository.delete, expected.id)
        
    def test_RepositoryTests_update_updates_entity(self):
        # Arrange
        data_to_update = TestModel(2)
        update = TestModel(data_to_update.id, "Updated data")
        data = [TestModel(1), data_to_update, TestModel(3), TestModel(4), TestModel(5)]
        storage = InMemoryStorage(data)
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
        storage = InMemoryStorage(data)
        repository = Repository(storage)

        # Act, Assert
        self.assertRaises(EntityDoesNotExistException, repository.update, expected)

class AppointmentsServiceTests(unittest.TestCase):
    def test_AppointmentsServiceTest_get_by_patient_name_returns_all_contained_case_insentitive(self):
        # Arrange
        appointments = [ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2020, 2, 12), 'Dr. Who', 'Healthy'),
                        ViewAppointment('vadim', 'Minsk', date(2003, 2, 12), date(2020, 2, 12), 'Dr. Who', 'Healthy'),
                        ViewAppointment('Vad', 'Minsk', date(2003, 2, 12), date(2020, 2, 12), 'Dr. Who', 'Healthy'),
                        ViewAppointment('Kurdesov Vadim', 'Minsk', date(2003, 2, 12), date(2020, 2, 12), 'Dr. Who', 'Healthy')]
        storage = InMemoryStorage(appointments)
        repository = Repository(storage) 
        service = AppointmentsService(repository)
        name = 'V'

        # Act
        actual = service.get_by_patient_name(name)

        # Assert
        self.assertEqual(appointments, actual)
        
    def test_AppointmentsServiceTest_get_by_patient_address_returns_all_contained_case_insentitive(self):
        # Arrange
        appointments = [ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2020, 2, 12), 'Dr. Who', 'Healthy'),
                        ViewAppointment('Vadim', 'minsk', date(2003, 2, 12), date(2020, 2, 12), 'Dr. Who', 'Healthy'),
                        ViewAppointment('Vadim', 'Min', date(2003, 2, 12), date(2020, 2, 12), 'Dr. Who', 'Healthy'),
                        ViewAppointment('Vadim', 'City Minsk', date(2003, 2, 12), date(2020, 2, 12), 'Dr. Who', 'Healthy')]
        storage = InMemoryStorage(appointments)
        repository = Repository(storage) 
        service = AppointmentsService(repository)
        name = 'Min'

        # Act
        actual = service.get_by_patient_address(name)

        # Assert
        self.assertEqual(appointments, actual)
        
    def test_AppointmentsServiceTest_get_by_patient_date_of_birth_returns_patients_with_the_same_birth_date(self):
        # Arrange
        expected_date = date(1994, 4, 2)
        expected = ViewAppointment('Denis', 'Tokyo', expected_date, date(2021, 3, 11), 'Dr. Who', 'Healthy')
        appointments = [ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. What', 'Sick'), expected]
        storage = InMemoryStorage(appointments)
        repository = Repository(storage) 
        service = AppointmentsService(repository)

        # Act
        actual = service.get_by_patient_date_of_birth(expected_date)

        # Assert
        self.assertEqual(appointments[1], actual[0])
        
    def test_AppointmentsServiceTest_get_by_appointent_date_returns_patients_with_the_same_appointent_date(self):
        # Arrange
        expected_date = date(1994, 4, 2)
        expected = ViewAppointment('Denis', 'Tokyo', date(2020, 2, 12), expected_date, 'Dr. Who', 'Healthy')
        appointments = [ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. What', 'Sick'), expected]
        storage = InMemoryStorage(appointments)
        repository = Repository(storage) 
        service = AppointmentsService(repository)

        # Act
        actual = service.get_by_appointent_date(expected_date)

        # Assert
        self.assertEqual(appointments[1], actual[0])
        
    def test_AppointmentsServiceTest_get_by_doctor_name_returns_all_contained_case_insentitive(self):
        # Arrange
        appointments = [ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2020, 2, 12), 'Who', 'Healthy'),
                        ViewAppointment('Denis', 'Minsk', date(2003, 2, 12), date(2020, 2, 12), 'Dr. Who', 'Healthy'),
                        ViewAppointment('Alex', 'Minsk', date(2003, 2, 12), date(2020, 2, 12), 'who', 'Healthy'),
                        ViewAppointment('Nick', 'Minsk', date(2003, 2, 12), date(2020, 2, 12), 'wh', 'Healthy')]
        storage = InMemoryStorage(appointments)
        repository = Repository(storage) 
        service = AppointmentsService(repository)
        name = 'w'

        # Act
        actual = service.get_by_doctor_name(name)

        # Assert
        self.assertEqual(appointments, actual)

if __name__ == "__main__":
    unittest.main()