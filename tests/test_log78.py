import unittest
from log78 import Log78, Environment, FileLog78
from log78.log_entry import LogEntry, BasicInfo
import pytest
from log78 import Log78
from unittest.mock import patch, MagicMock
import sys
import os
import json
import asyncio

class TestLog78(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.logger = Log78()  # 假设 Log78 是一个普通类，而不是单例

    async def test_environment_settings(self):
        self.logger.set_environment(Environment.Development)
        self.assertEqual(self.logger.current_environment, Environment.Development)

        # 添加日志记录测试
        test_message = "这是一条测试信息日志"
        await self.logger.INFO(test_message)

        # 等待一小段时间，确保日志被写入
        await asyncio.sleep(0.1)

        # 检查 detail.log 文件是否存在并有内容
        detail_log_file = os.path.join(os.getcwd(), "logs", "detail.log")
        if os.path.exists(detail_log_file):
            with open(detail_log_file, 'r', encoding='utf-8') as f:
                log_content = f.read()
                print(f"detail.log 内容: {log_content}")
                self.assertIn("这是一条测试信息日志", log_content)
        else:
            self.fail("detail.log 文件不存在")

        # 检查当前日志级别
        file_level, console_level, api_level = self.logger.get_current_levels()
        print(f"当前日志级别 - 文件: {file_level}, 控制台: {console_level}, API: {api_level}")
        self.assertEqual(file_level, 20)  # DEBUG level for file in Development environment
        self.assertEqual(console_level, 20)  # DEBUG level for console in Development environment
        self.assertEqual(api_level, 30)  # INFO level for API in Development environment

    async def test_log_levels(self):
        log_entry = LogEntry()
        log_entry.basic.message = "Debug message"
        log_entry.basic.log_level = "DEBUG"
        log_entry.basic.log_level_number = 20
        await self.logger.DEBUG(log_entry)
        # 这里需要添加断言来验证日志是否正确记录

    async def test_custom_log_entry(self):
        custom_entry = LogEntry()
        custom_entry.basic.message = "Custom log entry"
        custom_entry.basic.log_level = "INFO"
        custom_entry.basic.log_level_number = 30
        await self.logger.INFO(custom_entry)
        # 这里需要添加断言来验证自定义日志是否正确记录

    def test_clone(self):
        original_logger = Log78()
        original_logger.set_environment(Environment.Development)

        cloned_logger = original_logger.clone()

        self.assertEqual(original_logger.current_environment, cloned_logger.current_environment)
        self.assertEqual(original_logger.get_current_levels(), cloned_logger.get_current_levels())

        original_logger.set_environment(Environment.Production)
        self.assertNotEqual(original_logger.current_environment, cloned_logger.current_environment)

    # 添加更多测试...


if __name__ == '__main__':
    pytest.main([__file__, '-s', '-v'])