class ScreenConfiguration:
    """Contains screen configuration."""
    @property
    def screen_width(self) -> int:
        return self.__screen_width

    @screen_width.setter
    def screen_width(self, value: int) -> None:
        self.__screen_width = value
        
    @property
    def screen_height(self) -> int:
        return self.__screen_height

    @screen_height.setter
    def screen_height(self, value: int) -> None:
        self.__screen_height = value
        
    @property
    def fps(self) -> int:
        return self.__fps

    @fps.setter
    def fps(self, value: int) -> None:
        self.__fps = value

class TextConfiguration:
    """Contains text configuration."""
    @property
    def font_size(self) -> int:
        return self.__font_size

    @font_size.setter
    def font_size(self, value: int) -> None:
        self.__font_size = value
        
    @property
    def font_family(self) -> str:
        return self.__font_family

    @font_family.setter
    def font_family(self, value: str) -> None:
        self.__font_family = value

class PlayerConfiguration:
    """Contains player configuration."""
    @property
    def speed(self) -> int:
        return self.__speed

    @speed.setter
    def speed(self, value: int) -> None:
        self.__speed = value
        
    @property
    def lives(self) -> str:
        return self.__lives

    @lives.setter
    def lives(self, value: str) -> None:
        self.__lives = value

class MapConfiguration:
    """Contains map configuration"""
    @property
    def rows(self) -> int:
        return self.__rows

    @rows.setter
    def rows(self, value: int) -> None:
        self.__rows = value
        
    @property
    def colums(self) -> int:
        return self.__colums

    @colums.setter
    def colums(self, value: int) -> None:
        self.__colums = value
        
    @property
    def padding(self) -> int:
        return self.__padding

    @padding.setter
    def padding(self, value: int) -> None:
        self.__padding = value

    @property
    def maze_width(self) -> int:
        return self.__maze_width

    @maze_width.setter
    def maze_width(self, value: int) -> None:
        self.__maze_width = value
        
    @property
    def maze_height(self) -> int:
        return self.__maze_height

    @maze_height.setter
    def maze_height(self, value: int) -> None:
        self.__maze_height = value
        
    @property
    def cell_width(self) -> int:
        return self.__cell_width

    @cell_width.setter
    def cell_width(self, value: int) -> None:
        self.__cell_width = value
        
    @property
    def cell_height(self) -> int:
        return self.__cell_height

    @cell_height.setter
    def cell_height(self, value: int) -> None:
        self.__cell_height = value

class EnemyConfiguration:
    """Contains enemies configuration."""
    @property
    def speed(self) -> int:
        return self.__speed

    @speed.setter
    def speed(self, value: int) -> None:
        self.__speed = value 

class Configuration:
    """Contains game configurations."""
    __screen_configuration = ScreenConfiguration()
    __text_configuration = TextConfiguration()
    __player_configuration = PlayerConfiguration()
    __map_configuration = MapConfiguration()
    __enemy_configuration = EnemyConfiguration()

    @property
    def screen_configuration(self) -> ScreenConfiguration:
        return self.__screen_configuration
        
    @property
    def text_configuration(self) -> TextConfiguration:
        return self.__text_configuration
        
    @property
    def player_configuration(self) -> PlayerConfiguration:
        return self.__player_configuration
        
    @property
    def map_configuration(self) -> MapConfiguration:
        return self.__map_configuration
        
    @property
    def enemy_configuration(self) -> EnemyConfiguration:
        return self.__enemy_configuration