import unittest
from log78 import Log78, Environment
from log78.log_entry import LogEntry, BasicInfo
import pytest
from log78 import Log78
from unittest.mock import patch, MagicMock

class TestLog78(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.logger = Log78()  # 假设 Log78 是一个普通类，而不是单例

    def test_environment_settings(self):
        self.logger.set_environment(Environment.Development)
        self.assertEqual(self.logger.current_environment, Environment.Development)

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

@pytest.mark.asyncio
async def test_info_with_text_only():
    logger = Log78.instance()
    
    # 打印当前环境和日志级别
    print(f"当前环境: {logger.current_environment}")
    file_level, console_level, api_level = logger.get_current_levels()
    print(f"当前日志级别 - 文件: {file_level}, 控制台: {console_level}, API: {api_level}")

    # 确保我们在开发模式下
    logger.set_environment(Environment.Development)
    print(f"环境设置为: {logger.current_environment}")
    file_level, console_level, api_level = logger.get_current_levels()
    print(f"更新后的日志级别 - 文件: {file_level}, 控制台: {console_level}, API: {api_level}")

    # 使用 MagicMock 来模拟 ConsoleLog78
    mock_console_logger = MagicMock()
    logger.console_logger = mock_console_logger

    test_message = "这是一条测试信息日志"
    await logger.INFO(test_message)

    # 验证是否调用了 console_logger 的 write_line 方法
    mock_console_logger.write_line.assert_called_once()
    
    # 获取传递给 write_line 的 LogEntry 对象
    if mock_console_logger.write_line.call_args:
        log_entry = mock_console_logger.write_line.call_args[0][0]
        
        # 验证 LogEntry 的内容
        assert log_entry.basic.summary == test_message
        assert log_entry.basic.log_level == "INFO"
        assert log_entry.basic.log_level_number == 30

    else:
        pytest.fail("write_line was not called with any arguments")

    # 打印调试信息
    print(f"控制台日志记录器模拟调用: {mock_console_logger.mock_calls}")
    print(f"write_line 模拟调用: {mock_console_logger.write_line.mock_calls}")

if __name__ == '__main__':
    unittest.main()