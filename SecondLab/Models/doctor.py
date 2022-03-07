class Doctor:
    """Represents the hospital doctor."""
    def __init__(self,
        first_name: str,
        last_name: str) -> None:
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