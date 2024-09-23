using System;
using System.Threading.Tasks;
using www778878net.log;

namespace www778878net.log
{
  public interface ILog78
  {
    Task DETAIL(string summary, object? message = null, int level = 10);
    Task DEBUG(string summary, object? message = null, int level = 20);
    Task INFO(string summary, object? message = null, int level = 30);
    Task WARN(string summary, object? message = null, int level = 50);
    Task ERROR(string summary, object? message = null, int level = 60);
    Task ERROR(Exception error, string? summary = null, int level = 60);
    Task ERROR(LogEntry logEntry, int level = 60);
    Task DEBUG(LogEntry logEntry, int level = 20);
    Task INFO(LogEntry logEntry, int level = 30);
    Task WARN(LogEntry logEntry, int level = 50);    
    void Setup(IServerLog78? serverLogger, IFileLog78? fileLogger, IConsoleLog78? consoleLogger);
    void SetEnvironment(Log78.Environment env);
    void SetupLevel(int fileLevel, int consoleLevel, int apiLevel);
    void AddDebugKey(string key);
    void ClearDetailLog();
    void SetupDetailFile();
  }
}