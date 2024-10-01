import unittest
from unittest.mock import patch, MagicMock
from log78.logstash_server_log78 import LogstashServerLog78
from log78.log_entry import LogEntry, BasicInfo

class TestLogstashServerLog78(unittest.IsolatedAsyncioTestCase):
    async def test_log_to_server(self):
        server_url = "http://example.com"
        logger = LogstashServerLog78(server_url)

        log_entry = LogEntry(basic=BasicInfo(
            summary="Test summary",
            message="Test message",
            log_level="INFO",
            log_level_number=30
        ))
        log_json = log_entry.to_json()

        with patch('aiohttp.ClientSession.post') as mock_post:
            mock_response = MagicMock()
            mock_response.status = 200
            mock_post.return_value.__aenter__.return_value = mock_response

            await logger.log_to_server(log_json)

            mock_post.assert_called_once_with(
                server_url,
                data=log_json,
                headers={'Content-Type': 'application/json'},
                timeout=20
            )