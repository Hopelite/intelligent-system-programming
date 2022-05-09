from pygame import Vector2
from src.constants.map_marks import MapMarks

class MapData:
    walls = []

    coins = []

    enemies = []

    enemy_positions = []

    player = None

    player_position = []

class MapLoader:
    def __init__(self, file_path: str) -> None:
        self.__file_path = file_path

    def load_map(self) -> MapData:
        map_data = MapData()
        with open(self.__file_path, 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == MapMarks.WALL:
                        map_data.walls.append(Vector2(x, y))
                    elif char == MapMarks.COIN:
                        map_data.coins.append(Vector2(x, y))
                    elif char == MapMarks.PLAYER:
                        map_data.player_position = [x, y]
                    elif char in MapMarks.ENEMY:
                        map_data.enemy_positions.append([x, y])
        
        return map_data