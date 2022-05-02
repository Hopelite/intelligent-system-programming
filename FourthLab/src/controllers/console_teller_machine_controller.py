from decimal import Decimal, InvalidOperation
import os
import json
from src.persistence.banknote_storage import BanknoteStorage
from src.persistence.banknote_storage import NotEnoughMoneyInStorageException
from src.persistence.card_account import NotEnoughMoneyOnBalanceException
from src.persistence.banknote import InvalidBanknoteValueException
from src.persistence.banknote import Banknote
from src.persistence.bank_card import BankCard
from src.teller_machine import TellerMachine
from src.persistence.banknote_storage import JsonFileStorage, JsonFileBanknoteStorage

BANKNOTE_STORAGE_FILE = "atm_data.json"
BANK_CARD_FILE = "bank_card.json"
LEAVE_CHARACTER = "q"

class ITellerMachineController:
    def start(self) -> None:
        pass

class ConsoleTellerMachineController(ITellerMachineController):
    __inserted_card: BankCard

    def __init__(self) -> None:
        file_path = os.path.join(os.path.dirname(__file__), BANKNOTE_STORAGE_FILE)
        storage = BanknoteStorage(JsonFileBanknoteStorage(JsonFileStorage(file_path)))
        self.__teller_machine = TellerMachine(storage)
        self.__inserted_card = None
    
    def start(self) -> None:
        print("\nHello! To start work, please, insert your card.")
        user_choise = input("1) Insert card\n2) Leave\nInput: ")
        
        if user_choise == '1':
            return self.__insert_card()

    def __insert_card(self) -> None:
        file_path = os.path.join(os.path.dirname(__file__), BANK_CARD_FILE)
        with open(file_path) as file:
            self.__inserted_card = json.load(file, object_hook=BankCard.from_json)

        self.__access_card()
        self.__work_with_card()

    def __access_card(self) -> None:
        attempts_left = 3

        password = input("Enter the PIN: ")
        while password != self.__inserted_card.password:
            attempts_left -= 1
            if attempts_left <= 0:
                print("Card is blocked.")
                return self.__withdraw_card()

            password = input("Invalid PIN. Attempts left: " + attempts_left.__str__() + ". Enter 'q' to leave: ")

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
            banknotes = self.__str_to_banknotes(banknotes_string)
        except InvalidOperation:
            print("Invalid banknote value passed. Please, specify only numeric values.")
            return self.__deposit_cash()
        except InvalidBanknoteValueException:
            print("Invalid banknote value passed. Please, specify only positive numeric values.")
            return self.__deposit_cash()

        deposited = self.__teller_machine.deposit_cash(banknotes, self.__inserted_card)
        print("Successfully deposited", deposited)
        
    def __str_to_banknotes(self, string: str) -> list[Banknote]:
        string_values = string.split()
        banknotes = []
        for value in string_values:
            banknotes.append(Banknote(Decimal(value)))

        return banknotes

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
        except InvalidOperation:
            print("Invalid amount passed. Please, specify numeric value.")
            return self.__withdraw_cash()
        except NotEnoughMoneyOnBalanceException:
            print("You haven't got enough money to withdraw. Please, specify smaller amount.")
            return self.__withdraw_cash()
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
        except InvalidOperation:
            print("Invalid amount passed. Please, specify numeric value.")
            return self.__pay_for_the_phone()
        except NotEnoughMoneyOnBalanceException:
            print("You haven't got enough money to withdraw. Please, specify smaller amount.")
            return self.__pay_for_the_phone()

    def __withdraw_card(self) -> None:
        data = self.__inserted_card.to_json()

        file_path = os.path.join(os.path.dirname(__file__), BANK_CARD_FILE)
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        self.__inserted_card = None
        return self.start()