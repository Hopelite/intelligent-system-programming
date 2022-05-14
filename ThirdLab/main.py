import os
import sys
from src.configuration.configuration_manager import JSONConfigurationManager
from src.game import Game

if __name__ == '__main__':
    file_path = os.path.join(os.path.dirname(__file__), 'configuration.json')
    game = Game(JSONConfigurationManager(file_path))
    game.run()
    sys.exit()