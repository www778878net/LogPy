from abc import ABC, abstractmethod

class IServerLog78(ABC):
    @abstractmethod
    def log_to_server(self, simple: str, key1: str, leave: int = 0, key2: str = "", key3: str = "", 
                      content: str = "", key4: str = "", key5: str = "", key6: str = ""):
        pass