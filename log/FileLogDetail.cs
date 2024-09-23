using System;
using System.IO;
using Newtonsoft.Json;
using www778878net.log;

namespace www778878net.log
{
    public class FileLogDetail : IFileLog78
    {
        private string filePath;
        private static readonly object fileLock = new object();

        public FileLogDetail(string filename = "detail.log", string menu = "logs", bool clearOnCreate = true)
        {
            filePath = Path.Combine(menu, filename);
            Directory.CreateDirectory(menu);
            if (clearOnCreate)
            {
                Clear();
            }
        }

        public void LogToFile(LogEntry logEntry)
        {
            try
            {
                string logString = "<AI_FOCUS_LOG>" + logEntry.ToJson() + "</AI_FOCUS_LOG>\n";
                lock (fileLock)
                {
                    File.AppendAllText(filePath, logString);
                }
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"写入详细日志文件时出错: {ex}");
            }
        }

        public void Clear()
        {
            lock (fileLock)
            {
                File.WriteAllText(filePath, string.Empty);
            }
        }

        public void Close()
        {
            // 不需要特别的关闭操作
        }
    }
}