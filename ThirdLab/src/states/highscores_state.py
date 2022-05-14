import pygame
from src.configuration.configuration import Configuration
from src.constants.colors import Colors
from src.constants.state_names import StateNames
from src.helpers.screen_helper import ScreenHelper
from src.states.state import IState
from src.states.state_machine import StateMachine
from src.states.table_of_recods import TableOfRecords

class HighscoresState(IState):
    PADDING = 20

    def __init__(self, state_machine: StateMachine, configuration: Configuration, screen: pygame.Surface) -> None:
        self.__state_machine = state_machine
        self.__configuration = configuration
        self.__screen = screen
        self.__table_of_records = TableOfRecords()

    def get_state_name(self) -> str:
        return StateNames.HIGHSCORES

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__state_machine.stop()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.__state_machine.set_state(StateNames.MENU)

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.__draw_high_scores()
        ScreenHelper.draw_text('HIGH SCORES',
                                self.__screen,
                                [self.__configuration.screen_configuration.screen_width//2, self.PADDING * 2],
                                self.__configuration.text_configuration.font_size,
                                Colors.WHITE,
                                self.__configuration.text_configuration.font_family,
                                centered=True)

    def __draw_high_scores(self):
        self.__screen.fill(Colors.BLACK)
        records = self.__table_of_records.get_records()
        recordPosition = self.PADDING * 5
        for record in records:
            ScreenHelper.draw_text(record.name + ': ' + record.score.__str__(),
                                    self.__screen,
                                    [self.__configuration.screen_configuration.screen_width // 2, recordPosition],
                                    self.__configuration.text_configuration.font_size - 10,
                                    Colors.YELLOW,
                                    self.__configuration.text_configuration.font_family,
                                    centered=True)
            recordPosition += self.__configuration.text_configuration.font_size

        ScreenHelper.draw_text("Press ESC to return",
                                self.__screen,
                                [self.__configuration.screen_configuration.screen_width // 2, self.__configuration.screen_configuration.screen_height - self.__configuration.text_configuration.font_size - 20],
                                self.__configuration.text_configuration.font_size,
                                Colors.WHITE,
                                self.__configuration.text_configuration.font_family,
                                True)