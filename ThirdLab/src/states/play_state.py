import os.path
from random import randrange
import pygame
from pygame import Vector2
from src.configuration.configuration import Configuration
from src.constants.colors import Colors
from src.constants.paths import Paths
from src.constants.state_names import StateNames
from src.entities.enemy import Enemy, Personality
from src.entities.player import Player
from src.helpers.screen_helper import ScreenHelper
from src.map.map_loader import MapLoader
from src.states.state import IState
from src.states.state_machine import StateMachine

class PlayState(IState):
    WALLS_FILE_NAME = "walls.txt"
    BACKGROUND_TEXTURE_FILE_NAME = "maze.png"
    PACMAN_DEATH_SOUND_FILE = "pacman_death.wav"

    __colors = [Colors.RED, Colors.YELLOW, Colors.BLUE, Colors.GREEN]

    def __init__(self, state_machine: StateMachine, configuration: Configuration, screen: pygame.Surface) -> None:
        self.__state_machine = state_machine
        self.__configuration = configuration
        self.__death_sound = pygame.mixer.Sound(os.path.join(Paths.SOUNDS, self.PACMAN_DEATH_SOUND_FILE))
        pygame.time.set_timer(pygame.USEREVENT, 500)
        self.screen = screen
        self.reset()

    def get_state_name(self) -> str:
        return StateNames.PLAY

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__state_machine.stop()
            if event.type == pygame.USEREVENT:
                for enemy in self.enemies:
                    enemy.animate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(Vector2(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(Vector2(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(Vector2(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(Vector2(0, 1))

    def reset(self) -> None:
        self.__map_data = MapLoader(os.path.join(Paths.TEXTURES, self.WALLS_FILE_NAME)).load_map()
        background = pygame.image.load(os.path.join(Paths.TEXTURES, self.BACKGROUND_TEXTURE_FILE_NAME))
        self.__background = pygame.transform.scale(background, (self.__configuration.map_configuration.maze_width, self.__configuration.map_configuration.maze_height))
        self.enemies = []
        self.player = Player(self, self.__configuration, self.__map_data, Vector2(self.__map_data.player_position))
        self.__create_enemies()

    def update(self) -> None:
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.position == self.player.position:
                self.__damage_player()

    def draw(self) -> None:
        self.screen.fill(Colors.BLACK)
        self.screen.blit(self.__background, (self.__configuration.map_configuration.padding // 2, self.__configuration.map_configuration.padding // 2))
        self.__draw_coins()
        # ScreenHelper.draw_text('CURRENT SCORE: {}'.format(self.player.score),
        #                         self.__background,
        #                         [20, 0],
        #                         18,
        #                         Colors.WHITE,
        #                         self.__configuration.text_configuration.font_family)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()

    def __damage_player(self) -> None:
        self.player.lives -= 1
        if self.player.lives == 0:
            pygame.mixer.Sound.play(self.__death_sound)
            self.__state_machine.set_state(StateNames.END)
        else:
            self.player.reset_position()
            self.player.set_direction(Vector2(0,0))
            for enemy in self.enemies:
                enemy.reset_position()
                enemy.set_direction(Vector2(0,0))

    def __draw_coins(self):
        for coin in self.__map_data.coins:
            pygame.draw.circle(self.screen, 
                                Colors.YELLOW,
                               (int(coin.x * self.__configuration.map_configuration.cell_width) + self.__configuration.map_configuration.cell_width // 2 + self.__configuration.map_configuration.padding // 2,
                                int(coin.y * self.__configuration.map_configuration.cell_height) + self.__configuration.map_configuration.cell_height // 2 + self.__configuration.map_configuration.padding // 2),
                                5)

    def __create_enemies(self):
        for idx, pos in enumerate(self.__map_data.enemy_positions):
            personality = Personality.UNDEFINED

            if idx == 0:
                personality = Personality.FAST
            elif idx == 1:
                personality = Personality.SLOW

            color_index = randrange(0, len(self.__colors))
            self.enemies.append(Enemy(self, self.__configuration, self.__map_data, Vector2(pos), personality, self.__colors[color_index]))