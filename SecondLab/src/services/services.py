from datetime import date
from src.persistence.models import ViewAppointment
from src.persistence.repository import IRepository

class AppointmentsService:
    def __init__(self, repository: IRepository[ViewAppointment]) -> None:
        self.__repository = repository

    def get_by_patient_name(self, name: str) -> list[ViewAppointment]:
        return self.__get_by(lambda appointment: name.casefold() in appointment.patient_name.casefold())

    def get_by_patient_address(self, address: str) -> list[ViewAppointment]:
        return self.__get_by(lambda appointment: address.casefold() in appointment.patient_address.casefold())
        
    def get_by_patient_date_of_birth(self, date: date) -> list[ViewAppointment]:
        return self.__get_by(lambda appointment: date.__eq__(appointment.patient_date_of_birth))
                
    def get_by_appointment_date(self, date: date) -> list[ViewAppointment]:
        return self.__get_by(lambda appointment: date.__eq__(appointment.appointent_date))
        
    def get_by_doctor_name(self, name: str) -> list[ViewAppointment]:
        return self.__get_by(lambda appointment: name.casefold() in appointment.doctor_name.casefold())
    
    def __get_by(self, func) -> list[ViewAppointment]:
        result = []
        for appointment in self.__repository.get_all():
            if func(appointment):
                result.append(appointment)

        return result