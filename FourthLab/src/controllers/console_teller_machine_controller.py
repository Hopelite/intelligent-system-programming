import os
from decimal import Decimal, InvalidOperation
from src.persistence.bank_card import CardState
from src.persistence.banknote_storage import BanknoteStorage
from src.persistence.banknote_storage import NotEnoughMoneyInStorageException
from src.persistence.card_account import NotEnoughMoneyOnBalanceException
from src.persistence.banknote import InvalidBanknoteValueException
from src.persistence.banknote import Banknote
from src.persistence.bank_card import BankCard
from src.teller_machine import TellerMachine
from src.persistence.banknote_storage import JsonFileStorage, JsonFileBanknoteStorage
from src.controllers.teller_machine_controller_interface import ITellerMachineController

BANKNOTE_STORAGE_FILE = "atm_data.json"
BANK_CARD_FILE = "bank_card.json"
LEAVE_CHARACTER = "q"

class ConsoleTellerMachineController(ITellerMachineController):
    __inserted_card: BankCard

    def __init__(self) -> None:
        file_path = os.path.join(os.path.dirname(__file__), BANKNOTE_STORAGE_FILE)
        storage = BanknoteStorage(JsonFileBanknoteStorage(JsonFileStorage(file_path)))
        self.__teller_machine = TellerMachine(storage)
        self.__inserted_card = None
        self.__card_file_path = os.path.join(os.path.dirname(__file__), BANK_CARD_FILE)
    
    def start(self) -> None:
        print("\nHello! To start work, please, insert your card.")
        user_choise = input("1) Insert card\n2) Leave\nInput: ")
        
        if user_choise == '1':
            return self.__insert_card()

    def __insert_card(self) -> None:
        self.__inserted_card = BankCard.load_from_file(self.__card_file_path)
        self.__access_card()
        self.__work_with_card()

    def __access_card(self) -> None:
        password = input("Enter the PIN: ")
        while not self.__inserted_card.is_access_gained():
            card_state = self.__inserted_card.gain_access(password)
            if card_state == CardState.BLOCKED:
                print("Card is blocked.")
                return self.__withdraw_card()

            if not self.__inserted_card.is_access_gained():
                password = input("Invalid PIN. Attempts left: " + self.__inserted_card.attempts_left + ". Enter 'q' to leave: ")

    def __work_with_card(self) -> None:
        user_choise = input("\n1) View balance\n2) Deposit cash\n3) Withdraw cash\n4) Pay for the phone\n5) Withdraw card\nInput: ")

        if user_choise == '1':
            self.__show_card_balance()
        elif user_choise == '2':
            self.__deposit_cash()
        elif user_choise == '3':
            self.__withdraw_cash()
        elif user_choise == '4':
            self.__pay_for_the_phone()
        else:
            return self.__withdraw_card()

        self.__work_with_card()

    def __show_card_balance(self) -> None:
        print("Your card balance: ", self.__teller_machine.get_card_balance(self.__inserted_card))

    def __deposit_cash(self) -> None:
        banknotes_string = input("\nEnter the banknotes you want to deposit. Enter 'q' to leave: ")
        if banknotes_string == LEAVE_CHARACTER:
            return

        try:
            banknotes = Banknote.str_to_banknotes(banknotes_string)
        except InvalidOperation:
            print("Invalid banknote value passed. Please, specify only numeric values.")
            return self.__deposit_cash()
        except InvalidBanknoteValueException:
            print("Invalid banknote value passed. Please, specify only positive numeric values.")
            return self.__deposit_cash()

        deposited = self.__teller_machine.deposit_cash(banknotes, self.__inserted_card)
        print("Successfully deposited", deposited)

    def __withdraw_cash(self) -> None:
        try:
            user_input = input("Enter the amount of cash you want to withdraw. Enter 'q' to leave: ")
            if input == LEAVE_CHARACTER:
                return

            amount = Decimal(user_input)
            if amount < 0:
                print("Invalid amount passed. Please, enter a positive value.")
                return self.__withdraw_cash()

            self.__teller_machine.withdraw_cash(amount, self.__inserted_card)
            return
        except InvalidOperation:
            print("Invalid amount passed. Please, specify numeric value.")
        except NotEnoughMoneyOnBalanceException:
            print("You haven't got enough money to withdraw. Please, specify smaller amount.")
        except NotEnoughMoneyInStorageException:
            print("This ATM doesn't have such amount of money. Please, specify smaller amount. Sorry for the inconvenience.")

        return self.__withdraw_cash()

    def __pay_for_the_phone(self) -> None:
        phone_number = input("Enter the phone number: ")
        try:
            user_input = input("Enter the amount of cash you want to pay. Enter 'q' to leave: ")
            if user_input == LEAVE_CHARACTER:
                return

            amount = Decimal(user_input)
            if amount < 0:
                print("Invalid amount passed. Please, enter a positive value.")
                return self.__pay_for_the_phone()

            self.__teller_machine.pay_for_the_phone(phone_number, amount, self.__inserted_card)
            return
        except InvalidOperation:
            print("Invalid amount passed. Please, specify numeric value.")
        except NotEnoughMoneyOnBalanceException:
            print("You haven't got enough money to withdraw. Please, specify smaller amount.")
            
        return self.__pay_for_the_phone()

    def __withdraw_card(self) -> None:
        data = self.__inserted_card.to_json()
        self.__inserted_card.save_to_file(self.__card_file_path)
        self.__inserted_card = None
        return self.start()