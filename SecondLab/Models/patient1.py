from datetime import date

class Patient:
    """Represents the hospital patient."""
    def __init__(self,
        first_name: str,
        last_name: str,
        address: str,
        date_of_birth: date) -> None:
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