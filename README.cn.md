
<h1 align="center">Log78</h1>
<div align="center">

[English](./README.md) | 简体中文

[![License](https://img.shields.io/badge/license-Apache%202-green.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![测试状态](https://github.com/www778878net/Log78/actions/workflows/BuildandTest.yml/badge.svg?branch=main)](https://github.com/www778878net/Log78/actions/workflows/BuildandTest.yml)
[![QQ群](https://img.shields.io/badge/QQ群-323397913-blue.svg?style=flat-square&color=12b7f5&logo=qq)](https://qm.qq.com/cgi-bin/qm/qr?k=it9gUUVdBEDWiTOH21NsoRHAbE9IAzAO&jump_from=webapi&authKey=KQwSXEPwpAlzAFvanFURm0Foec9G9Dak0DmThWCexhqUFbWzlGjAFC7t0jrjdKdL)
</div>

## 反馈QQ群（点击加入）：[323397913](https://qm.qq.com/cgi-bin/qm/qr?k=it9gUUVdBEDWiTOH21NsoRHAbE9IAzAO&jump_from=webapi&authKey=KQwSXEPwpAlzAFvanFURm0Foec9G9Dak0DmThWCexhqUFbWzlGjAFC7t0jrjdKdL)

# Log78

Log78 是一个灵活的 Python 日志库,支持控制台、文件和服务器日志记录。

## 安装

使用 pip 安装 Log78:

```
pip install log78
```

## 快速开始

Log78 提供了两种记录日志的方式:一种是简单的方法用于快速记录,另一种是使用 `LogEntry` 对象进行更详细的记录。以下是如何使用简单方法开始:

```python
from log78 import Log78

# 获取 Log78 实例 - 无需设置!
log = Log78.instance()

# 记录一条简单的消息
await log.INFO("你好, Log78!")

# 使用摘要和自定义级别记录
await log.WARN("这是一个警告", "警告摘要", 60)
```

对于更详细的日志记录,您可以使用 `LogEntry` 对象:

```python
from log78 import LogEntry, BasicInfo

log_entry = LogEntry(basic=BasicInfo(message="详细的日志消息", summary="日志摘要"))
await log.INFO(log_entry)
```

这两种方法都可以直接使用,默认支持控制台和文件日志记录。

## 高级配置 (可选)

如果您需要自定义日志行为,可以使用 `setup` 方法:

```python
from log78 import Log78, ServerLog78, FileLog78, ConsoleLog78

# 创建自定义日志记录器实例(如果需要)
server_logger = ServerLog78()
file_logger = FileLog78("custom_logfile")
console_logger = ConsoleLog78()

# 设置自定义日志记录器
log = Log78.instance()
log.setup(server_logger, file_logger, console_logger)
```

## 属性

- `debug_kind`: 用于控制记录哪些类型日志的日志调试关键字集合。
- `level_file`, `level_console`, `level_api`: 分别表示文件日志、控制台日志和API日志的阈值级别。
- `debug_entry`: 用于设置更细粒度的调试条件。

## 建议的日志级别

- DEBUG (10): 详细的调试信息,通常仅在开发环境中使用
- INFO (30): 一般信息,可用于跟踪正常的应用程序操作
- WARN (50): 警告信息,表示潜在问题但不影响主要功能
- ERROR (60): 错误和严重问题,需要立即关注

## 示例: 调整日志级别

```python
from log78 import Log78, LogEntry, BasicInfo

log = Log78.instance()

# 将控制台日志级别调整为0以打印所有日志(用于调试)
log.level_console = 0
# 将文件日志级别调整为60,只记录更严重的警告和错误
log.level_file = 60

# 使用不同级别记录日志
log_entry = LogEntry(basic=BasicInfo(message="调试信息"))
await log.DEBUG(log_entry)  # 只会输出到控制台

log_entry.basic.message = "一般信息"
await log.INFO(log_entry)  # 会输出到控制台,不会记录到文件

log_entry.basic.message = "警告"
await log.WARN(log_entry)  # 会记录到控制台和文件

log_entry.basic.message = "错误"
await log.ERROR(log_entry)  # 会记录到控制台、文件和API
```

## 方法

- `DEBUG`, `INFO`, `WARN`, `ERROR`: 记录不同级别的日志。
- `ERROR(Exception, LogEntry)`: 记录异常错误日志。

## 使用 LogEntry 类

`LogEntry` 类提供了结构化信息用于详细日志记录:

```python
from log78 import Log78, LogEntry, BasicInfo, EventInfo, HttpInfo

log_entry = LogEntry()
log_entry.basic = BasicInfo(
    summary="用户登录成功",
    log_level_number=30,
    log_level="INFO",
    message="用户 johndoe 成功登录系统",
    service_name="AuthService",
    user_id="user123",
    user_name="johndoe"
)

log_entry.event = EventInfo(
    event_category="authentication",
    event_action="login",
    event_outcome="success"
)

log_entry.http = HttpInfo(
    http_request_method="POST",
    http_request_body_content="{\"username\":\"johndoe\",\"password\":\"*****\"}",
    http_response_status_code=200,
    url_original="https://api.example.com/login"
)

# 添加自定义属性
log_entry.add_property("customField", "customValue")

await log.INFO(log_entry)
```

## 其他

更多详细信息,请参阅项目的 [GitHub 仓库](https://github.com/www778878net/Log78) 或 [API 文档](http://www.778878.net/docs/#/Log78/)。
