# Exception raised when trying to pass invalid banknote value
class InvalidBanknoteValueException(Exception):
    pass

# Exception raised when trying to pass negative money amount       
class NegativeMoneyAmountException(Exception):
    pass

# Exception raised when storage doesn't have enough money to withdraw
class NotEnoughMoneyInStorageException(Exception):
    pass

# Exception raised when storage doesn't have enough money to withdraw
class NotEnoughMoneyOnBalanceException(Exception):
    pass

# Exception raised when trying to pass invalid card number
class InvalidCardNumberException(Exception):
    pass

# Exception raised when trying to pass invalid CVC
class InvalidCvcException(Exception):
    pass

# Exception raised when trying to pass invalid password
class InvalidPasswordException(Exception):
    pass