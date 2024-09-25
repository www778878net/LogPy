from abc import ABC, abstractmethod
from typing import Optional, Union

class ILog78(ABC):
    @abstractmethod
    async def detail(self, summary: str, message: Optional[Union[str, dict]] = None, level: int = 10):
        pass

    @abstractmethod
    async def debug(self, summary: str, message: Optional[Union[str, dict]] = None, level: int = 20):
        pass

    @abstractmethod
    async def info(self, summary: str, message: Optional[Union[str, dict]] = None, level: int = 30):
        pass

    @abstractmethod
    async def warn(self, summary: str, message: Optional[Union[str, dict]] = None, level: int = 50):
        pass

    @abstractmethod
    async def error(self, summary: str, message: Optional[Union[str, dict]] = None, level: int = 60):
        pass

    @abstractmethod
    async def error(self, error: Exception, summary: Optional[str] = None, level: int = 60):
        pass

    @abstractmethod
    async def error(self, log_entry: dict, level: int = 60):
        pass

    @abstractmethod
    async def debug(self, log_entry: dict, level: int = 20):
        pass

    @abstractmethod
    async def info(self, log_entry: dict, level: int = 30):
        pass

    @abstractmethod
    async def warn(self, log_entry: dict, level: int = 50):
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