from abc import ABC, abstractmethod

class IConsoleLog78(ABC):
    @abstractmethod
    def write_line(self, message: str):
        pass