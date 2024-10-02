import asyncio
import aiohttp
import time
from typing import Optional
from log78.log_entry import LogEntry, BasicInfo

class LogstashServerLog78:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self._logger = None
        self._error_count = 0
        self._last_attempt_time = 0
        self._retry_interval = 300  # 5分钟 = 300秒

    @property
    def logger(self):
        if self._logger is None:
            from log78.logger78 import Logger78
            self._logger = Logger78()  # 使用实例而不是单例
            self._logger.setup_level(99999, 20, 99999)  # 设置日志级别
        return self._logger

    async def log_to_server(self, log_json: str):
        current_time = time.time()
        if self._error_count >= 2 and (current_time - self._last_attempt_time) < self._retry_interval:
            return  # 暂时不发送日志

        if (current_time - self._last_attempt_time) >= self._retry_interval:
            self._error_count = 0  # 重置错误计数

        self._last_attempt_time = current_time

        try:
            return await asyncio.wait_for(self._log_to_server_internal(log_json), timeout=5)
        except asyncio.TimeoutError:
            self._handle_error("Logstash超时", "发送日志到Logstash服务器超时")
        except Exception as ex:
            self._handle_error("Logstash错误", f"发送日志到Logstash时发生意外错误: {str(ex)}")

    def _handle_error(self, summary, message):
        from log78.log_entry import LogEntry, BasicInfo  # 将导入移到函数内部
        self._error_count += 1
        error_log_entry = LogEntry(basic=BasicInfo(
            summary=summary,
            message=message,
            log_level="ERROR",
            log_level_number=60
        ))
        asyncio.create_task(self.logger.ERROR(error_log_entry))

    async def _log_to_server_internal(self, log_json: str):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.server_url, data=log_json, headers={'Content-Type': 'application/json'}, timeout=20) as response:
                    if response.status == 200:
                        success_log_entry = LogEntry(basic=BasicInfo(
                            summary="Logstash Success",
                            message="Logstash log sent successfully",
                            log_level="DEBUG",
                            log_level_number=20
                        ))
                        await self.logger.DEBUG(success_log_entry)
                    else:
                        error_message = f"Logstash server returned status code {response.status}"
                        error_log_entry = LogEntry(basic=BasicInfo(
                            summary="Logstash Error",
                            message=error_message,
                            log_level="ERROR",
                            log_level_number=60
                        ))
                        await self.logger.ERROR(error_log_entry)
                    return response
            except asyncio.TimeoutError:
                timeout_log_entry = LogEntry(basic=BasicInfo(
                    summary="Logstash Canceled",
                    message="HTTP request was canceled or timed out",
                    log_level="ERROR",
                    log_level_number=60
                ))
                await self.logger.ERROR(timeout_log_entry)
            except Exception as ex:
                error_message = f"Exception occurred while sending log to Logstash: {str(ex)}"
                exception_log_entry = LogEntry(basic=BasicInfo(
                    summary="Logstash Exception",
                    message=error_message,
                    log_level="ERROR",
                    log_level_number=60
                ))
                await self.logger.ERROR(exception_log_entry)
                raise

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 在这里可以添加清理代码,如果需要的话
        pass