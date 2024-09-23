using System;
using System.IO;
using System.Security.Cryptography;
using Serilog;
using Serilog.Core;

namespace www778878net.log
{
    public class FileLog78 : IFileLog78, IDisposable
    {
        private string menu ;
        private string filename;
        private Logger? _logger;

        public FileLog78(string _filename="7788_.log", string _menu = "logs")
        {
            menu = _menu;
            filename = _filename;
             string logFileName = Path.Combine(menu, filename);
                _logger = new LoggerConfiguration()
                .WriteTo.File(logFileName, rollingInterval: RollingInterval.Hour)
                .CreateLogger();            ConfigureLogger();
        }

        private void ConfigureLogger()
        {
            string logDirectory = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, menu);
            Directory.CreateDirectory(logDirectory);

   
        }

        public void LogToFile(LogEntry logEntry)
        {
            _logger?.Information(logEntry.ToJson());
        }

        public void Dispose()
        {
            _logger?.Dispose();
        }

    public void Clear()
    {
       
    }
  }
}