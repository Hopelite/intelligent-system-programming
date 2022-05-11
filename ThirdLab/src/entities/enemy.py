from enum import Enum
import pygame
from pygame import Vector2
from src.entities.entity import Entity
from src.configuration.configuration import Configuration
from src.map.map_loader import MapData
import random

class Personality(Enum):
    UNDEFINED = 0
    FAST = 1
    SLOW = 2
    SCARED = 3

class Enemy(Entity):
    def __init__(self, play_state, configuration: Configuration, map_data: MapData, start_position, number: int) -> None:
        super().__init__(configuration.map_configuration, start_position)
        self.__play_state = play_state
        self.__configuration = configuration
        # self.lives = configuration.player_configuration.lives
        # self.__speed = configuration.player_configuration.speed
        # self.direction = Vector2(1, 0)
        # self.__next_direction = None
        self.__map_data = map_data
        # self.__is_able_to_move = True

        self.radius = int(self.__configuration.map_configuration.cell_width // 2.3)
        self.number = number

        self.colour = self.__set_colour()

        self.direction = Vector2(0, 0)
        self.personality = self.set_personality()
        self.target = None
        self.speed = self.set_speed()

    def update(self) -> None:
        self.target = self.set_target()
        if self.target != self.position:
            self._screen_position += self.direction * self.speed
            if self.time_to_move():
                self.move()

        self._update_grid_position()
                            
    def set_target(self):
        if self.personality == "speedy" or self.personality == "slow":
            return self.__play_state.player.position
        else:
            if self.__play_state.player.position[0] > self.__configuration.map_configuration.colums // 2 and self.__play_state.player.position[1] > self.__configuration.map_configuration.rows // 2:
                return Vector2(1, 1)
            if self.__play_state.player.position[0] > self.__configuration.map_configuration.colums // 2 and self.__play_state.player.position[1] < self.__configuration.map_configuration.rows // 2:
                return Vector2(1, self.__configuration.map_configuration.rows-2)
            if self.__play_state.player.position[0] < self.__configuration.map_configuration.colums // 2 and self.__play_state.player.position[1] > self.__configuration.map_configuration.rows // 2:
                return Vector2(self.__configuration.map_configuration.colums-2, 1)
            else:
                return Vector2(self.__configuration.map_configuration.colums-2, self.__configuration.map_configuration.rows-2)

    def draw(self) -> None:
        pygame.draw.circle(self.__play_state.screen, self.colour,
                           (int(self._screen_position.x), int(self._screen_position.y)), self.radius)
        
    def set_speed(self):
        if self.personality in ["speedy", "scared"]:
            speed = 2
        else:
            speed = 1
        return speed

    def __set_colour(self):
        if self.number == 0:
            return (43, 78, 203)
        if self.number == 1:
            return (197, 200, 27)
        if self.number == 2:
            return (189, 29, 29)
        if self.number == 3:
            return (215, 159, 33)
            
    def set_personality(self) -> str:
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        else:
            return "scared"
            
    def get_random_direction(self):
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = Vector2(self.position.x + x_dir, self.position.y + y_dir)
            if next_pos not in self.__map_data.walls:
                break
        return Vector2(x_dir, y_dir)

    def time_to_move(self):
        if int(self._screen_position.x + self._map_configuration.padding // 2) % self._map_configuration.cell_width == 0:
            if self.direction == Vector2(1, 0) or self.direction == Vector2(-1, 0) or self.direction == Vector2(0, 0):
                return True

        if int(self._screen_position.y + self._map_configuration.padding // 2) % self._map_configuration.cell_height == 0:
            if self.direction == Vector2(0, 1) or self.direction == Vector2(0, -1) or self.direction == Vector2(0, 0):
                return True

        return False

    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()
        else:
            self.direction = self.get_path_direction(self.target)

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.position[0]
        ydir = next_cell[1] - self.position[1]
        return Vector2(xdir, ydir)

    def find_next_cell_in_path(self, target):
        path = self.BFS([int(self.position.x), int(self.position.y)], [
                        int(target[0]), int(target[1])])
        return path[1]

    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.__map_data.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest