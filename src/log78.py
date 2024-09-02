import datetime
from typing import Optional, List
from .iserver_log78 import IServerLog78
from .iconsole_log78 import IConsoleLog78
from .ifile_log78 import IFileLog78
from .console_log78 import ConsoleLog78
from .file_log78 import FileLog78

class Log78:
    def __init__(self):
        self.debug_kind: List[str] = []
        self.level_file: int = 50
        self.level_console: int = 30
        self.level_api: int = 70
        self.server_logger: Optional[IServerLog78] = None
        self.console_logger: Optional[IConsoleLog78] = ConsoleLog78()
        self.file_logger: Optional[IFileLog78] = None
        self.uname: str = ""

    _instance: Optional['Log78'] = None

    @classmethod
    def instance(cls) -> 'Log78':
        if cls._instance is None:
            cls._instance = Log78()
            cls._instance.setup(None, FileLog78(), ConsoleLog78(), "guest")
        return cls._instance

    def setup(self, server_logger: Optional[IServerLog78], file_logger: Optional[IFileLog78], 
              console_logger: Optional[IConsoleLog78], _uname: str = "guest"):
        self.server_logger = server_logger
        self.console_logger = console_logger
        self.file_logger = file_logger
        self.uname = _uname

    def clone(self) -> 'Log78':
        new_log = Log78()
        new_log.server_logger = self.server_logger
        new_log.file_logger = self.file_logger
        new_log.console_logger = self.console_logger
        new_log.uname = self.uname
        new_log.level_api = self.level_api
        new_log.level_console = self.level_console
        new_log.level_file = self.level_file
        return new_log

    def log_err(self, exception: Exception, key1: str = "errwinpro", previous_method_name: str = ""):
        self.log(exception.args[0], 90, key1, previous_method_name, self.uname, str(exception))

    def log(self, message: str, level: int = 50, key1: str = "", key2: str = "", key3: str = "", 
            content: str = "", key4: str = "", key5: str = "", key6: str = ""):
        key1 = key1 or ""
        key2 = key2 or ""
        key3 = key3 or self.uname

        is_debug = any(k in self.debug_kind for k in [key1, key2, key3, key4, key5, key6])

        if is_debug or level >= self.level_api:
            if self.server_logger:
                self.server_logger.log_to_server(message, key1, level, key2, key3, content, key4, key5, key6)

        info = f"{datetime.datetime.now()}\t{message}~~{content}~~{key1}"
        
        if is_debug or level >= self.level_file:
            if self.file_logger:
                self.file_logger.log_to_file(info)

        if is_debug or level >= self.level_console:
            if self.console_logger:
                self.console_logger.write_line(info)