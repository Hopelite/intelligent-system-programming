import pygame
from pygame.math import Vector2
import sys
from constants import *
from player import *
from enemy import *
from table_of_records import TableOfRecords, TableRecord
from abc import ABC, abstractmethod

PADDING = 20

pygame.init()

class IState(ABC):
    @abstractmethod
    def get_state_name(self) -> str:
        pass
    
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
        screen.blit(text, pos)

class StateMachine:
    def __init__(self, first_state_name: str, states: list[IState] = []) -> None:
        self.__states = states
        self.state_name = first_state_name
        self.is_running = True
        self.__clock = pygame.time.Clock()

    def add_state(self, state: IState) -> None:
        """Adds IState to StateMachine."""
        existing_state = self.__get_first_state_with_name(state.get_state_name())
        if existing_state != None:
            raise Exception("IState with the name " + state.get_state_name() + " already exists!")
        
        self.__states.append(state)

    def run(self) -> None:
        while self.is_running:
            self.__update()
            self.__clock.tick(FPS)

    def __update(self) -> None:
        """Searches for IState with the same state name and uses it."""
        state = self.__get_first_state_with_name(self.state_name)
        if state == None:
            raise Exception("There is no state with name " + self.state_name)

        state.handle_events()
        state.update()
        state.draw()
        pygame.display.update()

    def __get_first_state_with_name(self, state_name: str) -> IState:
        return next((s for s in self.__states if s.get_state_name() == state_name), None)

class MenuOption:
    def __init__(self, text: str, state_name: str) -> None:
        self.text = text
        self.state_name = state_name
        
class MenuState(IState):
    def __init__(self, state_machine: StateMachine, screen: pygame.Surface) -> None:
        self.__state_machine = state_machine
        self.__screen = screen
        self.__row_highlighted = 0
        self.__menu_options = [MenuOption("START", START), MenuOption("HIGHSCORES", RECORDS),
        MenuOption("INFO", INFO)]

    def get_state_name(self) -> str:
        return MENU
    
    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__state_machine.is_running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if self.__row_highlighted == 3:
                    self.__row_highlighted = 0
                else:
                    self.__row_highlighted += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_Up:
                if self.__row_highlighted == 0:
                    self.__row_highlighted = 3
                else:
                    self.__row_highlighted -= 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER:
                self.__state_machine.state_name = START

    def update(self) -> None:
        pass
    
    def draw(self) -> None:
        self.__screen.fill(BLACK)
        font_size = 46
        recordPosition = HEIGHT - PADDING - font_size
        text_color = (190, 190, 190)
        for index, option in enumerate(self.__menu_options):
            if index == self.__row_highlighted:
                text_color = (190, 190, 190)
            else:
                text_color = SELECTED_COLOR
            self._draw_text(option.text, self.__screen, [WIDTH//2, recordPosition],  font_size, text_color, "arial", centered=True)
            recordPosition -= font_size
        # self._draw_text("HIGHSCORES", self.__screen, [WIDTH//2, recordPosition],  font_size, (190, 190, 190), "arial", centered=True)
        # recordPosition -= font_size
        # self._draw_text("INFO", self.__screen, [WIDTH//2, recordPosition],  font_size, (190, 190, 190), "arial", centered=True)
        # recordPosition -= font_size
        # self._draw_text("QUIT", self.__screen, [WIDTH//2, recordPosition],  font_size, (190, 190, 190), "arial", centered=True)
        # recordPosition -= font_size
    
class StartState(IState):
    def __init__(self, state_machine: StateMachine, screen: pygame.Surface) -> None:
        self.__state_machine = state_machine
        self.__screen = screen
        self.__table_of_records = TableOfRecords()

    def get_state_name(self) -> str:
        return START
    
    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__state_machine.is_running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__state_machine.state_name = PLAY

    def update(self) -> None:
        pass
    
    def draw(self) -> None:
        self.__screen.fill(BLACK)
        self.__draw_high_scores()
        self._draw_text('PRESS SPACE', self.__screen, [
                       WIDTH//2, HEIGHT-50], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self._draw_text('HIGH SCORES', self.__screen, [WIDTH//2, PADDING],
                       START_TEXT_SIZE, (255, 255, 255), START_FONT, centered=True)

    def __draw_high_scores(self):
        self.__screen.fill(BLACK)
        records = self.__table_of_records.get_records()
        recordPosition = PADDING * 3
        for record in records:
            self._draw_text(record.name + ': ' + record.score.__str__(), self.__screen, [WIDTH//2, recordPosition],  36, (190, 190, 190), "arial", centered=True)
            recordPosition += 46

class PlayState(IState):
    def __init__(self, state_machine: StateMachine, screen: pygame.Surface) -> None:
        self.cell_width = MAZE_WIDTH//COLS
        self.cell_height = MAZE_HEIGHT//ROWS
        self.__state_machine = state_machine
        self.screen = screen
        self.walls = []
        self.coins = []
        self.enemies = []
        self.__enemies_positions = []
        self.__load_map()
        self.player = Player(self, Vector2(self.player_positions), 3)
        self.__create_enemies()
        self.__table_of_records = TableOfRecords()

    def get_state_name(self) -> str:
        return PLAY

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__state_machine.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(Vector2(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(Vector2(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(Vector2(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(Vector2(0, 1))

    def update(self) -> None:
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.__remove_life()

    def draw(self) -> None:
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.__draw_coins()
        self._draw_text('CURRENT SCORE: {}'.format(self.player.current_score),
                       self.screen, [60, 0], 18, WHITE, START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()

    def __remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.__state_machine.state_name = END
            self.__add_new_record_if_required(TableRecord("Test", self.player.current_score))
        else:
            self.player.grid_pos = Vector2(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = Vector2(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def __add_new_record_if_required(self, new_record: TableRecord):
        self.__table_of_records.save_record(new_record)

    def __draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)

    def __load_map(self) -> None:
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(Vector2(xidx, yidx))
                    elif char == "0":
                        self.coins.append(Vector2(xidx, yidx))
                    elif char == "P":
                        self.player_positions = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:
                        self.__enemies_positions.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height,
                                                                  self.cell_width, self.cell_height))

    def __create_enemies(self):
        for idx, pos in enumerate(self.__enemies_positions):
            self.enemies.append(Enemy(self, Vector2(pos), idx))

    def __draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0),
                             (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height),
                             (WIDTH, x*self.cell_height))

class EndState(IState):
    def __init__(self, state_machine: StateMachine, screen: pygame.Surface, play_state: PlayState) -> None:
        self.__state_machine = state_machine
        self.__screen = screen
        self._play_state = play_state

    def get_state_name(self) -> str:
        return END

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.__screen.fill(BLACK)
        self._draw_text("GAME OVER", self.__screen, [
                       WIDTH//2, HEIGHT//2],  36, (190, 190, 190), "arial", centered=True)
        self._draw_text("Press the escape button to QUIT", self.__screen, [
                       WIDTH//2, HEIGHT//1.5],  36, (190, 190, 190), "arial", centered=True)
    
    def __reset(self):
        self._play_state.player.lives = 3
        self._play_state.player.current_score = 0
        self._play_state.player.grid_pos = Vector2(self._play_state.player.starting_pos)
        self._play_state.player.pix_pos = self._play_state.player.get_pix_pos()
        self._play_state.player.direction *= 0
        for enemy in self._play_state.enemies:
            enemy.grid_pos = Vector2(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == '0':
                        self.coins.append(Vector2(xidx, yidx))
        self.__state_machine.state_name = PLAY

class Application():
    def __init__(self) -> None:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.__state_machine = StateMachine(MENU)
        play_state = PlayState(self.__state_machine, screen)
        self.__state_machine.add_state(MenuState(self.__state_machine, screen))
        self.__state_machine.add_state(StartState(self.__state_machine, screen))
        self.__state_machine.add_state(play_state)
        self.__state_machine.add_state(EndState(self.__state_machine, screen, play_state))

    def run(self):
        self.__state_machine.run()
        pygame.quit()
        sys.exit()