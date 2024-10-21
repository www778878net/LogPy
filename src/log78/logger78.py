import asyncio
import os
from enum import Enum
from typing import Optional, Dict, Any, Tuple, Union
from datetime import datetime
from log78.log_entry import LogEntry, BasicInfo, ErrorInfo
from log78.iserver_log78 import IServerLog78
from log78.iconsole_log78 import IConsoleLog78
from log78.ifile_log78 import IFileLog78
from log78.console_log78 import ConsoleLog78
from log78.file_log78 import FileLog78
from log78.file_log_detail import FileLogDetail
import traceback

from log78.logstash_server_log78 import LogstashServerLog78

class Environment(Enum):
    Production = 0
    Development = 1
    Testing = 2

class Logger78:
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
    def instance(cls) -> 'Logger78':
        if not hasattr(cls, "_instance"):
            cls._instance = Logger78()
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
            self.level_console = 30  # INFO
            self.level_file = 30     # INFO
            self.level_api = 50      # WARN
        elif self.current_environment == Environment.Development:
            self.level_console = 20  # DEBUG
            self.level_file = 20     # DEBUG
            self.level_api = 30      # INFO
        elif self.current_environment == Environment.Testing:
            self.level_console = 30  # INFO
            self.level_file = 30     # INFO
            self.level_api = 50      # INFO

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

            is_debug = self.is_debug_key(log_entry)
            log_json = None

            # 如果存在 debug 文件记录器或满足输出条件，才转换为 JSON
            if self.debug_file_logger or is_debug or log_entry.basic.log_level_number >= min(self.level_api, self.level_file, self.level_console):
                log_json = log_entry.to_json()

            # Debug 文件总是记录日志
            if self.debug_file_logger:
                self.debug_file_logger.log_to_file(log_json)

            # 如果不满足任何输出条件，直接返回
            if not is_debug and log_entry.basic.log_level_number < min(self.level_api, self.level_file, self.level_console):
                return

            if is_debug or log_entry.basic.log_level_number >= self.level_api:
                if self.server_logger:
                    try:
                        await self.server_logger.log_to_server(log_json)
                    except Exception as ex:
                        print(f"Error in server logging: {ex}")

            if is_debug or log_entry.basic.log_level_number >= self.level_file:
                if self.file_logger:
                    self.file_logger.log_to_file(log_json)

            if is_debug or log_entry.basic.log_level_number >= self.level_console:
                if self.console_logger:
                    self.console_logger.write_line(log_json)

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

    async def DETAIL(self, summary_or_log_entry: Union[str, LogEntry], message: Any = None, level: int = 10):
        if isinstance(summary_or_log_entry, LogEntry):
            log_entry = summary_or_log_entry
            log_entry.basic.log_level = "DETAIL"
            log_entry.basic.log_level_number = level
        else:
            log_entry = LogEntry(basic=BasicInfo(
                summary=summary_or_log_entry,
                message=message,
                log_level="DETAIL",
                log_level_number=level
            ))
        await self.process_log_internal(log_entry)

    async def DEBUG(self, summary_or_log_entry: Union[str, LogEntry], message: Any = None, level: int = 20):
        if isinstance(summary_or_log_entry, LogEntry):
            log_entry = summary_or_log_entry
            log_entry.basic.log_level = "DEBUG"
            log_entry.basic.log_level_number = level
        else:
            log_entry = LogEntry(basic=BasicInfo(
                summary=summary_or_log_entry,
                message=message,
                log_level="DEBUG",
                log_level_number=level
            ))
        await self.process_log_internal(log_entry)

    async def INFO(self, summary_or_log_entry: Union[str, LogEntry], message: Any = None, level: int = 30):
        
        if isinstance(summary_or_log_entry, LogEntry):
            log_entry = summary_or_log_entry
            log_entry.basic.log_level = "INFO"
            log_entry.basic.log_level_number = level
        else:
            log_entry = LogEntry(basic=BasicInfo(
                summary=summary_or_log_entry,
                message=message,
                log_level="INFO",
                log_level_number=level
            ))
        
        await self.process_log_internal(log_entry)
        

    async def WARN(self, summary_or_log_entry: Union[str, LogEntry], message: Any = None, level: int = 50):
        if isinstance(summary_or_log_entry, LogEntry):
            log_entry = summary_or_log_entry
            log_entry.basic.log_level = "WARN"
            log_entry.basic.log_level_number = level
        else:
            log_entry = LogEntry(basic=BasicInfo(
                summary=summary_or_log_entry,
                message=message,
                log_level="WARN",
                log_level_number=level
            ))
        await self.process_log_internal(log_entry)

    async def ERROR(self, summary_or_log_entry: Union[str, LogEntry, Exception], message: Any = None, level: int = 60):
        if isinstance(summary_or_log_entry, LogEntry):
            log_entry = summary_or_log_entry
            log_entry.basic.log_level = "ERROR"
            log_entry.basic.log_level_number = level
        elif isinstance(summary_or_log_entry, Exception):
            log_entry = LogEntry(
                basic=BasicInfo(
                    summary=str(summary_or_log_entry),
                    message=message,
                    log_level="ERROR",
                    log_level_number=level
                ),
                error=ErrorInfo(
                    error_type=type(summary_or_log_entry).__name__,
                    error_message=str(summary_or_log_entry),
                    error_stack_trace=traceback.format_exc()
                )
            )
        else:
            log_entry = LogEntry(basic=BasicInfo(
                summary=summary_or_log_entry,
                message=message,
                log_level="ERROR",
                log_level_number=level
            ))
        await self.process_log_internal(log_entry)

    def setup_level(self, file_level: int, console_level: int, api_level: int):
        self.level_file = file_level
        self.level_console = console_level
        self.level_api = api_level

    def get_current_levels(self) -> Tuple[int, int, int]:
        return (self.level_file, self.level_console, self.level_api)

    def clone(self) -> 'Logger78':
        cloned = Logger78()
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

# 在文件末尾添加以下测试代码
if __name__ == "__main__":
    import asyncio

    async def test_log78():
        logger = Logger78.instance()
        logger.setup(
          LogstashServerLog78(f"http://192.168.31.132:5000"),
          FileLog78(),
          ConsoleLog78()
      )
        logger.setup_level(file_level=10, console_level=10, api_level=10)  # 设置所有级别为最低，确保所有日志都会输出

        # 测试不同级别的日志
        await logger.INFO("这是一条 INFO 日志")
        await logger.DETAIL("这是一条 DETAIL 日志")
        await logger.DEBUG("这是一条 DEBUG 日志")        
        await logger.WARN("这是一条 WARN 日志")
        await logger.ERROR("这是一条 ERROR 日志")

        # 测试使用 LogEntry 对象
        log_entry = LogEntry(basic=BasicInfo(
            summary="测试 LogEntry",
            message="这是使用 LogEntry 对象的日志",
            log_level="INFO",
            log_level_number=30
        ))
        await logger.INFO(log_entry)

    # 运行测试函数
    asyncio.run(test_log78())