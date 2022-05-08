import sys
import getopt
from src.controllers.teller_machine_controller_interface import ITellerMachineController
from src.controllers.console_teller_machine_controller import ConsoleTellerMachineController
from src.controllers.gui_teller_machine_controller import GUITellerMachineController

if __name__ == "__main__":
    controller: ITellerMachineController = None
    if sys.argv[1] == "gui":
            controller = GUITellerMachineController()
    elif sys.argv[1] == "console":
            controller = ConsoleTellerMachineController()
    else:
        print("Available options are: 'console' and 'gui'")
        sys.exit(2)

    controller.start()