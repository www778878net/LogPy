from abc import ABC, abstractmethod

class IFileLog78(ABC):
    @abstractmethod
    def log_to_file(self, log_json: str):
        pass

    @abstractmethod
    def clear(self):
        pass