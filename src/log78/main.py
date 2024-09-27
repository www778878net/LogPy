import asyncio
from log78 import Log78, LogEntry, BasicInfo, Environment

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

async def main():
    print("Log78 演示程序")
    print("1. 基本日志记录")
    await demo_basic_logging()
    
    print("\n2. 详细日志记录")
    await demo_detailed_logging()

if __name__ == "__main__":
    asyncio.run(main())
