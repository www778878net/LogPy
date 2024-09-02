from abc import ABC, abstractmethod

class IFileLog78(ABC):
    @property
    @abstractmethod
    def menu(self) -> str:
        pass

    @menu.setter
    @abstractmethod
    def menu(self, value: str):
        pass

    @abstractmethod
    def log_to_file(self, message: str = ""):
        pass

    @abstractmethod
    def clear(self):
        pass