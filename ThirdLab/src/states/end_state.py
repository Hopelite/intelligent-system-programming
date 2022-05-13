import os.path
import pygame
from pygame import Vector2
from src.configuration.configuration import Configuration
from src.constants.colors import Colors
from src.constants.paths import Paths
from src.constants.state_names import StateNames
from src.entities.enemy import Enemy
from src.entities.player import Player
from src.helpers.screen_helper import ScreenHelper
from src.map.map_loader import MapData, MapLoader
from src.states.play_state import PlayState
from src.states.state import IState
from src.states.state_machine import StateMachine
from src.states.table_of_recods import TableOfRecords, TableRecord

class EndState(IState):
    def __init__(self, play_state: PlayState, state_machine: StateMachine, configuration: Configuration, screen: pygame.Surface) -> None:
        self.__play_state = play_state
        self.__state_machine = state_machine
        self.__configuration = configuration
        self.__screen = screen
        self.__is_filling = None
        self.__table_of_records = TableOfRecords()
        self.__player_name = ""

    def get_state_name(self) -> str:
        return StateNames.END

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__state_machine.stop()
            if event.type == pygame.KEYDOWN:
                if self.__is_filling:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.__add_new_record()
                            self.__state_machine.set_state(StateNames.HIGHSCORES)
                        elif event.key == pygame.K_BACKSPACE:
                            self.__player_name = self.__player_name[:-1]
                        else:
                            self.__player_name += event.unicode
                elif not self.__is_filling:
                    if event.key == pygame.K_ESCAPE:
                        self.__state_machine.set_state(StateNames.HIGHSCORES)
                        self.__play_state.reset()

    def __add_new_record(self) -> None:
        self.__table_of_records.save_record(TableRecord(self.__player_name, self.__play_state.player.score))

    def update(self) -> None:
        if self.__is_filling == None:
            records = self.__table_of_records.get_records()[:10]
            if self.__play_state.player.score:
                for record in records:
                    if record.score < self.__play_state.player.score:
                        self.__is_filling = True
                        return

            self.__is_filling = False
                    

    def draw(self) -> None:
        self.__screen.fill(Colors.BLACK)

        if not self.__is_filling:
            ScreenHelper.draw_text("GAME OVER",
                self.__screen,
                [305, 100],
                self.__configuration.text_configuration.font_size,
                Colors.YELLOW,
                self.__configuration.text_configuration.font_family,
                centered=True
            )

            ScreenHelper.draw_text("Press ESC to return",
                    self.__screen,
                    [self.__configuration.screen_configuration.screen_width // 2, self.__configuration.screen_configuration.screen_height - self.__configuration.text_configuration.font_size - 20],
                    self.__configuration.text_configuration.font_size,
                    Colors.WHITE,
                    self.__configuration.text_configuration.font_family,
                    True)
        elif self.__is_filling:
            ScreenHelper.draw_text("ENTER YOUR NAME: {0}".format(self.__player_name),
                self.__screen,
                [305, 100],
                self.__configuration.text_configuration.font_size - 10,
                Colors.YELLOW,
                self.__configuration.text_configuration.font_family,
                centered=True
            )