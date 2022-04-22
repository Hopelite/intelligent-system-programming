from abc import abstractmethod
from datetime import date
from decimal import Decimal, InvalidOperation
from src.persistence.data_storage import JsonFileStorage
from src.persistence.banknote import Banknote, InvalidBanknoteValueException
from src.persistence.bank_card import BankCard
from src.teller_machine import ITellerMachine, IUserInterface
from src.persistence.banknote_storage import JsonFileBanknoteStorage, BanknoteStorage, NotEnoughMoneyInStorageException
from src.persistence.card_account import CardAccount

class TellerMachine(ITellerMachine):
    """Implements methods for operationing with teller machine."""
    def __init__(self) -> None:
        json_file_storage = JsonFileStorage[list[Banknote]]("atm_data.json")
        banknote_file_storage = JsonFileBanknoteStorage(json_file_storage)
        self.__storage = BanknoteStorage(banknote_file_storage)

    def get_card_balance(self, card: BankCard) -> Decimal:
        return card.card_account.view_balance()

    def withdraw_cash(self, amount: Decimal, card: BankCard) -> list[Banknote]:
        try:
            if amount < 0:
                print("You cannot withdraw negative money amount")
                return
            if card.card_account.view_balance() < amount:
                print("You haven't got enough money to withdraw.")
                return
            banknotes = self.__storage.withdraw_banknotes(amount)
            card.card_account.withdraw_cash(amount)
            return banknotes
        except NotEnoughMoneyInStorageException:
            print("Sorry, but this ATM doesn't have enough money in storage to withdraw. Please, request smaller amount.")

    def deposit_cash(self, cash: list[Banknote], card: BankCard) -> Decimal:
        self.__storage.deposit_banknotes(cash)
        amount = self.__calculate_cash_amount(cash)
        card.card_account.deposit_cash(amount)
        return amount

    def pay_for_the_phone(self, phone_number: str, amount: Decimal, card: BankCard) -> None:
        if self.get_card_balance(card) < amount:
            print("You haven't got enough money.")
        else:
            card.card_account.withdraw_cash(amount)
            print("Successfully paid for the phone.")

    def __calculate_cash_amount(self, banknotes: list[Banknote]) -> Decimal:
        cash = Decimal()
        for banknote in banknotes:
            cash += banknote.value

        return cash

class ITellerMachineUI:
    """Contains methods for teller machine user interface."""
    @abstractmethod
    def insert_card(self, bank_card: BankCard) -> bool:
        pass
    
    @abstractmethod
    def withdraw_card(self) -> BankCard:
        pass

    @abstractmethod
    def get_card_balance(self) -> None:
        pass

    @abstractmethod
    def withdraw_cash(self) -> list[Banknote]:
        pass

    @abstractmethod
    def deposit_cash(self) -> None:
        pass
    
    @abstractmethod
    def pay_for_the_phone(self) -> None:
        pass

class TellerMachineUI:
    """Implements teller machine user interface."""
    def __init__(self, teller_machine: ITellerMachine) -> None:
        self.__teller_machine = teller_machine
        self.__card_inserted = None

    def __leave_character(self) -> str:
        return "q"

    def insert_card(self, bank_card: BankCard) -> bool:
        password = input("Enter the PIN: ")
        while bank_card.password != password:
            password = input("Invalid PIN. Try again. Enter 'q' to leave: ")
            if password == self.__leave_character():
                return False
        
        self.__card_inserted = bank_card
        print("Access granted!")
        return True

    def withdraw_card(self) -> BankCard:
        if self.__card_inserted == None:
            print("ATM has no card inserted.")

        card = self.__card_inserted
        self.__card_inserted = None
        return card

    def get_card_balance(self) -> None:
        if self.__card_inserted == None:
            print("ATM has no card inserted.")
        else:
            print("Your card balance: ", self.__teller_machine.get_card_balance(self.__card_inserted))

    def withdraw_cash(self) -> list[Banknote]:
        amount = Decimal(input("Enter the amount of cash you want to withdraw: "))
        if self.__card_inserted == None:
            print("ATM has no card inserted.")
            return []
        else:
            return self.__teller_machine.withdraw_cash(amount, self.__card_inserted)
    
    def deposit_cash(self) -> None:
        if self.__card_inserted == None:
            print("ATM has no card inserted.")
        else:
            banknotes_string = input("\nEnter the banknotes you want to deposit. Enter 'q' to leave: ")
            if banknotes_string == self.__leave_character():
                return
            try:
                banknotes = self.__str_to_banknotes(banknotes_string)
            except InvalidOperation:
                print("Invalid banknote value passed. Please, specify only numeric values.")
                return self.deposit_cash()
            except InvalidBanknoteValueException:
                print("Invalid banknote value passed. Please, specify only positive numeric values.")
                return self.deposit_cash()

            deposited = self.__teller_machine.deposit_cash(banknotes, self.__card_inserted)
            print("Successfully deposited", deposited)

    def pay_for_the_phone(self) -> None:
        if self.__card_inserted == None:
            print("ATM has no card inserted.")
        else:
            phone_number = input("Enter phone number: ")
            try:
                amount = Decimal(input("Enter the amount of cash you want to pay: "))
                if amount < 0:
                    print("You cannot specify negative money amount.")
                    return

                self.__teller_machine.pay_for_the_phone(phone_number, amount, self.__card_inserted)
            except InvalidOperation:
                print("Invalid amount passed. Please, specify only numeric values.")

    def __str_to_banknotes(self, string: str) -> list[Banknote]:
        string_values = string.split()
        banknotes = []
        for value in string_values:
            banknotes.append(Banknote(Decimal(value)))

        return banknotes

class ConsoleInterface(IUserInterface):
    def __init__(self) -> None:
        card_account = CardAccount()
        initial_balance = Decimal(500)
        card_account.deposit_cash(initial_balance)
        
        self.user_interface = TellerMachineUI(TellerMachine())
        self.user_banknotes = [Banknote(5), Banknote(15), Banknote(10), Banknote(20)]

        self.card = BankCard(
                card_number="1111222233334444", 
                expiration_date=date(2024,12,1),
                username="Vadim Kurdesov",
                cvc="111",
                password="1111",
                card_account=card_account)

    def run(self):
        print("\nHello! To start work, please, insert your card.")
        user_choise = input("1) Insert card\n2) Get card info\n3) Leave\nInput: ")

        if user_choise == '1':
            self.start_work(self.card)
        elif user_choise == '2':
            self.get_card_info(self.card)

    def start_work(self, bank_card: BankCard) -> None:
        if self.user_interface.insert_card(bank_card):
            self.work_with_card(self.user_interface)

    def work_with_card(self, user_interface: ITellerMachineUI) -> None:
        user_choise = input("\n1) View balance\n2) Deposit cash\n3) Withdraw cash\n4) Pay for the phone\n5) Withdraw card\nInput: ")
        
        if user_choise == '1':
            user_interface.get_card_balance()
        elif user_choise == '2':
            user_interface.deposit_cash()
        elif user_choise == '3':
            user_interface.withdraw_cash()
        elif user_choise == '4':
            user_interface.pay_for_the_phone()
        else:
            return
        
        self.work_with_card(user_interface)

    def get_card_info(self, bank_card: BankCard) -> None:
        print(bank_card.__str__())
        self.run()

    def deposit_cash(self, user_interface: ITellerMachineUI):
        user_interface.deposit_cash()
        self.work_with_card(user_interface)