from abc import ABC, abstractmethod

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