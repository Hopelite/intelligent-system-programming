import os
import json
from src.controllers.teller_machine_controller_interface import ITellerMachineController
from src.persistence.bank_card import BankCard
from src.views.teller_machine_views import *
from kivy.app import App
from kivy.lang import Builder

NUMBER_OF_ATTEMPS = 3
BANK_CARD_FILE = "bank_card.json"

Builder.load_file("src/views/teller_machine_views.kv")

class GUITellerMachineController(App, ITellerMachineController):
    __inserted_card: BankCard
    __attemps_count: int

    def __init__(self, **kwargs) -> None:
        super().__init__()
        file_path = os.path.join(os.path.dirname(__file__), BANK_CARD_FILE)
        with open(file_path) as file:
            self.__inserted_card = json.load(file, object_hook=BankCard.from_json)
        self.__attemps_count = 0 
        self.__screen_manager = TellerMachineSceenManager(BalanceScreen(self.__inserted_card, name="balance_screen"))

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
        self.__screen_manager.current = "login_screen"

    def show_balance(self) -> None:
        self.__screen_manager.current = "balance_screen"

    def show_menu_screen(self) -> None:
        self.__screen_manager.current = "menu_screen"