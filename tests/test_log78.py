import unittest
from src.log78 import Log78, Environment
from src.log_entry import LogEntry, BasicInfo

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

if __name__ == '__main__':
    unittest.main()