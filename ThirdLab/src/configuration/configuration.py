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

class Configuration:
    """Contains game configurations."""
    __screen_configuration = ScreenConfiguration()
    __text_configuration = TextConfiguration()

    @property
    def screen_configuration(self) -> ScreenConfiguration:
        return self.__screen_configuration
        
    @property
    def text_configuration(self) -> TextConfiguration:
        return self.__text_configuration