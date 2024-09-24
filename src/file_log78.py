import os
import logging
from datetime import datetime
from .log_entry import LogEntry

class FileLog78:
    def __init__(self, filename="7788_.log", menu="logs"):
        self.menu = menu
        self.filename = filename
        self._logger = self._configure_logger()

    def _configure_logger(self):
        log_directory = os.path.join(os.getcwd(), self.menu)
        os.makedirs(log_directory, exist_ok=True)
        log_file = os.path.join(log_directory, self.filename)
        
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def log_to_file(self, log_entry: LogEntry):
        self._logger.info(log_entry.to_json())

    def clear(self):
        # 这个方法在Python版本中不需要实现,因为我们使用的是Python的logging模块
        pass

    def __del__(self):
        for handler in self._logger.handlers[:]:
            self._logger.removeHandler(handler)
            handler.close()