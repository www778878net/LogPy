from abc import ABC, abstractmethod
from typing import Optional

class IServerLog78(ABC):
    @property
    @abstractmethod
    def server_url(self) -> str:
        pass

    @server_url.setter
    @abstractmethod
    def server_url(self, value: str):
        pass

    @abstractmethod
    async def log_to_server(self, log_json: str) -> Optional[dict]:
        pass