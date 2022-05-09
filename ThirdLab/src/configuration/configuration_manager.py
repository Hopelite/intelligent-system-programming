import json
from src.configuration.configuration import Configuration
from abc import ABC, abstractmethod

class IConfigurationManager(ABC):
    @abstractmethod
    def load_configuration(self) -> Configuration:
        pass

class JSONConfigurationManager(IConfigurationManager):
    def __init__(self, path_to_file: str) -> None:
        self.__file_path = path_to_file

    def load_configuration(self) -> Configuration:
        with open(self.__file_path, 'r') as file:
            data = json.load(file)
            return JSONConfigurationManager.__deserialize(data)
            
    @staticmethod
    def __deserialize(configs) -> Configuration:
        configuration = Configuration()
        configuration.screen_configuration.screen_width = configs["screenSettings"]['screenWidth']
        configuration.screen_configuration.screen_height = configs["screenSettings"]['screenHeight']
        configuration.screen_configuration.fps = configs["screenSettings"]['FPS']

        configuration.text_configuration.font_size = configs["textSettings"]['font_size']
        configuration.text_configuration.font_family = configs["textSettings"]['font_family']

        return configuration