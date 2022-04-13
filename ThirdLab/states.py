from abc import ABC, abstractmethod
import pygame
from constants import *

PADDING = 20

class IState(ABC):
    @abstractmethod
    def handle_events(self) -> None:
        pass
    
    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass
    
    def _draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        self._screen.blit(text, pos)

class StartState(IState):
    def __init__(self, screen: pygame.Surface, state_machine: s) -> None:
        self._screen = screen

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = PLAY

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.__screen.fill(BLACK)
        self._draw_text('PRESS SPACE', self.__screen, [
                       WIDTH//2, HEIGHT-50], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self._draw_text('HIGH SCORES', self.__screen, [WIDTH//2, PADDING],
                       START_TEXT_SIZE, (255, 255, 255), START_FONT, centered=True)
        pygame.display.update()