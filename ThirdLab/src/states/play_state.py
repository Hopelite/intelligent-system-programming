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
from src.states.state import IState
from src.states.state_machine import StateMachine
from src.states.table_of_recods import TableOfRecords

class PlayState(IState):
    WALLS_FILE_NAME = "walls.txt"
    BACKGROUND_TEXTURE_FILE_NAME = "maze.png"

    def __init__(self, state_machine: StateMachine, configuration: Configuration, screen: pygame.Surface) -> None:
        self.__state_machine = state_machine
        self.__configuration = configuration

        # self.__maze_width = self.__configuration.screen_configuration.screen_width - self.__configuration.map_configuration.padding
        # self.__maze_height = self.__configuration.screen_configuration.screen_height - self.__configuration.map_configuration.padding

        self.screen = screen
        self.__table_of_records = TableOfRecords()
        self.__map_data = MapLoader(os.path.join(Paths.TEXTURES, self.WALLS_FILE_NAME)).load_map()
        
        background = pygame.image.load(os.path.join(Paths.TEXTURES, self.BACKGROUND_TEXTURE_FILE_NAME))
        self.__background = pygame.transform.scale(background, (self.__configuration.map_configuration.maze_width, self.__configuration.map_configuration.maze_height))

        # self.__cell_width = self.__maze_width // self.__configuration.map_configuration.colums
        # self.__cell_height = self.__maze_height // self.__configuration.map_configuration.rows

        # self.__state_machine = state_machine
        # self.screen = screen
        # self.walls = []
        # self.coins = []
        self.enemies = []
        # self.__enemies_positions = []
        # self.__load_map()

        self.player = Player(self, self.__configuration, self.__map_data, Vector2(self.__map_data.player_position))
        self.__create_enemies()

    def get_state_name(self) -> str:
        return StateNames.PLAY

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__state_machine.stop()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(Vector2(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(Vector2(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(Vector2(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(Vector2(0, 1))

    def update(self) -> None:
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        # for enemy in self.enemies:
        #     if enemy.grid_pos == self.player.grid_pos:
        #         self.__remove_life()

    def draw(self) -> None:
        self.screen.fill(Colors.BLACK)
        self.screen.blit(self.__background, (self.__configuration.map_configuration.padding // 2, self.__configuration.map_configuration.padding // 2))
        self.__draw_coins()
        ScreenHelper.draw_text('CURRENT SCORE: {}'.format(self.player.score),
                                self.__background,
                                [60, 0],
                                18,
                                Colors.WHITE,
                                self.__configuration.text_configuration.font_family)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()

    # def __remove_life(self):
    #     self.player.lives -= 1
    #     if self.player.lives == 0:
    #         self.__state_machine.state_name = END
    #         self.__add_new_record_if_required(TableRecord("Test", self.player.current_score))
    #     else:
    #         self.player.grid_pos = Vector2(self.player.starting_pos)
    #         self.player.pix_pos = self.player.get_pix_pos()
    #         self.player.direction *= 0
    #         for enemy in self.enemies:
    #             enemy.grid_pos = Vector2(enemy.starting_pos)
    #             enemy.pix_pos = enemy.get_pix_pos()
    #             enemy.direction *= 0

    # def __add_new_record_if_required(self, new_record: TableRecord):
    #     self.__table_of_records.save_record(new_record)

    def __draw_coins(self):
        for coin in self.__map_data.coins:
            pygame.draw.circle(self.screen, 
                                # (124, 123, 7),
                                Colors.YELLOW,
                               (int(coin.x * self.__configuration.map_configuration.cell_width) + self.__configuration.map_configuration.cell_width // 2 + self.__configuration.map_configuration.padding // 2,
                                int(coin.y * self.__configuration.map_configuration.cell_height) + self.__configuration.map_configuration.cell_height // 2 + self.__configuration.map_configuration.padding // 2),
                                5)

    # def __load_map(self) -> None:
    #     self.background = pygame.image.load('maze.png')
    #     self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

    #     with open("walls.txt", 'r') as file:
    #         for yidx, line in enumerate(file):
    #             for xidx, char in enumerate(line):
    #                 if char == "1":
    #                     self.walls.append(Vector2(xidx, yidx))
    #                 elif char == "0":
    #                     self.coins.append(Vector2(xidx, yidx))
    #                 elif char == "P":
    #                     self.player_positions = [xidx, yidx]
    #                 elif char in ["2", "3", "4", "5"]:
    #                     self.__enemies_positions.append([xidx, yidx])
    #                 elif char == "B":
    #                     pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height,
    #                                                               self.cell_width, self.cell_height))

    def __create_enemies(self):
        for idx, pos in enumerate(self.__map_data.enemy_positions):
            self.enemies.append(Enemy(self, self.__configuration, self.__map_data, Vector2(pos), idx))

    # def __draw_grid(self):
    #     for x in range(WIDTH//self.cell_width):
    #         pygame.draw.line(self.background, GREY, (x*self.cell_width, 0),
    #                          (x*self.cell_width, HEIGHT))
    #     for x in range(HEIGHT//self.cell_height):
    #         pygame.draw.line(self.background, GREY, (0, x*self.cell_height),
    #                          (WIDTH, x*self.cell_height))