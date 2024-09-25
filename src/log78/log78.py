import asyncio
import os
from enum import Enum
from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from .log_entry import LogEntry, BasicInfo, ErrorInfo
from .iserver_log78 import IServerLog78
from .iconsole_log78 import IConsoleLog78
from .ifile_log78 import IFileLog78
from .console_log78 import ConsoleLog78
from .file_log78 import FileLog78
from .file_log_detail import FileLogDetail

class Environment(Enum):
    Production = 0
    Development = 1
    Testing = 2

class Log78:
    def __init__(self):
        self.debug_kind = set()
        self.level_file = 30
        self.level_console = 60
        self.level_api = 50
        self.server_logger: Optional[IServerLog78] = None
        self.console_logger: Optional[IConsoleLog78] = ConsoleLog78()
        self.file_logger: Optional[IFileLog78] = FileLog78()
        self.debug_file_logger: Optional[IFileLog78] = None
        self.debug_entry: Optional[LogEntry] = None
        self.current_environment = Environment.Production
        self.custom_properties: Dict[str, Any] = {}
        self._lock = asyncio.Lock()
        self._semaphore = asyncio.Semaphore(1)
        self.set_environment_from_env_var()

    @classmethod
    def instance(cls) -> 'Log78':
        if not hasattr(cls, "_instance"):
            cls._instance = Log78()
            cls._instance.setup(None, FileLog78(), ConsoleLog78())
        return cls._instance

    def set_environment_from_env_var(self):
        env_var = os.environ.get("LOG78_ENVIRONMENT")
        if env_var:
            try:
                self.set_environment(Environment[env_var])
            except KeyError:
                self.set_environment(Environment.Production)
        else:
            self.set_environment(Environment.Production)

    def set_environment(self, env: Environment):
        self.current_environment = env
        self.update_log_levels()
        self.setup_debug_file_logger()

    def update_log_levels(self):
        if self.current_environment == Environment.Production:
            self.level_console = 60  # ERROR
            self.level_file = 30     # INFO
            self.level_api = 30      # INFO
        elif self.current_environment == Environment.Development:
            self.level_console = 20  # DEBUG
            self.level_file = 20     # DEBUG
            self.level_api = 30      # INFO
        elif self.current_environment == Environment.Testing:
            self.level_console = 60  # ERROR
            self.level_file = 20     # DEBUG
            self.level_api = 30      # INFO

    def setup_debug_file_logger(self):
        if self.current_environment == Environment.Development:
            self.debug_file_logger = FileLogDetail()
        else:
            self.debug_file_logger = None

    def setup(self, server_logger: Optional[IServerLog78], file_logger: Optional[IFileLog78], console_logger: Optional[IConsoleLog78]):
        self.server_logger = server_logger
        self.file_logger = file_logger or self.file_logger
        self.console_logger = console_logger or self.console_logger

    def setup_detail_file(self):
        self.debug_file_logger = FileLogDetail()

    def clear_detail_log(self):
        if self.debug_file_logger:
            self.debug_file_logger.clear()

    def add_property(self, key: str, value: Any):
        self.custom_properties[key] = value

    async def process_log_internal(self, log_entry: Optional[LogEntry]):
        async with self._semaphore:
            if log_entry is None or log_entry.basic is None:
                await self.ERROR(LogEntry(basic=BasicInfo(message="Error: LogEntry or LogEntry.Basic is null")))
                return

            async with self._lock:
                for key, value in self.custom_properties.items():
                    log_entry.add_property(key, value)

            if self.debug_file_logger:
                self.debug_file_logger.log_to_file(log_entry)

            is_debug = self.is_debug_key(log_entry)

            if is_debug or log_entry.basic.log_level_number >= self.level_api:
                if self.server_logger:
                    try:
                        await self.server_logger.log_to_server(log_entry)
                    except Exception as ex:
                        print(f"Error in server logging: {ex}")

            if is_debug or log_entry.basic.log_level_number >= self.level_file:
                if self.file_logger:
                    self.file_logger.log_to_file(log_entry)

            if is_debug or log_entry.basic.log_level_number >= self.level_console:
                if self.console_logger:
                    self.console_logger.write_line(log_entry)

    def is_debug_key(self, log_entry: LogEntry) -> bool:
        if self.debug_entry and self.debug_entry.basic:
            return (self.debug_entry.basic.service_name and log_entry.basic.service_name and 
                    self.debug_entry.basic.service_name.lower() == log_entry.basic.service_name.lower()) or \
                   (self.debug_entry.basic.service_obj and log_entry.basic.service_obj and 
                    self.debug_entry.basic.service_obj.lower() == log_entry.basic.service_obj.lower()) or \
                   (self.debug_entry.basic.service_fun and log_entry.basic.service_fun and 
                    self.debug_entry.basic.service_fun.lower() == log_entry.basic.service_fun.lower()) or \
                   (self.debug_entry.basic.user_id and log_entry.basic.user_id and 
                    self.debug_entry.basic.user_id.lower() == log_entry.basic.user_id.lower()) or \
                   (self.debug_entry.basic.user_name and log_entry.basic.user_name and 
                    self.debug_entry.basic.user_name.lower() == log_entry.basic.user_name.lower())

        keys_to_check = [
            log_entry.basic.service_name,
            log_entry.basic.service_obj,
            log_entry.basic.service_fun,
            log_entry.basic.user_id,
            log_entry.basic.user_name
        ]

        return any(key and key.lower() in self.debug_kind for key in keys_to_check if key)

    async def DETAIL(self, summary: str, message: Any = None, level: int = 10):
        await self.DETAIL(LogEntry(basic=BasicInfo(summary=summary, message=message, log_level_number=level)))

    async def DEBUG(self, summary: str, message: Any = None, level: int = 20):
        await self.DEBUG(LogEntry(basic=BasicInfo(summary=summary, message=message, log_level_number=level)))

    async def INFO(self, summary: str, message: Any = None, level: int = 30):
        await self.INFO(LogEntry(basic=BasicInfo(summary=summary, message=message, log_level_number=level)))

    async def WARN(self, summary: str, message: Any = None, level: int = 50):
        await self.WARN(LogEntry(basic=BasicInfo(summary=summary, message=message, log_level_number=level)))

    async def ERROR(self, summary: str, message: Any = None, level: int = 60):
        await self.ERROR(LogEntry(basic=BasicInfo(summary=summary, message=message, log_level_number=level)))

    async def ERROR(self, error: Exception, summary: Optional[str] = None, level: int = 60):
        log_entry = LogEntry(
            basic=BasicInfo(summary=summary or str(error), log_level_number=level),
            error=ErrorInfo(
                error_type=type(error).__name__,
                error_message=str(error),
                error_stack_trace=error.__traceback__
            )
        )
        await self.ERROR(log_entry)

    async def DETAIL(self, log_entry: LogEntry, level: int = 10):
        log_entry.basic.log_level = "DETAIL"
        log_entry.basic.log_level_number = level
        await self.process_log_internal(log_entry)

    async def DEBUG(self, log_entry: LogEntry, level: int = 20):
        log_entry.basic.log_level = "DEBUG"
        log_entry.basic.log_level_number = level
        await self.process_log_internal(log_entry)

    async def INFO(self, log_entry: LogEntry, level: int = 30):
        log_entry.basic.log_level = "INFO"
        log_entry.basic.log_level_number = level
        await self.process_log_internal(log_entry)

    async def WARN(self, log_entry: LogEntry, level: int = 50):
        log_entry.basic.log_level = "WARN"
        log_entry.basic.log_level_number = level
        await self.process_log_internal(log_entry)

    async def ERROR(self, log_entry: LogEntry, level: int = 60):
        log_entry.basic.log_level = "ERROR"
        log_entry.basic.log_level_number = level
        await self.process_log_internal(log_entry)

    def setup_level(self, file_level: int, console_level: int, api_level: int):
        self.level_file = file_level
        self.level_console = console_level
        self.level_api = api_level

    def get_current_levels(self) -> Tuple[int, int, int]:
        return (self.level_file, self.level_console, self.level_api)

    def clone(self) -> 'Log78':
        cloned = Log78()
        cloned.server_logger = self.server_logger
        cloned.file_logger = self.file_logger
        cloned.console_logger = self.console_logger
        cloned.level_api = self.level_api
        cloned.level_console = self.level_console
        cloned.level_file = self.level_file
        cloned.current_environment = self.current_environment
        cloned.custom_properties = self.custom_properties.copy()  # 确保复制自定义属性
        return cloned

    async def add_debug_key(self, key: str):
        async with self._lock:
            self.debug_kind.add(key.lower())