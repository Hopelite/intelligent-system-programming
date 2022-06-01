from decimal import Decimal

class Banknote:
    """Represents the banknote model."""
    def __init__(self, value: Decimal) -> None:
        self.__value = BanknoteValidator.validate_value(value)

    @property
    def value(self) -> Decimal:
        return self.__value

    def __str__(self) -> str:
        return self.value.__str__()

    def __lt__(self, other) -> bool:
        return self.value < other.value
        
    def __gt__(self, other) -> bool:
        return self.value > other.value
        
    def __eq__(self, other) -> bool:
        return self.value == other.value
    
    @staticmethod
    def str_to_banknotes(string: str):
        string_values = string.split()
        banknotes = []
        for value in string_values:
            banknotes.append(Banknote(Decimal(value)))

        return banknotes
        
class BanknoteValidator:
    @staticmethod
    def validate_value(value: Decimal) -> Decimal:
        if value <= 0:
            raise InvalidBanknoteValueException("Unable to create a banknote with value that is negative or equals zero.")
            
        return value
        
class InvalidBanknoteValueException(Exception):
    """Exception raised when trying to pass invalid banknote value."""
    pass
