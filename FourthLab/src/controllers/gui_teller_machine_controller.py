from decimal import Decimal
import os
import json
from src.controllers.teller_machine_controller_interface import ITellerMachineController
from src.persistence.banknote_storage import BanknoteStorage, JsonFileBanknoteStorage
from src.persistence.data_storage import JsonFileStorage
from src.persistence.banknote import Banknote
from src.persistence.bank_card import BankCard
from src.teller_machine import TellerMachine
from src.views.teller_machine_views import *
from kivy.app import App
from kivy.lang import Builder

NUMBER_OF_ATTEMPS = 3
BANK_CARD_FILE = "bank_card.json"
BANKNOTE_STORAGE_FILE = "atm_data.json"

Builder.load_file("src/views/teller_machine_views.kv")

class GUITellerMachineController(App, ITellerMachineController):
    __inserted_card: BankCard
    __attemps_count: int

    def __init__(self, **kwargs) -> None:
        super().__init__()
        card_file_path = os.path.join(os.path.dirname(__file__), BANK_CARD_FILE)
        with open(card_file_path) as file:
            self.__inserted_card = json.load(file, object_hook=BankCard.from_json)
            
        file_path = os.path.join(os.path.dirname(__file__), BANKNOTE_STORAGE_FILE)
        storage = BanknoteStorage(JsonFileBanknoteStorage(JsonFileStorage(file_path)))
        self.__teller_machine = TellerMachine(storage)
        self.__attemps_count = 0 
        self.__screen_manager = TellerMachineSceenManager()

    def build(self):
        return self.__screen_manager

    def start(self) -> None:
        self.run()

    def enter_pin(self, pin: str) -> None:
        login_screen = self.__screen_manager.get_screen("login_screen")

        if self.__attemps_count >= NUMBER_OF_ATTEMPS:
            login_screen.show_error_message("Card has been blocked")
            return

        error_message = ""
        if not str.isnumeric(pin):
            error_message = "PIN must contain only digits"
        elif len(pin) != 4:
            error_message = "PIN must consist of 4 digits"
        elif self.__inserted_card.password != pin:
            self.__attemps_count += 1
            error_message = "Invalid PIN. Attempts remain: " + (NUMBER_OF_ATTEMPS - self.__attemps_count).__str__()
            if self.__attemps_count >= NUMBER_OF_ATTEMPS:
                error_message = "Card has been blocked"
            
        if error_message != "":
            login_screen.show_error_message(error_message)
            return

        login_screen.clear()
        self.__attemps_count = 0
        self.__screen_manager.current = "menu_screen"

    def withdraw_card(self) -> None:
        data = self.__inserted_card.to_json()

        file_path = os.path.join(os.path.dirname(__file__), BANK_CARD_FILE)
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        self.__screen_manager.current = "login_screen"

    def show_show_balance_screen(self) -> None:
        self.__screen_manager.get_screen("balance_screen").update_balance_label(self.__inserted_card.card_account.balance.__str__())
        self.__screen_manager.current = "balance_screen"

    def show_menu_screen(self) -> None:
        self.__screen_manager.current = "menu_screen"

    def show_deposit_screen(self) -> None:
        self.__screen_manager.current = "deposit_screen"
        
    def deposit_cash(self) -> None:
        deposit_screen = self.__screen_manager.get_screen("deposit_screen")
        banknotes = self.__convert_to_banknotes(deposit_screen.selected_banknotes)
        self.__teller_machine.deposit_cash(banknotes, self.__inserted_card)
        deposit_screen.clear_selected_banknotes()

    def __convert_to_banknotes(self, str_banknotes: list[str]) -> list[Banknote]:
        result = []
        for str_banknote in str_banknotes:
            result.append(Banknote(Decimal(str_banknote)))

        return result

    def show_withdraw_screen(self) -> None:
        self.__screen_manager.current = "withdraw_screen"
        
    def withdraw_cash(self, amount_str: str) -> None:
        withdraw_screen = self.__screen_manager.get_screen("withdraw_screen")
        error_message = ""
        if not amount_str.isdigit():
            error_message = "Invalid amount passed. Please, specify positive integer value."
            withdraw_screen.update_status_label(error_message)
            return

        amount = Decimal(amount_str)
        if amount <= 0:
            error_message = "Invalid amount passed. Please, specify positive numeric value."
        elif self.__inserted_card.card_account.balance < amount:
            error_message = "You haven't got enough money to withdraw. Please, specify smaller amount."
            
        if error_message != "":
            withdraw_screen.update_status_label(error_message)
            return

        banknotes = self.__teller_machine.withdraw_cash(amount, self.__inserted_card)
        success_message = "Withrawed banknotes: "
        for banknote in banknotes:
            success_message += (' ' + banknote.value.__str__())

        withdraw_screen.update_status_label(success_message)
        

    def show_pay_for_the_phone_screen(self) -> None:
        self.__screen_manager.current = "phone_screen"

    def pay_for_the_phone(self, phone_number: str, amount_str: str) -> None:
        phone_screen = self.__screen_manager.get_screen("phone_screen")
        error_message = ""
        if not amount_str.isdigit():
            error_message = "Invalid amount passed. Please, specify positive integer value."
            phone_screen.show_error_message(error_message)
            return

        amount = Decimal(amount_str)
        if amount <= 0:
            error_message = "Invalid amount passed. Please, specify positive numeric value."
        elif self.__inserted_card.card_account.balance < amount:
            error_message = "You haven't got enough money to withdraw. Please, specify smaller amount."
            
        if error_message != "":
            phone_screen.show_error_message(error_message)
            return
        
        self.__inserted_card.card_account.withdraw_cash(amount)
        phone_screen.show_error_message("Successfully paid " + amount.__str__() + " for the " + phone_number)
        self.__screen_manager.current = "phone_screen"