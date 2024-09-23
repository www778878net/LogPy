#nullable enable
using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Text;
using System.Reflection;
using System.Threading.Tasks;
using System.Threading;
using System.Linq;

namespace www778878net.log
{
  public class Log78:ILog78
  {
    private HashSet<string> debugKind = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
    private int LevelFile { get; set; } = 30;
    private int LevelConsole { get; set; } = 60;
    private int LevelApi { get; set; } = 50;
    private IServerLog78? serverLogger;
    private IConsoleLog78? consoleLogger = new ConsoleLog78();
    private IFileLog78? fileLogger = new FileLog78();
    private IFileLog78? debugFileLogger;

    public LogEntry? DebugEntry { get; set; }
    public Environment CurrentEnvironment { get; private set; } = Environment.Production;

    private static Log78? instance;
    public static Log78 Instance
    {
      get
      {
        if (instance == null)
        {
          instance = new Log78();
          instance.Setup(null, new FileLog78(), new ConsoleLog78());
        }
        return instance;
      }
    }

    public Log78()
    {
      SetEnvironmentFromEnvVar();
    }

    // 添加一个新的构造函数，用于依赖注入
    public Log78(IServerLog78? serverLogger, IFileLog78? fileLogger, IConsoleLog78? consoleLogger)
    {
        SetEnvironmentFromEnvVar();
        Setup(serverLogger, fileLogger, consoleLogger);
    }

    private void SetEnvironmentFromEnvVar()
    {
      string? envVar = System.Environment.GetEnvironmentVariable("LOG78_ENVIRONMENT");
      if (Enum.TryParse(envVar, true, out Environment env))
      {
        SetEnvironment(env);
      }
      else
      {
        SetEnvironment(Environment.Production);
      }
    }

    public void SetEnvironment(Environment env)
    {
      CurrentEnvironment = env;
      UpdateLogLevels();
      SetupDebugFileLogger();
    }

    private void UpdateLogLevels()
    {
      switch (CurrentEnvironment)
      {
        case Environment.Production:
          LevelConsole = 60; // ERROR
          LevelFile = 30;    // INFO
          LevelApi = 30;     // INFO
          break;
        case Environment.Development:
          LevelConsole = 20; // DEBUG
          LevelFile = 20;    // DEBUG
          LevelApi = 30;     // INFO
          break;
        case Environment.Testing:
          LevelConsole = 60; // ERROR
          LevelFile = 20;    // DEBUG
          LevelApi = 30;     // INFO
          break;
      }
    }

    private void SetupDebugFileLogger()
    {
      if (CurrentEnvironment == Environment.Development)
      {
        debugFileLogger = new FileLogDetail();
      }
      else
      {
        debugFileLogger = null;
      }
    }

    public void Setup(IServerLog78? serverLogger, IFileLog78? fileLogger, IConsoleLog78? consoleLogger)
    {
      this.serverLogger = serverLogger;
      this.fileLogger = fileLogger ?? this.fileLogger;
      this.consoleLogger = consoleLogger ?? this.consoleLogger;
    }

    public void SetupDetailFile()
    {
      debugFileLogger = new FileLogDetail();
    }

    public void ClearDetailLog()
    {
      debugFileLogger?.Clear();
    }

    private Dictionary<string, object> customProperties = new Dictionary<string, object>();

    public void AddProperty(string key, object value)
    {
      customProperties[key] = value;
    }

    private readonly object _lock = new object();
    private readonly SemaphoreSlim _semaphore = new SemaphoreSlim(1, 1);

    private async Task ProcessLogInternal(LogEntry? logEntry)
    {
      await _semaphore.WaitAsync();
      try
      {
        if (logEntry?.Basic == null)
        {
          await ERROR(new LogEntry { Basic = new BasicInfo { Message = "Error: LogEntry or LogEntry.Basic is null" } });
          return;
        }

        lock (_lock)
        {
          // 添加自定义属性到日志条目
          foreach (var prop in customProperties)
          {
            logEntry.AddProperty(prop.Key, prop.Value);
          }
        }

        // 始终写入详细日志，不管当前环境
        debugFileLogger?.LogToFile(logEntry);

        bool isdebug = IsDebugKey(logEntry);

        if (isdebug || logEntry.Basic.LogLevelNumber >= LevelApi)
        {
          if (serverLogger != null)
          {
            try
            {
              await serverLogger.LogToServer(logEntry);
            }
            catch (Exception ex)
            {
              Console.WriteLine($"Error in server logging: {ex.Message}");
            }
          }
        }

        if (isdebug || logEntry.Basic.LogLevelNumber >= LevelFile)
        {
          fileLogger?.LogToFile(logEntry);
        }

        if (isdebug || logEntry.Basic.LogLevelNumber >= LevelConsole)
        {
          consoleLogger?.WriteLine(logEntry);
        }
      }
      finally
      {
        _semaphore.Release();
      }
    }

    private bool IsDebugKey(LogEntry logEntry)
    {
      if (DebugEntry?.Basic != null)
      {
        return (DebugEntry.Basic.ServiceName != null &&
                logEntry.Basic.ServiceName != null &&
                DebugEntry.Basic.ServiceName.Equals(logEntry.Basic.ServiceName, StringComparison.OrdinalIgnoreCase)) ||
               (DebugEntry.Basic.ServiceObj != null &&
                logEntry.Basic.ServiceObj != null &&
                DebugEntry.Basic.ServiceObj.Equals(logEntry.Basic.ServiceObj, StringComparison.OrdinalIgnoreCase)) ||
               (DebugEntry.Basic.ServiceFun != null &&
                logEntry.Basic.ServiceFun != null &&
                DebugEntry.Basic.ServiceFun.Equals(logEntry.Basic.ServiceFun, StringComparison.OrdinalIgnoreCase)) ||
               (DebugEntry.Basic.UserId != null &&
                logEntry.Basic.UserId != null &&
                DebugEntry.Basic.UserId.Equals(logEntry.Basic.UserId, StringComparison.OrdinalIgnoreCase)) ||
               (DebugEntry.Basic.UserName != null &&
                logEntry.Basic.UserName != null &&
                DebugEntry.Basic.UserName.Equals(logEntry.Basic.UserName, StringComparison.OrdinalIgnoreCase));
      }

      string?[] keysToCheck = new[]
      {
        logEntry.Basic.ServiceName,
        logEntry.Basic.ServiceObj,
        logEntry.Basic.ServiceFun,
        logEntry.Basic.UserId,
        logEntry.Basic.UserName
      };

      return keysToCheck.Any(key => key != null && debugKind.Contains(key.ToLower()));
    }

    public async Task DETAIL(string summary, object? message = null, int level = 10)
    {
      await DETAIL(new LogEntry { Basic = new BasicInfo { Summary = summary, Message = message, LogLevelNumber = level } });
    }

    public async Task DEBUG(string summary, object? message = null, int level = 20)
    {
      await DEBUG(new LogEntry { Basic = new BasicInfo { Summary = summary, Message = message, LogLevelNumber = level } });
    }

    public async Task INFO(string summary, object? message = null, int level = 30)
    {
      await INFO(new LogEntry { Basic = new BasicInfo { Summary = summary, Message = message, LogLevelNumber = level } });
    }

    public async Task WARN(string summary, object? message = null, int level = 50)
    {
      await WARN(new LogEntry { Basic = new BasicInfo { Summary = summary, Message = message, LogLevelNumber = level } });
    }

    public async Task ERROR(string summary, object? message = null, int level = 60)
    {
      await ERROR(new LogEntry { Basic = new BasicInfo { Summary = summary, Message = message, LogLevelNumber = level } });
    }

    public async Task ERROR(Exception error, string? summary = null, int level = 60)
    {
      var logEntry = new LogEntry 
      { 
        Basic = new BasicInfo { Summary = summary ?? error.Message, LogLevelNumber = level },
        Error = new ErrorInfo 
        { 
          ErrorType = error.GetType().FullName,
          ErrorMessage = error.Message,
          ErrorStackTrace = error.StackTrace
        }
      };
      await ERROR(logEntry);
    }

    public async Task ERROR(Exception error, LogEntry logEntry, int level = 60)
    {
      logEntry.Basic.LogLevel = "ERROR";
      logEntry.Basic.LogLevelNumber = level;

      logEntry.Error.ErrorType = error.GetType().FullName;
      logEntry.Error.ErrorMessage = error.Message;
      logEntry.Error.ErrorStackTrace = error.StackTrace;

      if (string.IsNullOrEmpty(logEntry.Basic.Summary))
      {
        logEntry.Basic.Summary = error.Message;
      }

      if (logEntry.Basic.Message == null)
      {
        logEntry.Basic.Message = $"{error.GetType().Name}: {error.Message}";
      }
      else if (logEntry.Basic.Message is string messageString && string.IsNullOrEmpty(messageString))
      {
        logEntry.Basic.Message = $"{error.GetType().Name}: {error.Message}";
      }

      await ProcessLogInternal(logEntry);
    }

    public async Task DETAIL(LogEntry logEntry, int level = 10)
    {
      logEntry.Basic.LogLevel = "DETAIL";
      logEntry.Basic.LogLevelNumber = level;
      await ProcessLogInternal(logEntry);
    }

    public async Task DEBUG(LogEntry logEntry, int level = 20)
    {
      logEntry.Basic.LogLevel = "DEBUG";
      logEntry.Basic.LogLevelNumber = level;
      await ProcessLogInternal(logEntry);
    }

    public async Task INFO(LogEntry logEntry, int level = 30)
    {
      logEntry.Basic.LogLevel = "INFO";
      logEntry.Basic.LogLevelNumber = level;
      await ProcessLogInternal(logEntry);
    }

    public async Task WARN(LogEntry logEntry, int level = 50)
    {
      logEntry.Basic.LogLevel = "WARN";
      logEntry.Basic.LogLevelNumber = level;
      await ProcessLogInternal(logEntry);
    }

    public async Task ERROR(LogEntry logEntry, int level = 60)
    {
      logEntry.Basic.LogLevel = "ERROR";
      logEntry.Basic.LogLevelNumber = level;
      await ProcessLogInternal(logEntry);
    }

    public void SetupLevel(int fileLevel, int consoleLevel, int apiLevel)
    {
      LevelFile = fileLevel;
      LevelConsole = consoleLevel;
      LevelApi = apiLevel;
    }

    public (int FileLevel, int ConsoleLevel, int ApiLevel) GetCurrentLevels()
    {
      return (LevelFile, LevelConsole, LevelApi);
    }

    public Log78 Clone()
    {
        var cloned = new Log78();
        cloned.serverLogger = this.serverLogger;
        cloned.fileLogger = this.fileLogger;
        cloned.consoleLogger = this.consoleLogger;
        cloned.LevelApi = this.LevelApi;
        cloned.LevelConsole = this.LevelConsole;
        cloned.LevelFile = this.LevelFile;
        cloned.CurrentEnvironment = this.CurrentEnvironment;
    
        return cloned;
    }

    public enum Environment
    {
      Production,
      Development,
      Testing
    }

    public void AddDebugKey(string key)
    {
      lock (_lock)
      {
        debugKind.Add(key.ToLower());
      }
    }
  }
}