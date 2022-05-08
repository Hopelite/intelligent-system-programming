from kivy.uix.screenmanager import Screen, ScreenManager

class LoginScreen(Screen):
    def clear(self) -> None:
        self.ids["warning_message"].text = ""
        self.ids["input"].ids["text_input"].text = ""

    def show_error_message(self, message: str) -> None:
        self.ids["warning_message"].text = message
        
class MenuScreen(Screen):
    pass

class BalanceScreen(Screen):
    def update_balance_label(self, amount: str) -> None:
        self.ids["balance_label"].text = amount

class DepositCashScreen(Screen):
    __selected_banknotes: list[str] = []

    @property
    def selected_banknotes(self) -> list[str]:
        return self.__selected_banknotes

    def select_banknote(self, banknote: str) -> None:
        self.__selected_banknotes.append(banknote)
        self.ids["banknotes_label"].text = self.ids["banknotes_label"].text + ' ' + banknote

    def clear_selected_banknotes(self) -> None:
        self.ids["banknotes_label"].text = 'Banknotes to deposit: '

class WithdrawCashScreen(Screen):
    def update_status_label(self, message: str) -> None:
        self.ids["status_label"].text = message

class PayForPhoneScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def show_error_message(self, message: str) -> None:
        self.ids["warning_message"].text = message

class TellerMachineSceenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(LoginScreen(name="login_screen"))
        self.add_widget(MenuScreen(name="menu_screen"))
        self.add_widget(BalanceScreen(name="balance_screen"))
        self.add_widget(DepositCashScreen(name="deposit_screen"))
        self.add_widget(PayForPhoneScreen(name="phone_screen"))
        self.add_widget(WithdrawCashScreen(name="withdraw_screen"))
