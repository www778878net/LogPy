# Log78

Log78 is a flexible Python logging library that supports console, file, and server logging.

## Installation

Install Log78 using pip:

```
pip install log78
```

## Quick Start

Log78 provides two ways to log messages: a simple method for quick logging and a more detailed method using `LogEntry` objects. Here's how to get started with the simple method:

```python
from log78 import Log78

# Get the Log78 instance - no setup required!
log = Logger78.instance()

# Log a simple message
await log.INFO("Hello, Log78!")

# Log with a summary and custom level
await log.WARN("This is a warning", "Warning Summary", 60)
```

For more detailed logging, you can use the `LogEntry` object:

```python
from log78 import LogEntry, BasicInfo

log_entry = LogEntry(basic=BasicInfo(message="Detailed log message", summary="Log Summary"))
await log.INFO(log_entry)
```

Both methods are ready to use out of the box with default console and file logging.

## Advanced Configuration (Optional)

If you need custom logging behavior, you can use the `setup` method:

```python
from log78 import Logger78. ServerLog78, FileLog78, ConsoleLog78

# Create custom logger instances if needed
server_logger = ServerLog78()
file_logger = FileLog78("custom_logfile")
console_logger = ConsoleLog78()

# Setup custom loggers
log = Logger78.instance()
log.setup(server_logger, file_logger, console_logger)
```

## Properties

- `debug_kind`: A set of log debugging keywords used to control which types of logs are recorded.
- `level_file`, `level_console`, `level_api`: Respectively represent the threshold levels for file logs, console logs, and API logs.
- `debug_entry`: Used to set more fine-grained debugging conditions.

## Suggested Log Levels

- DEBUG (10): Detailed debug information, typically used only in development environments
- INFO (30): General information, can be used to track normal application operations
- WARN (50): Warning information, indicating potential issues but not affecting main functionality
- ERROR (60): Errors and serious problems that require immediate attention

## Example: Adjusting Log Levels

```python
from log78 import Logger78. LogEntry, BasicInfo

log = Logger78.instance()

# Adjust console log level to 0 to print all logs (for debugging)
log.level_console = 0
# Adjust file log level to 60 to only record more severe warnings and errors
log.level_file = 60

# Using different levels to record logs
log_entry = LogEntry(basic=BasicInfo(message="Debug information"))
await log.DEBUG(log_entry)  # Will only output to console

log_entry.basic.message = "General information"
await log.INFO(log_entry)  # Will output to console, not recorded in file

log_entry.basic.message = "Warning"
await log.WARN(log_entry)  # Will be recorded in both console and file

log_entry.basic.message = "Error"
await log.ERROR(log_entry)  # Will be recorded in console, file, and API
```

## Methods

- `DEBUG`, `INFO`, `WARN`, `ERROR`: Record logs of different levels.
- `ERROR(Exception, LogEntry)`: Records exception error logs.

## Using the LogEntry Class

The `LogEntry` class provides structured information for detailed logging:

```python
from log78 import Logger78. LogEntry, BasicInfo, EventInfo, HttpInfo

log_entry = LogEntry()
log_entry.basic = BasicInfo(
    summary="User login successful",
    log_level_number=30,
    log_level="INFO",
    message="User johndoe successfully logged into the system",
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

# Add custom properties
log_entry.add_property("customField", "customValue")

await log.INFO(log_entry)
```

## Other

For more detailed information, please refer to the project's [GitHub repository](https://github.com/www778878net/Log78) or the [API documentation](http://www.778878.net/docs/#/Log78/).