import os
import datetime
from .ifile_log78 import IFileLog78

class FileLog78(IFileLog78):
    log_path = "/"

    def __init__(self, _menu: str = ""):
        self._menu = _menu
        self.file = self._get_file_name()
        self.clear()

    @property
    def menu(self) -> str:
        return self._menu

    @menu.setter
    def menu(self, value: str):
        self._menu = value

    def _get_file_name(self) -> str:
        idate = datetime.datetime.now().day % 3
        return f"{self._menu}{idate}.txt"

    def log_to_file(self, message: str = ""):
        try:
            with open(os.path.join(self.log_path, self.file), "a") as f:
                f.write(message)
        except:
            pass

    def clear(self):
        idate = datetime.datetime.now().day % 3
        for i in range(3):
            if i == idate:
                continue
            try:
                os.remove(os.path.join(self.log_path, f"{self._menu}{i}.txt")))
            except FileNotFoundError:
                pass