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

using System;
using Serilog;
using Serilog.Core;

namespace www778878net.log
{
    public class ConsoleLog78 : IConsoleLog78, IDisposable
    {
        private Logger _logger;

        public ConsoleLog78()
        {
             _logger = new LoggerConfiguration()
                .WriteTo.Console()
                .CreateLogger();
             
        }
 

        public void WriteLine(LogEntry logEntry)
        {
            _logger.Information(logEntry.ToJson());
        }

        public void Dispose()
        {
            _logger?.Dispose();
        }
    }
}