from abc import ABC, abstractmethod
from pygame import Vector2
from src.configuration.configuration import MapConfiguration

class Entity(ABC):
    def __init__(self, configuration: MapConfiguration, start_position) -> None:
        self._map_configuration = configuration
        self._start_position = [start_position.x, start_position.y]
        self.position = start_position
        self._screen_position = self._get_screen_position()

    def reset_position(self) -> None:
        self.position = self._start_position[:]
        self._screen_position = self._get_screen_position()

    @abstractmethod
    def update(self) -> None:
        pass
    
    @abstractmethod
    def draw(self) -> None:
        pass

    def _get_screen_position(self) -> Vector2:
        return Vector2((self.position[0] * self._map_configuration.cell_width) + self._map_configuration.padding // 2 + self._map_configuration.cell_width // 2,
                    (self.position[1] * self._map_configuration.cell_height) +
                    self._map_configuration.padding // 2 + self._map_configuration.cell_height // 2)

    def _update_grid_position(self) -> None:
        self.position[0] = (self._screen_position[0] - self._map_configuration.padding +
                            self._map_configuration.cell_width // 2) // self._map_configuration.cell_width + 1
        self.position[1] = (self._screen_position[1] - self._map_configuration.padding +
                            self._map_configuration.cell_height // 2) // self._map_configuration.cell_height + 1
