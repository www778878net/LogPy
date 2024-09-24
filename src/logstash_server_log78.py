import asyncio
import aiohttp
from datetime import datetime
from typing import Optional
from .log_entry import LogEntry, BasicInfo
from .log78 import Log78

class LogstashServerLog78:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self._logger = Log78.instance()

    async def log_to_server(self, log_entry: LogEntry):
        try:
            return await asyncio.wait_for(self._log_to_server_internal(log_entry), timeout=30)
        except Exception as ex:
            error_log_entry = LogEntry()
            error_log_entry.basic = BasicInfo()
            error_log_entry.basic.summary = "Logstash Error"
            error_log_entry.basic.message = f"Unexpected error in LogToServer: {str(ex)}"
            await self._logger.ERROR(error_log_entry)

    async def _log_to_server_internal(self, log_entry: LogEntry):
        json_content = log_entry.to_json()
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.server_url, data=json_content, headers={'Content-Type': 'application/json'}, timeout=20) as response:
                    if response.status == 200:
                        success_log_entry = LogEntry()
                        success_log_entry.basic = BasicInfo()
                        success_log_entry.basic.summary = "Logstash Success"
                        success_log_entry.basic.message = "Logstash log sent successfully"
                        await self._logger.DEBUG(success_log_entry)
                    else:
                        error_message = f"Logstash server returned status code {response.status}"
                        error_log_entry = LogEntry()
                        error_log_entry.basic = BasicInfo()
                        error_log_entry.basic.summary = "Logstash Error"
                        error_log_entry.basic.message = error_message
                        await self._logger.ERROR(error_log_entry)
                    return response
            except asyncio.TimeoutError:
                timeout_log_entry = LogEntry()
                timeout_log_entry.basic = BasicInfo()
                timeout_log_entry.basic.summary = "Logstash Canceled"
                timeout_log_entry.basic.message = "HTTP request was canceled or timed out"
                await self._logger.ERROR(timeout_log_entry)
            except Exception as ex:
                error_message = f"Exception occurred while sending log to Logstash: {str(ex)}"
                exception_log_entry = LogEntry()
                exception_log_entry.basic = BasicInfo()
                exception_log_entry.basic.summary = "Logstash Exception"
                exception_log_entry.basic.message = error_message
                await self._logger.ERROR(exception_log_entry)
                raise

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 在这里可以添加清理代码,如果需要的话
        pass