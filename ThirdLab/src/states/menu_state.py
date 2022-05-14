import os.path
import pygame
from itertools import cycle
from src.configuration.configuration import Configuration
from src.constants.colors import Colors
from src.constants.paths import Paths
from src.constants.state_names import StateNames
from src.helpers.screen_helper import ScreenHelper
from src.states.state import IState
from src.states.state_machine import StateMachine

MENU_SELECTION_SOUND_FILE = "menu_selection.mp3"

class MenuOption:
    def __init__(self, text: str, state_name: str) -> None:
        self.text = text
        self.state_name = state_name

class MenuState(IState):
    def __init__(self, state_machine: StateMachine, configuration: Configuration, screen: pygame.Surface) -> None:
        self.__state_machine = state_machine
        self.__configuration = configuration
        self.__screen = screen
        self.__row_highlighted = 0
        self.__menu_options = [MenuOption("PLAY", StateNames.PLAY),
                                        MenuOption("HIGHSCORES", StateNames.HIGHSCORES),
                                        MenuOption("INFO", StateNames.INFO)]
        self.__row_indices = cycle(range(0, len(self.__menu_options)))
        self.__selection_sound = pygame.mixer.Sound(os.path.join(Paths.SOUNDS, MENU_SELECTION_SOUND_FILE))

    def get_state_name(self) -> str:
        return StateNames.MENU
    
    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__state_machine.stop()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.__row_highlighted = next(self.__row_indices)
                pygame.mixer.Sound.play(self.__selection_sound)
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            #     self.__row_highlighted = next(reversed(self.__row_indices))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.__state_machine.set_state(self.__menu_options[self.__row_highlighted].state_name)

    def update(self) -> None:
        pass
    
    def draw(self) -> None:
        self.__screen.fill(Colors.BLACK)
        recordPosition = self.__configuration.screen_configuration.screen_height / 2
        text_color = Colors.GREY
        for index, option in enumerate(self.__menu_options):
            if index == self.__row_highlighted:
                text_color = Colors.YELLOW
            else:
                text_color = Colors.GREY

            ScreenHelper.draw_text(option.text,
                            self.__screen,
                            [self.__configuration.screen_configuration.screen_width // 2, recordPosition],
                            self.__configuration.text_configuration.font_size,
                            text_color,
                            self.__configuration.text_configuration.font_family,
                            centered=True)
                            
            recordPosition += self.__configuration.text_configuration.font_size