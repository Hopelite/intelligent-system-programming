from abc import ABC
from datetime import date

class IIdentifiable(ABC):
    """Makes model identifiable by ID property."""
    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int):
        self.__id = value

class Patient(IIdentifiable):
    """Represents the hospital patient."""
    def __init__(self,
        id: int, 
        first_name: str,
        last_name: str,
        address: str,
        date_of_birth: date) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.date_of_birth = date_of_birth

    @property
    def first_name(self) -> str:
        return self.__first_name

    @first_name.setter
    def first_name(self, value: str):
        self.__first_name = value
        
    @property
    def last_name(self) -> str:
        return self.__last_name

    @last_name.setter
    def last_name(self, value: str):
        self.__last_name = value
        
    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str):
        self.__address = value
    
    @property
    def date_of_birth(self) -> date:
        return self.__date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value: date):
        self.__date_of_birth = value

    @property
    def full_name(self) -> str:
        return self.first_name + ' ' + self.last_name

class Doctor(IIdentifiable):
    """Represents the hospital doctor."""
    def __init__(self,
        id: int,
        first_name: str,
        last_name: str) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self) -> str:
        return self.__first_name

    @first_name.setter
    def first_name(self, value: str):
        self.__first_name = value
        
    @property
    def last_name(self) -> str:
        return self.__last_name

    @last_name.setter
    def last_name(self, value: str):
        self.__last_name = value
        
    @property
    def full_name(self) -> str:
        return self.first_name + ' ' + self.last_name

class Appointment(IIdentifiable):
    """Represents the doctor's appointment."""
    def __init__(self,
        id: int,
        patient_id: int,
        appointent_date: date,
        doctor_id: int,
        conclusion: str) -> None:
        self.id = id
        self.patient = patient_id
        self.appointent_date = appointent_date
        self.doctor_id = doctor_id
        self.conclusion = conclusion

    @property
    def patient_id(self) -> int:
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, value: int):
        self.__patient_id = value
        
    @property
    def appointent_date(self) -> date:
        return self.__appointent_date

    @appointent_date.setter
    def appointent_date(self, value: date):
        self.__appointent_date = value
        
    @property
    def doctor_id(self) -> int:
        return self.__doctor_id

    @doctor_id.setter
    def doctor_id(self, value: int):
        self.__doctor_id = value

    @property
    def conclusion(self) -> str:
        return self.__conclusion

    @conclusion.setter
    def conclusion(self, value: str):
        self.__conclusion = value