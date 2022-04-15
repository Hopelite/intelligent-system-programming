from datetime import date
from src.persistence.models import ViewAppointment
from src.persistence.repository import IRepository

class AppointmentsService:
    def __init__(self, repository: IRepository[ViewAppointment]) -> None:
        self.__repository = repository

    def get_by_patient_name(self, name: str) -> list[ViewAppointment]:
        return self.__get_by(lambda appointment: name.casefold() == appointment.patient_name.casefold())

    def get_by_patient_address(self, address: str) -> list[ViewAppointment]:
        return self.__get_by(lambda appointment: address.casefold() == appointment.patient_address.casefold())
        
    def get_by_patient_date_of_birth(self, date: date) -> list[ViewAppointment]:
        return self.__get_by(lambda appointment: date.__eq__(appointment.patient_date_of_birth))
                
    def get_by_appointment_date(self, date: date) -> list[ViewAppointment]:
        return self.__get_by(lambda appointment: date.__eq__(appointment.appointent_date))
        
    def get_by_doctor_name(self, name: str) -> list[ViewAppointment]:
        return self.__get_by(lambda appointment: name.casefold() == appointment.doctor_name.casefold())
    
    def delete_by_patient_name(self, name: str) -> None:
        return self.__delete_by(lambda appointment: name.casefold() == appointment.patient_name.casefold())
        
    def delete_by_patient_address(self, address: str) -> None:
        return self.__delete_by(lambda appointment: address.casefold() == appointment.patient_address.casefold())
        
    def delete_by_patient_date_of_birth(self, date: date) -> None:
        return self.__delete_by(lambda appointment: date.__eq__(appointment.patient_date_of_birth))
                
    def delete_by_appointment_date(self, date: date) -> None:
        return self.__delete_by(lambda appointment: date.__eq__(appointment.appointent_date))
    
    def __get_by(self, func) -> list[ViewAppointment]:
        result = []
        for appointment in self.__repository.get_all():
            if func(appointment):
                result.append(appointment)

        return result
            
    def __delete_by(self, func) -> None:
        appointments_left = []
        for appointment in self.__repository.get_all():
            if not func(appointment):
                appointments_left.append(appointment)

        self.__repository.replace_all(appointments_left)