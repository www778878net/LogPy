import logging
from .log_entry import LogEntry

class ConsoleLog78:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def write_line(self, log_entry: LogEntry):
        self._logger.info(log_entry.to_json())

    def __del__(self):
        for handler in self._logger.handlers[:]:
            self._logger.removeHandler(handler)
            handler.close()