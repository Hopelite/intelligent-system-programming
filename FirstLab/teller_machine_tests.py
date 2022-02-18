from datetime import datetime
from decimal import Decimal
import unittest
from teller_machine import Banknote, CardAccount, InvalidCardNumberException, NotEnoughMoneyInStorageException, NotEnoughMoneyOnBalanceException, TellerMachine
from teller_machine import InvalidBanknoteValueException
from teller_machine import BanknoteStorage
from teller_machine import NegativeMoneyAmountException
from teller_machine import BankCard
from teller_machine import InvalidCvcException
from teller_machine import InvalidPasswordException

class TellerMachineTests(unittest.TestCase):
    def test_banknote_negative_value_set_raises_an_exception(self):
        self.assertRaises(InvalidBanknoteValueException, Banknote, -100)

    def test_banknote_zero_value_set_raises_an_exception(self):
        self.assertRaises(InvalidBanknoteValueException, Banknote, 0)

    def test_banknotestorage_get_cash_available_empty_storage_returns_zero(self):
        # Arrange
        expected = Decimal()
        storage = BanknoteStorage()

        # Act
        actual = storage.get_cash_available()

        # Assert
        self.assertEqual(expected, actual)

    def test_banknotestorage_get_cash_available_returns_calculated_cash(self):
        # Arrange
        banknotes = [Banknote(1), Banknote(2), Banknote(3), Banknote(4), Banknote(5)]
        expected = Decimal(15)
        storage = BanknoteStorage(banknotes)

        # Act
        actual = storage.get_cash_available()

        # Assert
        self.assertEqual(expected, actual)
        
    def test_banknotestorage_withdraw_banknotes_negative_amount_raises_an_exception(self):
        # Arrange
        storage = BanknoteStorage()

        # Act, Assert
        self.assertRaises(NegativeMoneyAmountException, storage.withdraw_banknotes, -100)
        
    def test_banknotestorage_withdraw_banknotes_amount_equals_zero_returns_empty_list(self):
        # Arrange
        storage = BanknoteStorage()
        expected = list[Banknote]

        # Act
        actual = storage.withdraw_banknotes(0)
         
        # Assert
        self.assertEqual(expected, actual)
        
    def test_banknotestorage_withdraw_banknotes_returns_withdrawed_banknotes(self):
        # Arrange
        banknotes = [Banknote(1), Banknote(2), Banknote(3), Banknote(4), Banknote(5)]
        storage = BanknoteStorage(banknotes)
        amount_Expected = Decimal(8)
        amount_Total = Decimal(15)
        expected = [Banknote(5), Banknote(3)]

        # Act
        actual = storage.withdraw_banknotes(amount_Expected)
         
        # Assert
        self.assertEqual(expected, actual)
        self.assertEqual(amount_Total - amount_Expected, storage.get_cash_available())
        
    def test_banknotestorage_withdraw_banknotes_doesnt_have_enough_banknotes_returns_closest(self):
        # Arrange
        banknotes = [Banknote(1), Banknote(2), Banknote(5), Banknote(10)]
        storage = BanknoteStorage(banknotes)
        amount = Decimal(9)
        actual_amount_Expected = Decimal(8)
        amount_Total = Decimal(18)
        expected = [Banknote(5), Banknote(2), Banknote(1)]

        # Act
        actual = storage.withdraw_banknotes(amount)
         
        # Assert
        self.assertEqual(expected, actual)
        self.assertEqual(amount_Total - actual_amount_Expected, storage.get_cash_available())
        
    def test_banknotestorage_withdraw_banknotes_doesnt_have_any_close_enough_banknotes_returns_empty_list(self):
        # Arrange
        banknotes = [Banknote(10), Banknote(20), Banknote(50), Banknote(100)]
        storage = BanknoteStorage(banknotes)
        amount_Expected = 180
        amount = Decimal(9)

        # Act
        actual = storage.withdraw_banknotes(amount)
         
        # Assert
        self.assertEqual(0, len(actual))
        self.assertEqual(amount_Expected, storage.get_cash_available())
        
    def test_banknotestorage_withdraw_banknotes_doesnt_have_enough_cash_raises_an_exception(self):
        # Arrange
        banknotes = [Banknote(10)]
        storage = BanknoteStorage(banknotes)
        amount = Decimal(25)

        # Act, Assert
        self.assertRaises(NotEnoughMoneyInStorageException, storage.withdraw_banknotes, amount)
        
    def test_banknotestorage_deposit_banknotes_adds_banknotes_to_empty_storage(self):
        # Arrange
        banknotes = [Banknote(1), Banknote(2), Banknote(3), Banknote(4), Banknote(5)]
        amount_Expected = 15
        storage = BanknoteStorage()

        # Act
        storage.deposit_banknotes(banknotes)
         
        # Assert
        self.assertEqual(amount_Expected, storage.get_cash_available())
        
    def test_banknotestorage_deposit_banknotes_adds_banknotes_to_empty_storage(self):
        # Arrange
        banknotes = [Banknote(1), Banknote(2), Banknote(3), Banknote(4), Banknote(5)]
        amount_Expected = 15
        storage = BanknoteStorage(banknotes)

        # Act
        storage.deposit_banknotes(banknotes)
         
        # Assert
        self.assertEqual(amount_Expected * 2, storage.get_cash_available())

    def test_bankcard_card_number_length_does_not_equal_sixteen_raise_an_exception(self):
        self.assertRaises(InvalidCardNumberException, BankCard, "1111", datetime(2000, 12, 12), "Test User", "1" * 3, "1" * 4, CardAccount())
        
    def test_bankcard_card_number_contains_not_only_digits_raises_an_exception(self):
        self.assertRaises(InvalidCardNumberException, BankCard, "A" * 16, datetime(2000, 12, 12), "Test User", "1" * 3, "1" * 4, CardAccount())

    def test_bankcard_cvc_length_does_not_equal_three_raises_an_exception(self):
        self.assertRaises(InvalidCvcException, BankCard, "1" * 16, datetime(2000, 12, 12), "Test User", "1234", "1" * 4, CardAccount())
        
    def test_bankcard_cvc_contains_not_only_digits_raises_an_exception(self):
        self.assertRaises(InvalidCvcException, BankCard, "1" * 16, datetime(2000, 12, 12), "Test User", "12A", "1" * 4, CardAccount())
        
    def test_bankcard_password_length_does_not_equal_four_raises_an_exception(self):
        self.assertRaises(InvalidPasswordException, BankCard, "1" * 16, datetime(2000, 12, 12), "Test User", "1" * 3, "123", CardAccount())
        
    def test_bankcard_password_contains_not_only_digits_raises_an_exception(self):
        self.assertRaises(InvalidPasswordException, BankCard, "1" * 16, datetime(2000, 12, 12), "Test User", "1" * 3, "123A", CardAccount())

    def test_cardaccount_withdraw_cash_negative_money_amount_raises_an_exception(self):
        # Arrange 
        card_account = CardAccount()
        
        # Act, Assert
        self.assertRaises(NegativeMoneyAmountException, card_account.withdraw_cash, -100)
        
    def test_cardaccount_withdraw_cash_not_enought_money_on_balance_raises_an_exception(self):
        # Arrange 
        card_account = CardAccount()
        
        # Act, Assert
        self.assertRaises(NotEnoughMoneyOnBalanceException, card_account.withdraw_cash, 100)

    def test_cardaccount_deposit_cash_negative_money_amount_raises_an_exception(self):
        # Arrange 
        card_account = CardAccount()
        
        # Act, Assert
        self.assertRaises(NegativeMoneyAmountException, card_account.deposit_cash, -100)

    def test_cardaccount_view_balance_returns_balance(self):
        # Arrange
        card_account = CardAccount()
        expected = Decimal(100)
        card_account.deposit_cash(expected)

        # Act
        actual = card_account.view_balance()

        # Assert
        self.assertEqual(expected, actual)

    def test_tellermachine_get_card_balance_returns_card_balance(self):
        # Arrange
        teller_machine = TellerMachine()
        expected = Decimal(10)
        card_account = CardAccount()
        card_account.deposit_cash(expected)
        bank_card = BankCard('1' * 16, datetime.now(), "Test User", "111", "1111", card_account)

        # Act
        actual = teller_machine.get_card_balance(bank_card)

        # Assert
        self.assertEqual(expected, actual)
        
    def test_tellermachine_withdraw_cash_returns_cash(self):
        # Arrange
        banknotes = [Banknote(15), Banknote(20), Banknote(50), Banknote(25), Banknote(25)]
        teller_machine = TellerMachine(banknotes)
        amount = Decimal(100)
        card_account = CardAccount()
        card_account.deposit_cash(amount)
        bank_card = BankCard('1' * 16, datetime.now(), "Test User", "111", "1111", card_account)
        expected = [Banknote(50), Banknote(25), Banknote(25)]

        # Act
        actual = teller_machine.withdraw_cash(amount, bank_card)

        # Assert
        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()