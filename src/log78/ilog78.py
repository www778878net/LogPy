from abc import ABC, abstractmethod
from typing import Optional, Union

class ILog78(ABC):
    @abstractmethod
    async def DETAIL(self, summary: str, message: Optional[Union[str, dict]] = None, level: int = 10):
        pass

    @abstractmethod
    async def DEBUG(self, summary: str, message: Optional[Union[str, dict]] = None, level: int = 20):
        pass

    @abstractmethod
    async def INFO(self, summary: str, message: Optional[Union[str, dict]] = None, level: int = 30):
        pass

    @abstractmethod
    async def WARN(self, summary: str, message: Optional[Union[str, dict]] = None, level: int = 50):
        pass

    @abstractmethod
    async def ERROR(self, summary: str, message: Optional[Union[str, dict]] = None, level: int = 60):
        pass

    @abstractmethod
    async def ERROR(self, error: Exception, summary: Optional[str] = None, level: int = 60):
        pass

    @abstractmethod
    async def ERROR(self, log_entry: dict, level: int = 60):
        pass

    @abstractmethod
    async def DEBUG(self, log_entry: dict, level: int = 20):
        pass

    @abstractmethod
    async def INFO(self, log_entry: dict, level: int = 30):
        pass

    @abstractmethod
    async def WARN(self, log_entry: dict, level: int = 50):
        pass

    @abstractmethod
    def setup(self, server_logger: Optional['IServerLog78'], file_logger: Optional['IFileLog78'], console_logger: Optional['IConsoleLog78']):
        pass

    @abstractmethod
    def set_environment(self, env: 'Log78.Environment'):
        pass

    @abstractmethod
    def setup_level(self, file_level: int, console_level: int, api_level: int):
        pass

    @abstractmethod
    def add_debug_key(self, key: str):
        pass

    @abstractmethod
    def clear_detail_log(self):
        pass

    @abstractmethod
    def setup_detail_file(self):
        pass