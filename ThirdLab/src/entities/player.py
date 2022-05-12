import pygame
from pygame import Vector2
from src.constants.colors import Colors
from src.configuration.configuration import Configuration
from src.entities.entity import Entity
from src.map.map_loader import MapData

class Player(Entity):
    def __init__(self, play_state, configuration: Configuration, map_data: MapData, start_position):
        super().__init__(configuration.map_configuration, start_position)
        self.__play_state = play_state
        self.__configuration = configuration
        self.lives = configuration.player_configuration.lives
        self.__speed = configuration.player_configuration.speed
        self.__current_direction = Vector2(1, 0)
        self.__next_direction = None
        self.__map_data = map_data
        self.__is_able_to_move = True
        self.score = 0

    def update(self) -> None:
        if self.__is_able_to_move:
            self._screen_position += self.__current_direction * self.__speed
        if self.is_time_to_move():
            if self.__next_direction != None:
                self.__current_direction = self.__next_direction
            self.__is_able_to_move = self.__can_move()

        self._update_grid_position()

        if self.__is_on_coin():
            self.__eat_coin()

    def draw(self) -> None:
        pygame.draw.circle(self.__play_state.screen,
            Colors.YELLOW,
            (int(self._screen_position.x), int(self._screen_position.y)),
            self._map_configuration.cell_width // 2 - 2)

        for live in range(self.lives):
            pygame.draw.circle(self.__play_state.screen, Colors.YELLOW, (30 + 20 * live, self.__configuration.screen_configuration.screen_height - 15), 7)
    
    def set_direction(self, direction: Vector2):
        self.__current_direction = direction

    def __is_on_coin(self):
        if self.position in self.__map_data.coins:
            if int(self._screen_position.x + self._map_configuration.padding // 2) % self._map_configuration.cell_width == 0:
                if self.__current_direction == Vector2(1, 0) or self.__current_direction == Vector2(-1, 0):
                    return True

            if int(self._screen_position.y + self._map_configuration.padding // 2) % self._map_configuration.cell_height == 0:
                if self.__current_direction == Vector2(0, 1) or self.__current_direction == Vector2(0, -1):
                    return True

        return False

    def __eat_coin(self):
        self.__map_data.coins.remove(self.position)
        self.score += 1

    def move(self, direction: Vector2) -> None:
        self.__next_direction = direction

    def is_time_to_move(self) -> bool:
        if int(self._screen_position.x + self._map_configuration.padding // 2) % self._map_configuration.cell_width == 0:
            if self.__current_direction == Vector2(1, 0) or self.__current_direction == Vector2(-1, 0) or self.__current_direction == Vector2(0, 0):
                return True

        if int(self._screen_position.y + self._map_configuration.padding // 2) % self._map_configuration.cell_height == 0:
            if self.__current_direction == Vector2(0, 1) or self.__current_direction == Vector2(0, -1) or self.__current_direction == Vector2(0, 0):
                return True

        return False

    def __can_move(self) -> bool:
        for wall in self.__map_data.walls:
            if Vector2(self.position + self.__current_direction) == wall:
                return False

        return True