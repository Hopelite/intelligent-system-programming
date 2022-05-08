import json
import os
import pygame
from src.configuration.configuration import Configuration
from src.constants.colors import Colors
from src.constants.state_names import StateNames
from src.helpers.screen_helper import ScreenHelper
from src.states.state import IState
from src.states.state_machine import StateMachine

class TableRecord:
    def __init__(self, name: str, score: int) -> None:
        self.name = name
        self.score = score

class TableOfRecords:
    def __init__(self) -> None:
        file_path = os.path.join(os.path.dirname(__file__), "records.json")
        self.__reader = JsonReader(file_path)
        self.__writer = JsonWriter(file_path)

    def get_records(self) -> list[TableRecord]:
        return self.__reader.read()[0:10]

    def save_record(self, new_record: TableRecord) -> None:
        records = self.__reader.read()
        records.sort(key=lambda x: x.score, reverse=True)
        index = 0
        for record in records:
            if record.score < new_record.score:
                break
            index += 1

        records.insert(index, new_record)

        self.__writer.write(records)

class JsonReader:
    def __init__(self, path: str) -> None:
        self.__path = path

    def read(self) -> list[TableRecord]:
        records = []
        with open(self.__path, 'r') as file:
            data = json.load(file)

            for record in data:
                records.append(TableRecord(record['name'], int(record['score'])))

        return records

class JsonWriter:
    def __init__(self, path: str) -> None:
        self.__path = path

    def write(self, records: list[TableRecord]) -> None:
        json_records = json.dumps([ob.__dict__ for ob in records], indent=4)
        
        with open(self.__path, 'w') as file:
            file.write(json_records)

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
                                [self.__configuration.screen_configuration.screen_width//2, self.PADDING],
                                self.__configuration.text_configuration.font_size,
                                Colors.WHITE,
                                self.__configuration.text_configuration.font_family,
                                centered=True)

    def __draw_high_scores(self):
        self.__screen.fill(Colors.BLACK)
        records = self.__table_of_records.get_records()
        recordPosition = self.PADDING * 3
        for record in records:
            ScreenHelper.draw_text(record.name + ': ' + record.score.__str__(),
                                    self.__screen,
                                    [self.__configuration.screen_configuration.screen_width // 2, recordPosition],
                                    36,
                                    (190, 190, 190),
                                    "arial",
                                    centered=True)
            recordPosition += self.__configuration.text_configuration.font_size