import os, sys, getopt, json
from teller_machine import BankCard, ITellerMachineUI, TellerMachine, TellerMachineUI
BANK_CARD_FILE = "bank_card.json"

argumentList = sys.argv[1:]
options = "hbp:w:d:m:"
long_options = ["help", "balance", "password", "withdraw", "deposit", "phone"]

def work_with_card(user_interface: ITellerMachineUI, card: BankCard) -> None:
    arguments, values = getopt.getopt(argumentList, options, long_options)

    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--help"):
            pass
        elif currentArgument in ("-p", "--password"):
            if not user_interface.insert_card(card, currentValue):
                break
        elif currentArgument in ("-b", "--balance"):
            user_interface.show_card_balance()
        elif currentArgument in ("-w", "--withdraw"):
            user_interface.withdraw_cash(currentValue)
        elif currentArgument in ("-d", "--deposit"):
            user_interface.deposit_cash()
        elif currentArgument in ("-m", "--phone"):
            user_interface.pay_for_the_phone(currentValue)

    user_interface.withdraw_card()

if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), BANK_CARD_FILE)
    with open(file_path) as file:
        card = json.load(file, object_hook=BankCard.from_json)

    user_interface = TellerMachineUI(TellerMachine())
    work_with_card(user_interface, card)