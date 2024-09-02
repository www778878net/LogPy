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
using System.IO;
using System.Xml.Serialization;



namespace www778878net.log
{
    public class FileLog78:IFileLog78
    {
        public string menu { get; set; }

        private string file;
        private static object olook = new object();
        public static string logpath{get;set;} = "/";

        public FileLog78(string _menu="") 
        { 
            this.menu = _menu;
            int idate = DateTime.Now.Day % 3;
            file = menu + idate.ToString() + ".txt";
            Clear();
        }
        public void LogToFile(string message)
        {
            lock (olook)
            {
                try
                {
                    File.AppendAllText( file, message);
                }
                catch { }
            }
        }

        /// <summary>
        /// 默认清除LOG只保留3天的
        /// </summary>
        public void Clear()
        {
            int idate = DateTime.Now.Day % 3;
            for (int i = 0; i < 3; i++)
            {
                if (i == idate) continue;
                File.Delete(menu + i.ToString() + ".txt");
            }

        }
    }
}