import os
import json
from .log_entry import LogEntry

class FileLogDetail:
    def __init__(self, filename="detail.log", menu="logs"):
        self.file_path = os.path.join(menu, filename)
        os.makedirs(menu, exist_ok=True)      

    def log_to_file(self, log_entry: LogEntry):
        try:
            log_string = f"<AI_FOCUS_LOG>{log_entry.to_json()}</AI_FOCUS_LOG>\n"
            with open(self.file_path, 'a', encoding='utf-8') as f:  # 添加 encoding='utf-8'
                f.write(log_string)
        except Exception as ex:
            print(f"写入详细日志文件时出错: {ex}")

    def clear(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:  # 添加 encoding='utf-8'
            f.write('')

    def close(self):
        # Python会自动关闭文件,所以这里不需要特别的操作
        pass