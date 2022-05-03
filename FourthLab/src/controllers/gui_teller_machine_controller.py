from src.controllers.teller_machine_controller_interface import ITellerMachineController

class GUITellerMachineController(ITellerMachineController):
    def start(self) -> None:
        return super().start()