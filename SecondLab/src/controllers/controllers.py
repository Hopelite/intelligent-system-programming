import math
from datetime import datetime
from src.persistence.data_storage import XMLStorage
from src.persistence.models import ViewAppointment
from src.persistence.repository import Repository
from src.services.services import AppointmentsService
from src.views.views import ProgramScreenManager, TableScreen, AddScreen

class ViewAppointmentsController:
    def __init__(self) -> None:
        storage = XMLStorage("C:\\Users\\Admin\\source\\repos\\BSUIR\\intelligent-system-programming\\SecondLab\\src\\input.xml")
        self.__repository = Repository[ViewAppointment](storage)
        self.__service = AppointmentsService(self.__repository)

    def start_program(self) -> ProgramScreenManager:
        table_screen = self.get_table()
        return ProgramScreenManager(table_screen) 

    def get_number_of_pages(self) -> int:
        return math.ceil(len(self.__repository.get_all()) / 10)

    def get_table(self, page: int = 1, size: int = 10) -> TableScreen:
        appointments = self.__paginate(self.__repository.get_all(), page, size)
        return TableScreen(appointments, name="table_screen")

    def find_by_patient_name(self, name: str, page: int = 1, size: int = 10) -> TableScreen:
        appointments = self.__paginate(self.__service.get_by_patient_name(name), page, size)
        return TableScreen(appointments, name="table_screen")
        
    def find_by_address(self, address: str, page: int = 1, size: int = 10) -> TableScreen:
        appointments = self.__paginate(self.__service.get_by_patient_address(address), page, size)
        return TableScreen(appointments, name="table_screen")
        
    def find_by_doctor_name(self, name: str, page: int = 1, size: int = 10) -> TableScreen:
        appointments = self.__paginate(self.__service.get_by_doctor_name(name)[(page - 1) * size:size], page, size)
        return TableScreen(appointments, name="table_screen")
        
    def find_by_appointment_date(self, appointment_date_str: str, page: int = 1, size: int = 10) -> TableScreen:
        appointment_date = datetime.strptime(appointment_date_str, '%m-%d-%Y').date()
        appointments = self.__paginate(self.__service.get_by_appointment_date(appointment_date), page, size)
        return TableScreen(appointments, name="table_screen")

    def delete_by_patient_name(self, name: str) -> TableScreen:
        self.__service.delete_by_patient_name(name)
        return self.get_table()

    def delete_by_patient_address(self, address: str) -> TableScreen:
        self.__service.delete_by_patient_address(address)
        return self.get_table()

    def add_appointment(self, name, address, birth, appointment_date, doctor, conclusion) -> AddScreen:
        try:
            appointment = self.__parse_to_appointment(name, address, birth, appointment_date, doctor, conclusion)
            if self.__is_appointment_not_filled(appointment):
                return AddScreen(appointment, False, name='add_screen')
            else:
                self.__repository.add(appointment)
                return AddScreen(success=True, name='add_screen')
        except:
            return AddScreen(success=False, name='add_screen')
            
    def __parse_to_appointment(self, 
    patient_name: str, patient_address: str, 
    patient_date_of_birth: str, appointment_date: str,
    doctor_name: str, conclusion: str) -> ViewAppointment:
    
        parsed_birth_date = None
        if appointment_date != '':
            parsed_birth_date = datetime.strptime(patient_date_of_birth, '%d-%m-%Y').date()
        parsed_appointment_date = None
        if appointment_date != '':
            parsed_appointment_date = datetime.strptime(appointment_date, '%d-%m-%Y').date()

        return ViewAppointment(
            patient_name=patient_name, patient_address = patient_address,
            patient_date_of_birth=parsed_birth_date,
            appointent_date=parsed_appointment_date,
            doctor_name=doctor_name, conclusion=conclusion)

    def __is_appointment_not_filled(self, appointment: ViewAppointment):
        return appointment.patient_name == "" or appointment.patient_address == "" \
            or appointment.patient_date_of_birth == None or appointment.appointent_date == None \
                or appointment.doctor_name == ""

    def __paginate(self, appointments: list[ViewAppointment], page: int, size: int) -> list[ViewAppointment]:
        start_index = (page - 1) * size
        end_index = start_index + size

        if end_index > len(appointments) + size:
            start_index -= size
            end_index -= size

        return appointments[start_index:end_index]