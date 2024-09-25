import unittest
import asyncio
from log78.logstash_server_log78 import LogstashServerLog78
from log78.log_entry import LogEntry, BasicInfo
from unittest.mock import patch, MagicMock

class TestLogstashServerLog78(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.server_url = "http://example.com"
        self.logger = LogstashServerLog78(self.server_url)

    @patch('aiohttp.ClientSession.post')
    async def test_log_to_server(self, mock_post):
        # 模拟成功的响应
        mock_response = MagicMock()
        mock_response.status = 200
        mock_post.return_value.__aenter__.return_value = mock_response

        log_entry = LogEntry()
        log_entry.basic = BasicInfo()
        log_entry.basic.message = "Test message"
        log_entry.basic.summary = "Test summary"
        response = await self.logger.log_to_server(log_entry)

        self.assertIsNotNone(response)
        mock_post.assert_called_once_with(
            self.server_url,
            data=log_entry.to_json(),
            headers={'Content-Type': 'application/json'},
            timeout=20
        )

    @patch('aiohttp.ClientSession.post')
    async def test_log_to_server_error(self, mock_post):
        # 模拟错误响应
        mock_response = MagicMock()
        mock_response.status = 500
        mock_post.return_value.__aenter__.return_value = mock_response

        log_entry = LogEntry()
        log_entry.basic = BasicInfo()
        log_entry.basic.message = "Test message"
        log_entry.basic.summary = "Test summary"
        response = await self.logger.log_to_server(log_entry)

        self.assertIsNotNone(response)
        self.assertEqual(response.status, 500)

    @patch('aiohttp.ClientSession.post')
    async def test_log_to_server_timeout(self, mock_post):
        # 模拟超时
        mock_post.side_effect = asyncio.TimeoutError()

        log_entry = LogEntry()
        log_entry.basic = BasicInfo()
        log_entry.basic.message = "Test message"
        log_entry.basic.summary = "Test summary"
        response = await self.logger.log_to_server(log_entry)

        self.assertIsNone(response)

    # 添加更多测试...

if __name__ == '__main__':
    unittest.main()