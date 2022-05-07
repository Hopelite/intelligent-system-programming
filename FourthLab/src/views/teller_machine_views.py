from kivy.uix.screenmanager import Screen, ScreenManager
from src.persistence.bank_card import BankCard

class LoginScreen(Screen):
    def clear(self) -> None:
        self.ids["warning_message"].text = ""
        self.ids["input"].ids["text_input"].text = ""

    def show_error_message(self, message: str) -> None:
        self.ids["warning_message"].text = message
        
class MenuScreen(Screen):
    pass

class BalanceScreen(Screen):
    def __init__(self, card: BankCard, **kw):
        super().__init__(**kw)
        self.ids["balance_label"].text = card.card_account.balance.__str__()
    
class TellerMachineSceenManager(ScreenManager):
    def __init__(self, balance_screen: BalanceScreen, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(LoginScreen(name="login_screen"))
        self.add_widget(MenuScreen(name="menu_screen"))
        self.add_widget(balance_screen)
