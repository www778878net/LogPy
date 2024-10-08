import asyncio
import aiohttp
from typing import Optional
from www778878net.log_entry import LogEntry, BasicInfo

class LogstashServerLog78:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self._logger = None

    @property
    def logger(self):
        if self._logger is None:
            from www778878net.log78 import Log78
            self._logger = Log78.instance()
        return self._logger

    async def log_to_server(self, log_json: str):
        try:
            return await asyncio.wait_for(self._log_to_server_internal(log_json), timeout=30)
        except Exception as ex:
            error_log_entry = LogEntry(basic=BasicInfo(
                summary="Logstash Error",
                message=f"Unexpected error in LogToServer: {str(ex)}",
                log_level="ERROR",
                log_level_number=60
            ))
            await self.logger.ERROR(error_log_entry)

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