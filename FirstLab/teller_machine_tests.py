import unittest
from teller_machine import Banknote
from teller_machine import InvalidBanknoteValueException
import teller_machine

class TellerMachineTests(unittest.TestCase):
    def test_banknote_negative_value_set_raises_an_exception(self):
        self.assertRaises(InvalidBanknoteValueException, Banknote, -100)

    def test_banknote_zero_value_set_raises_an_exception(self):
        self.assertRaises(InvalidBanknoteValueException, Banknote, 0)

if __name__ == "__main__":
    unittest.main()