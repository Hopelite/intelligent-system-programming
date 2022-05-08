import pygame

class ScreenHelper:
    @staticmethod
    def draw_text(text: str, screen: pygame.Surface, pos, size: int, colour, font_name: str, centered: bool = False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(text, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)