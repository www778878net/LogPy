import os
from loguru import logger

class FileLog78:
    def __init__(self, filename="7788_{time:YYYY-MM-DD_HH}.log", menu="logs"):
        self.menu = menu
        self.filename = filename
        self._configure_logger()

    def _configure_logger(self):
        log_directory = os.path.join(os.getcwd(), self.menu)
        os.makedirs(log_directory, exist_ok=True)
        log_file = os.path.join(log_directory, self.filename)
        
        logger.remove()  # 移除默认的处理器
        logger.add(
            log_file,
            rotation="1h",  # 每小时轮换一次
            retention="1 week",  # 保留一周的日志
            compression="zip",  # 压缩旧日志
            format="{message}",  # 只记录消息内容
            encoding="utf-8",  # 指定编码为 UTF-8
            serialize=False,  # 不序列化日志记录
            enqueue=True  # 使用队列来写入日志，避免 I/O 阻塞
        )

    def log_to_file(self, log_json: str):
        logger.info(log_json)

    def clear(self):
        # 使用 loguru 时，这个方法可能不需要实现
        pass

    def __del__(self):
        # loguru 会自动处理文件关闭，所以这里不需要特别的清理代码
        pass