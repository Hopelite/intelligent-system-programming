import os.path

class Paths:
    SOURCE = os.path.dirname(os.path.dirname(__file__))

    SOUNDS = os.path.join(SOURCE, 'sounds')
    
    TEXTURES = os.path.join(SOURCE, 'textures')