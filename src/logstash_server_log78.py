import asyncio
import aiohttp
from datetime import datetime
from typing import Optional
from .log_entry import LogEntry
from .log78 import Log78

class LogstashServerLog78:
    def __init__(self, server_url: str, level_file: int = 50):
        self.server_url = server_url
        self.throw_on_error = False
        self._semaphore = asyncio.Semaphore(10)  # 限制最大并发请求数为10
        self._logger = Log78()
        self._logger.setup_level(level_file, level_file, 99999)

    async def log_to_server(self, log_entry: LogEntry) -> Optional[aiohttp.ClientResponse]:
        async with self._semaphore:
            try:
                return await asyncio.wait_for(self._log_to_server_internal(log_entry), timeout=30)
            except asyncio.TimeoutError:
                await self._logger.ERROR(LogEntry(basic={"message": "LogToServer operation timed out", "summary": "Logstash Timeout"}))
                return None
            except Exception as ex:
                await self._logger.ERROR(LogEntry(basic={"message": f"Unexpected error in LogToServer: {str(ex)}", "summary": "Logstash Error"}))
                return None

    async def _log_to_server_internal(self, log_entry: LogEntry) -> Optional[aiohttp.ClientResponse]:
        try:
            json_content = log_entry.to_json()
            async with aiohttp.ClientSession() as session:
                async with session.post(self.server_url, data=json_content, headers={'Content-Type': 'application/json'}, timeout=20) as response:
                    if response.status < 400:
                        await self._logger.DEBUG(LogEntry(basic={"message": "Logstash log sent successfully", "summary": "Logstash Success"}))
                    else:
                        error_message = f"Failed to send log to Logstash. Status code: {response.status}"
                        await self._logger.ERROR(LogEntry(basic={"message": error_message, "summary": "Logstash Error"}))
                        if self.throw_on_error:
                            raise aiohttp.ClientError(error_message)
                    return response
        except asyncio.TimeoutError:
            await self._logger.ERROR(LogEntry(basic={"message": "HTTP request was canceled or timed out", "summary": "Logstash Canceled"}))
            return None
        except Exception as ex:
            error_message = f"Error sending log to Logstash: {str(ex)}"
            await self._logger.ERROR(LogEntry(basic={"message": error_message, "summary": "Logstash Exception"}))
            if self.throw_on_error:
                raise
            return None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 在这里可以添加清理代码,如果需要的话
        pass