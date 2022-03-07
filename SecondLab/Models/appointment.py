from datetime import date
from patient import Patient
from doctor import Doctor

class Appointment:
    """Represents doctor's appointment."""
    def __init__(self,
        patient: Patient,
        appointent_date: date,
        doctor: Doctor,
        conclusion: str) -> None:
        self.patient = patient
        self.appointent_date = appointent_date
        self.doctor = doctor
        self.conclusion = conclusion

    @property
    def patient(self) -> Patient:
        return self.__patient

    @patient.setter
    def patient(self, value: Patient):
        self.__patient = value
        
    @property
    def appointent_date(self) -> date:
        return self.__appointent_date

    @appointent_date.setter
    def appointent_date(self, value: date):
        self.__appointent_date = value
        
    @property
    def doctor(self) -> Doctor:
        return self.__doctor

    @doctor.setter
    def doctor(self, value: Doctor):
        self.__doctor = value

    @property
    def conclusion(self) -> str:
        return self.__conclusion

    @conclusion.setter
    def conclusion(self, value: str):
        self.__conclusion = value