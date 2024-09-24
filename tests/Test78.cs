// Copyright 2024 frieda
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

using Microsoft.VisualStudio.TestTools.UnitTesting;
using www778878net.log;
using System;
using System.Net.Http;
using System.Threading.Tasks;
using System.IO;
using Newtonsoft.Json.Linq;
using System.Linq;
using Newtonsoft.Json;

namespace Test78
{
    [TestClass]
    public class Log78Tests
    {
        private static Log78? logger;

        [ClassInitialize]
        public static void ClassInitialize(TestContext context)
        {
            logger = Log78.Instance;
            logger.SetupDetailFile();
            logger.ClearDetailLog();
        }

        [TestMethod]
        public async Task TestEnvironmentSettings()
        {
            logger?.SetEnvironment(Log78.Environment.Development);
            // ... (其余测试代码)
            await Task.CompletedTask;
        }

        [TestMethod]
        public async Task TestLogLevels()
        {
            var logEntry = new LogEntry
            {
                Basic = new BasicInfo
                {
                    Message = "Debug message",
                    LogLevel = "DEBUG",
                    LogLevelNumber = 20
                }
            };
            await logger!.DEBUG(logEntry);
            // ... (其余测试代码)
        }

        [TestMethod]
        public async Task TestCustomLogEntry()
        {
            var customEntry = new LogEntry
            {
                Basic = new BasicInfo
                {
                    Message = "Custom log entry",
                    LogLevel = "INFO",
                    LogLevelNumber = 30
                }
                // ... (设置其他 LogEntry 属性)
            };

            await logger!.INFO(customEntry);
            // ... (其余测试代码)
        }

        [TestMethod]
        public async Task TestLogstashServerLog78()
        {
            var serverLog = new LogstashServerLog78("http://example.com", 50);
            // ... (其余测试代码)
            await Task.CompletedTask;
        }

        [TestMethod]
        public async Task TestClone()
        {
            var originalLogger = Log78.Instance;
            originalLogger.SetEnvironment(Log78.Environment.Development);

            var clonedLogger = originalLogger.Clone();

            // 验证两个logger的设置是相同的
            Assert.AreEqual(originalLogger.CurrentEnvironment, clonedLogger.CurrentEnvironment);
            Assert.AreEqual(originalLogger.GetCurrentLevels(), clonedLogger.GetCurrentLevels());

            // 验证更改原始logger的设置不会影响克隆的logger
            originalLogger.SetEnvironment(Log78.Environment.Production);
            Assert.AreNotEqual(originalLogger.CurrentEnvironment, clonedLogger.CurrentEnvironment);

            await Task.CompletedTask;
        }

        [TestMethod]
        public async Task TestDetailLogAlwaysWritten()
        {
            var logger = Log78.Instance;
            logger.SetEnvironment(Log78.Environment.Production);
            logger.SetupDetailFile();

            var logEntry = new LogEntry
            {
                Basic = new BasicInfo
                {
                    Message = "Test detail log",
                    LogLevel = "INFO",
                    LogLevelNumber = 30
                }
            };

            await logger.INFO(logEntry);

            // 验证详细日志文件存在并包含日志条目
            string logPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "logs", "detail.log");
            Assert.IsTrue(File.Exists(logPath), "Detail log file should exist");
            string logContent = File.ReadAllText(logPath);
            Console.WriteLine($"Log content: {logContent}"); // 添加这行来输出日志内容
            Assert.IsTrue(logContent.Contains("Test detail log"), "Detail log should contain the log message");
        }

        [TestMethod]
        public async Task TestLogMethodOverloads()
        {
            var logger = Log78.Instance;
            logger.SetEnvironment(Log78.Environment.Development);
            logger.SetupDetailFile();

            await logger.DETAIL("Detail summary", new { DetailInfo = "Some detail info" });
            await logger.DEBUG("Debug summary", new { DebugInfo = "Some debug info" });
            await logger.INFO("Info summary", new { InfoData = "Some info data" });
            await logger.WARN("Warn summary", new { WarnCode = 123 });
            await logger.ERROR("Error summary", new { ErrorCode = 500 });

            try
            {
                throw new Exception("Test exception");
            }
            catch (Exception ex)
            {
                await logger.ERROR(ex, "Custom error summary");
            }

            // 验证详细日志文件存在并包含所有日志消息
            string logPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "logs", "detail.log");
            Assert.IsTrue(File.Exists(logPath), "Detail log file should exist");
            string logContent = File.ReadAllText(logPath);
            Console.WriteLine($"Log content: {logContent}");
            Assert.IsTrue(logContent.Contains("Detail summary"), "Log should contain Detail summary");
            Assert.IsTrue(logContent.Contains("Some detail info"), "Log should contain detail info");
            Assert.IsTrue(logContent.Contains("Debug summary"), "Log should contain Debug summary");
            Assert.IsTrue(logContent.Contains("Some debug info"), "Log should contain debug info");
            Assert.IsTrue(logContent.Contains("Info summary"), "Log should contain Info summary");
            Assert.IsTrue(logContent.Contains("Some info data"), "Log should contain info data");
            Assert.IsTrue(logContent.Contains("Warn summary"), "Log should contain Warn summary");
            Assert.IsTrue(logContent.Contains("123"), "Log should contain warn code");
            Assert.IsTrue(logContent.Contains("Error summary"), "Log should contain Error summary");
            Assert.IsTrue(logContent.Contains("500"), "Log should contain error code");
            Assert.IsTrue(logContent.Contains("Custom error summary"), "Log should contain custom error summary");
            Assert.IsTrue(logContent.Contains("Test exception"), "Log should contain exception message");
        }

        [TestMethod]
        public async Task TestMessageSerialization()
        {
            var logger = Log78.Instance;
            logger.SetEnvironment(Log78.Environment.Development);
            logger.SetupDetailFile();

            // 测试字符串消息
            await logger.INFO("String message test", "This is a string message");

            // 测试对象消息
            await logger.INFO("Object message test", new { Key = "Value", Number = 123 });

            // 验证详细日志文件存在并包含所有日志消息
            string logPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "logs", "detail.log");
            Assert.IsTrue(File.Exists(logPath), "Detail log file should exist");
            string logContent = File.ReadAllText(logPath);
            Console.WriteLine($"Log content: {logContent}");
            
            // 解析日志内容
            var logEntries = logContent.Split(new[] { "<AI_FOCUS_LOG>", "</AI_FOCUS_LOG>" }, StringSplitOptions.RemoveEmptyEntries)
                                       .Where(json => !string.IsNullOrWhiteSpace(json))
                                       .Select(json => JObject.Parse(json))
                                       .ToList();

            Assert.IsTrue(logEntries.Count > 0, "At least one log entry should be parsed");

            // 验证字符串消息
            var stringMessageEntry = logEntries.FirstOrDefault(e => e["summary"]?.ToString() == "String message test");
            Assert.IsNotNull(stringMessageEntry, "String message entry should exist");
            Assert.AreEqual("This is a string message", stringMessageEntry["message"]?.ToString(), "String message should be correct");

            // 验证对象消息
            var objectMessageEntry = logEntries.FirstOrDefault(e => e["summary"]?.ToString() == "Object message test");
            Assert.IsNotNull(objectMessageEntry, "Object message entry should exist");
            Assert.IsTrue(objectMessageEntry["message"] is JObject, "Object message should be a JSON object");
            var messageObject = objectMessageEntry["message"] as JObject;
            Assert.IsNotNull(messageObject, "Message object should not be null");
            Assert.AreEqual("Value", messageObject["Key"]?.ToString(), "Object message should contain correct key");
            Assert.AreEqual("123", messageObject["Number"]?.ToString(), "Object message should contain correct number");
        }

        [TestMethod]
        public async Task TestDynamicLogLevelAdjustment()
        {
            var logger = Log78.Instance;
            logger.SetEnvironment(Log78.Environment.Development);
            logger.SetupDetailFile();

            // 设置自定义日志级别
            logger.SetupLevel(40, 50, 60);

            // 测试不同级别的日志
            await logger.DETAIL("Detail message", new { Level = "DETAIL" });
            await logger.DEBUG("Debug message", new { Level = "DEBUG" });
            await logger.INFO("Info message", new { Level = "INFO" });
            await logger.WARN("Warn message", new { Level = "WARN" });
            await logger.ERROR("Error message", new { Level = "ERROR" });

            // 验证详细日志文件存在并包含所有日志消息
            string logPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "logs", "detail.log");
            Assert.IsTrue(File.Exists(logPath), "Detail log file should exist");
            string logContent = File.ReadAllText(logPath);
            Console.WriteLine($"Log content: {logContent}");

            // 验证日志级别设置是否生效
            Assert.IsTrue(logContent.Contains("Detail message"), "Log should contain Detail message");
            Assert.IsTrue(logContent.Contains("Debug message"), "Log should contain Debug message");
            Assert.IsTrue(logContent.Contains("Info message"), "Log should contain Info message");
            Assert.IsTrue(logContent.Contains("Warn message"), "Log should contain Warn message");
            Assert.IsTrue(logContent.Contains("Error message"), "Log should contain Error message");

            // 验证日志级别
            var (fileLevel, consoleLevel, apiLevel) = logger.GetCurrentLevels();
            Assert.AreEqual(40, fileLevel, "File log level should be 40");
            Assert.AreEqual(50, consoleLevel, "Console log level should be 50");
            Assert.AreEqual(60, apiLevel, "API log level should be 60");
        }

        [TestMethod]
        public async Task TestDebugEntry()
        {
            var logger = Log78.Instance;
            logger.SetEnvironment(Log78.Environment.Development);
            logger.SetupDetailFile();

            // 设置调试条件
            logger.DebugEntry = new LogEntry
            {
                Basic = new BasicInfo { UserName = "guest" }
            };

            // 记录一条不满足调试条件的日志
            await logger.INFO("Normal log", new { UserName = "admin" });

            // 记录一条满足调试条件的日志
            await logger.INFO("Debug log", new { UserName = "guest" });

            // 验证详细日志文件存在并包含所有日志消息
            string logPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "logs", "detail.log");
            Assert.IsTrue(File.Exists(logPath), "Detail log file should exist");
            string logContent = File.ReadAllText(logPath);
            Console.WriteLine($"Log content: {logContent}");

            // 解析日志内容
            var logEntries = logContent.Split(new[] { "<AI_FOCUS_LOG>", "</AI_FOCUS_LOG>" }, StringSplitOptions.RemoveEmptyEntries)
                                       .Where(json => !string.IsNullOrWhiteSpace(json))
                                       .Select(json => JObject.Parse(json))
                                       .ToList();

            Assert.IsTrue(logEntries.Count > 0, "At least one log entry should be parsed");

            // 验证调试日志
            var debugLogEntry = logEntries.FirstOrDefault(e => e["summary"]?.ToString() == "Debug log");
            Assert.IsNotNull(debugLogEntry, "Debug log entry should exist");
            Assert.AreEqual("guest", debugLogEntry["message"]?["UserName"]?.ToString(), "Debug log should contain correct username");

            // 验证普通日志是否被记录（取决于当前的日志级别设置）
            var normalLogEntry = logEntries.FirstOrDefault(e => e["summary"]?.ToString() == "Normal log");
            if (logger.GetCurrentLevels().FileLevel <= 30) // INFO level
            {
                Assert.IsNotNull(normalLogEntry, "Normal log entry should exist if file log level is INFO or lower");
            }
            else
            {
                Assert.IsNull(normalLogEntry, "Normal log entry should not exist if file log level is higher than INFO");
            }
        }

        [TestMethod]
        public async Task TestDebugKind()
        {
            var logger = Log78.Instance;
            logger.SetEnvironment(Log78.Environment.Development);
            logger.SetupDetailFile();

            // 添加调试键
            logger.AddDebugKey("testuser");

            // 记录一条不满足调试条件的日志
            await logger.INFO("Normal log", new { UserName = "admin" });

            // 记录一条满足调试条件的日志
            await logger.INFO("Debug log", new { UserName = "testuser" });

            // 验证详细日志文件存在并包含所有日志消息
            string logPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "logs", "detail.log");
            Assert.IsTrue(File.Exists(logPath), "Detail log file should exist");
            string logContent = File.ReadAllText(logPath);
            Console.WriteLine($"Log content: {logContent}");

            // 解析日志内容
            var logEntries = logContent.Split(new[] { "<AI_FOCUS_LOG>", "</AI_FOCUS_LOG>" }, StringSplitOptions.RemoveEmptyEntries)
                                       .Where(json => !string.IsNullOrWhiteSpace(json))
                                       .Select(json => JObject.Parse(json))
                                       .ToList();

            Assert.IsTrue(logEntries.Count > 0, "At least one log entry should be parsed");

            // 验证调试日志
            var debugLogEntry = logEntries.FirstOrDefault(e => e["summary"]?.ToString() == "Debug log");
            Assert.IsNotNull(debugLogEntry, "Debug log entry should exist");
            Assert.AreEqual("testuser", debugLogEntry["message"]?["UserName"]?.ToString(), "Debug log should contain correct username");

            // 验证普通日志是否被记录（取决于当前的日志级别设置）
            var normalLogEntry = logEntries.FirstOrDefault(e => e["summary"]?.ToString() == "Normal log");
            if (logger.GetCurrentLevels().FileLevel <= 30) // INFO level
            {
                Assert.IsNotNull(normalLogEntry, "Normal log entry should exist if file log level is INFO or lower");
            }
            else
            {
                Assert.IsNull(normalLogEntry, "Normal log entry should not exist if file log level is higher than INFO");
            }
        }

        [TestMethod]
        public async Task TestCustomEntryLogging()
        {
            var logger = Log78.Instance;
            logger.SetEnvironment(Log78.Environment.Development);
            logger.SetupDetailFile();

            // 创建扩展的日志条目，包含空的 HttpInfo
            var extendedEntry = new customEntry
            {
                Basic = new BasicInfo
                {
                    Summary = "Custom log entry test",
                    Message = "This is a custom log entry",
                    LogLevel = "INFO",
                    LogLevelNumber = 30
                },
                CustomField1 = "Custom Value",
                CustomField2 = 42,
                Http = new HttpInfo() // 空的 HttpInfo
            };

            Console.WriteLine("Before logging custom entry");
            await logger.INFO(extendedEntry);
            Console.WriteLine("After logging custom entry");

            string logPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "logs", "detail.log");
            Assert.IsTrue(File.Exists(logPath), "Detail log file should exist");
            string logContent = File.ReadAllText(logPath);
            Console.WriteLine($"Log content: {logContent}");

            var logEntries = logContent.Split(new[] { "<AI_FOCUS_LOG>", "</AI_FOCUS_LOG>" }, StringSplitOptions.RemoveEmptyEntries)
                                       .Where(json => !string.IsNullOrWhiteSpace(json))
                                       .Select(json => JObject.Parse(json))
                                       .ToList();

            Assert.IsTrue(logEntries.Count > 0, "At least one log entry should be parsed");

            var customLogEntry = logEntries.LastOrDefault();
            Assert.IsNotNull(customLogEntry, "Custom log entry should exist");
            Console.WriteLine($"Parsed custom log entry: {customLogEntry}");
            Assert.AreEqual("Custom log entry test", customLogEntry?["summary"]?.ToString(), "Summary should be correct");
            Assert.AreEqual("This is a custom log entry", customLogEntry?["message"]?.ToString(), "Message should be correct");
            Assert.AreEqual("Custom Value", customLogEntry?["customfield1"]?.ToString(), "CustomField1 should be included");
            Assert.AreEqual(42, customLogEntry?["customfield2"]?.Value<int>(), "CustomField2 should be included");
            
            // 验证空的 HttpInfo 的属性不存在
            Assert.IsFalse(customLogEntry.ContainsKey("httprequestmethod"), "Empty HttpRequestMethod should not be included");
            Assert.IsFalse(customLogEntry.ContainsKey("httprequestbodycontent"), "Empty HttpRequestBodyContent should not be included");
            Assert.IsFalse(customLogEntry.ContainsKey("httpresponsestatuscode"), "Empty HttpResponseStatusCode should not be included");
            Assert.IsFalse(customLogEntry.ContainsKey("urloriginal"), "Empty UrlOriginal should not be included");
        }

        // ... (其他测试方法)
    }

    public class customEntry : LogEntry
    {
        public string CustomField1 { get; set; } = string.Empty;
        public int CustomField2 { get; set; }
    }
}