from .log_entry import LogEntry

class ConsoleLog78:
    def __init__(self):
        pass  # 不需要初始化 logging

    def write_line(self, log_json: str):
        print(log_json)  # 直接打印 JSON 字符串

    def __del__(self):
        pass  # 不需要清理 logging handlers