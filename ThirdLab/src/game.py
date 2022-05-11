import pygame
from src.configuration.configuration_manager import Configuration, IConfigurationManager
from src.constants.state_names import StateNames
from src.states.highscores_state import HighscoresState
from src.states.menu_state import MenuState
from src.states.play_state import PlayState
from src.states.state_machine import StateMachine

pygame.init()

class Game:
    __configuration: Configuration

    def __init__(self, configuration_manager: IConfigurationManager) -> None:
        self.__configuration = configuration_manager.load_configuration()
        screen = pygame.display.set_mode(
            (self.__configuration.screen_configuration.screen_width,
             self.__configuration.screen_configuration.screen_height))
        
        self.__state_machine = StateMachine(self.__configuration, StateNames.MENU)
        self.__state_machine.add_state(MenuState(self.__state_machine, self.__configuration, screen))
        self.__state_machine.add_state(PlayState(self.__state_machine, self.__configuration, screen))
        self.__state_machine.add_state(HighscoresState(self.__state_machine, self.__configuration, screen))

    def run(self) -> None:
        self.__state_machine.start()
        pygame.quit()