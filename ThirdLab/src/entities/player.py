import pygame
from pygame import Vector2
from src.configuration.configuration import Configuration
from src.states.state import IState

class Player:
    def __init__(self, play_state: IState, pos, health):
        self.__play_state = play_state

        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = Vector2(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = health

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction*self.speed
        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        # Setting grid position in reference to pix pos
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER +
                            self.__play_state.cell_width//2)//self.__play_state.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER +
                            self.__play_state.cell_height//2)//self.__play_state.cell_height+1
        if self.on_coin():
            self.eat_coin()

    def draw(self):
        pygame.draw.circle(self.__play_state.screen, PLAYER_COLOUR, (int(self.pix_pos.x),
                                                            int(self.pix_pos.y)), self.__play_state.cell_width//2-2)

        # Drawing player lives
        for x in range(self.lives):
            pygame.draw.circle(self.__play_state.screen, PLAYER_COLOUR, (30 + 20*x, HEIGHT - 15), 7)

        # Drawing the grid pos rect
        # pygame.draw.rect(self.app.screen, RED, (self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_BUFFER//2,
        #                                         self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2, self.app.cell_width, self.app.cell_height), 1)

    def on_coin(self):
        if self.grid_pos in self.__play_state.coins:
            if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.__play_state.cell_width == 0:
                if self.direction == Vector2(1, 0) or self.direction == Vector2(-1, 0):
                    return True
            if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.__play_state.cell_height == 0:
                if self.direction == Vector2(0, 1) or self.direction == Vector2(0, -1):
                    return True
        return False

    def eat_coin(self):
        self.__play_state.coins.remove(self.grid_pos)
        self.current_score += 1

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return Vector2((self.grid_pos[0]*self.__play_state.cell_width)+TOP_BOTTOM_BUFFER//2+self.__play_state.cell_width//2,
                   (self.grid_pos[1]*self.__play_state.cell_height) +
                   TOP_BOTTOM_BUFFER//2+self.__play_state.cell_height//2)

    def time_to_move(self):
        if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.__play_state.cell_width == 0:
            if self.direction == Vector2(1, 0) or self.direction == Vector2(-1, 0) or self.direction == Vector2(0, 0):
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.__play_state.cell_height == 0:
            if self.direction == Vector2(0, 1) or self.direction == Vector2(0, -1) or self.direction == Vector2(0, 0):
                return True

    def can_move(self):
        for wall in self.__play_state.walls:
            if Vector2(self.grid_pos+self.direction) == wall:
                return False
        return True