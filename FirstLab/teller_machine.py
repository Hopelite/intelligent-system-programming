import datetime
from decimal import Decimal

class Banknote:
    def __init__(self, value: Decimal) -> None:
        if value <= 0:
            raise InvalidBanknoteValueException("Unable to create a banknote with value that is negative or equals zero.")
        self.__value = value

    @property
    def value(self) -> Decimal:
        return self.__value

class InvalidBanknoteValueException(Exception):
    pass