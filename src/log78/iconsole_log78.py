from abc import ABC, abstractmethod

class IConsoleLog78(ABC):
    @abstractmethod
    def write_line(self, log_json: str):
        pass