import asyncio
from log78 import Log78, LogEntry, BasicInfo, Environment
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

async def demo_basic_logging():
    log = Log78.instance()
    log.set_environment(Environment.Development)

    await log.INFO("这是一条基本的信息日志")
    await log.WARN("这是一条警告日志", "警告摘要")
    await log.ERROR("这是一条错误日志", "错误摘要", 70)

async def demo_detailed_logging():
    log = Log78.instance()
    
    log_entry = LogEntry()
    log_entry.basic = BasicInfo(
        summary="用户登录",
        message="用户 John Doe 成功登录",
        service_name="AuthService",
        user_id="user123"
    )
    
    await log.INFO(log_entry)

async def test_file_logging():
    log = Log78.instance()
    log.set_environment(Environment.Development)

    await log.INFO("这是一条写入文件的中文日志测试")
    await log.WARN("警告：包含特殊字符 !@#$%^&*()_+")
    await log.ERROR("错误：包含 Unicode 字符 ♠♥♦♣")
    
    log_entry = LogEntry(basic=BasicInfo(
        summary="复杂日志条目",
        message="这是一个包含多种信息的日志条目",
        service_name="测试服务",
        user_id="user_123"
    ))
    await log.INFO(log_entry)

    print("请检查日志文件以确认中文和特殊字符是否正确显示")

async def main():
    print("Log78 演示程序")
    print("文件日志测试")
    await test_file_logging()

if __name__ == "__main__":
    asyncio.run(main())
