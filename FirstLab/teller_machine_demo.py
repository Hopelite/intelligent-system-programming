from datetime import date
from decimal import Decimal
import teller_machine
from teller_machine import BankCard, Banknote, CardAccount, ITellerMachineUI, TellerMachine, TellerMachineUI

def main(bank_card: BankCard) -> None:
    print("\nHello! To start work, please, insert your card.")
    user_choise = input("1) Insert card\n2) Get card info\n3) Leave\nInput: ")

    if user_choise == '1':
        start_work(bank_card)
    elif user_choise == '2':
        get_card_info(bank_card)
    else:
        return

def start_work(bank_card: BankCard) -> None:
    user_interface.insert_card(bank_card)
    work_with_card(user_interface)

def work_with_card(user_interface: ITellerMachineUI) -> None:
    user_choise = input("\n1) View balance\n2) Deposit cash\n3) Withdraw cash\n4) Withdraw card\nInput: ")
    
    if user_choise == '1':
        user_interface.get_card_balance()
    elif user_choise == '2':
        user_interface.deposit_cash()
    elif user_choise == '3':
        user_interface.withdraw_cash()
    else:
        return
    
    work_with_card(user_interface)

def get_card_info(bank_card: BankCard) -> None:
    print(bank_card.__str__())
    main(bank_card)

def deposit_cash(user_interface: ITellerMachineUI):
    user_interface.deposit_cash()
    work_with_card(user_interface)

if __name__ == "__main__":
    card_account = CardAccount()
    initial_balance = Decimal(20)
    card_account.deposit_cash(initial_balance)

    card = BankCard(
                card_number="1111222233334444", 
                expiration_date=date(2024,12,1),
                username="Vadim Kurdesov",
                cvc="111",
                password="1111",
                card_account=card_account)

    initial_cash = [Banknote(5),
                    Banknote(5),
                    Banknote(5),
                    Banknote(10),
                    Banknote(10),
                    Banknote(20),
                    Banknote(20),
                    Banknote(50),
                    Banknote(50),
                    Banknote(100)]
    teller_machine = TellerMachine(initial_cash)
    user_interface = TellerMachineUI(teller_machine)

    user_banknotes = [Banknote(5), Banknote(15), Banknote(10), Banknote(20)]

    main(card)