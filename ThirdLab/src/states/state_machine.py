import pygame
from src.states.state import IState
from src.configuration.configuration import Configuration

class StateMachine:
    def __init__(self, configuration: Configuration, first_state_name: str, states: list[IState] = []) -> None:
        self.__configuration = configuration
        self.__state_name = first_state_name
        self.__states = states
        self.__clock = pygame.time.Clock()

    def add_state(self, state: IState) -> None:
        """Adds IState to StateMachine."""
        existing_state = self.__get_first_state_with_name(state.get_state_name())
        if existing_state != None:
            raise SuchStateAlreadyExistsException("IState with the name {0} already exists!".format(state.get_state_name()))
        
        self.__states.append(state)

    def start(self) -> None:
        """Starts StateMachine."""
        self.__is_running = True
        while self.__is_running:
            self.__update()
            self.__clock.tick(self.__configuration.screen_configuration.fps)

    def stop(self) -> None:
        self.__is_running = False

    def set_state(self, state_name: str) -> None:
        self.__state_name = state_name

    def __update(self) -> None:
        state = self.__get_first_state_with_name(self.__state_name)
        if state == None:
            raise NoSuchStateException("There is no state with the name {0}".format(self.__state_name))

        state.handle_events()
        state.update()
        state.draw()
        pygame.display.update()

    def __get_first_state_with_name(self, state_name: str) -> IState:
        return next((s for s in self.__states if s.get_state_name() == state_name), None)

class SuchStateAlreadyExistsException(Exception):
    pass

class NoSuchStateException(Exception):
    pass