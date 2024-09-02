#nullable enable
using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Text;

namespace www778878net.log
{
    /// <summary>
    /// 根据LOG等级确认哪些打印 哪些写文件 哪些写入服务器
    /// </summary>
    public class Log78
    {     
      
        /// <summary>
        /// 类别等于其中之一 既打印本地 又打印服务器
        /// </summary>
        public string[] debugKind = new string[0];
        public int LevelFile { get; set; } = 50;
        public int LevelConsole { get; set; } = 30;
        public int LevelApi { get; set; } = 70;
        private IServerLog78? serverLogger;
        private IConsoleLog78? consoleLogger=new ConsoleLog78();
        private IFileLog78? fileLogger;


        public string uname{get;set;}="";//默认key3是用户名

        // 公共的静态方法，用于获取单例实例
        private static  Log78? instance ;
        public static Log78 Instance
        {
            get
            {
                if(instance==null){
                    instance = new Log78();
                    instance.setup(null,new FileLog78(),new ConsoleLog78(),"guest");
                  }
                    
                     
                     
                return instance;
            }
        }
        


        public void setup(IServerLog78? serverLogger, IFileLog78? fileLogger, IConsoleLog78? consoleLogger, string _uname = "guest")
        {
            this.serverLogger = serverLogger;
            this.consoleLogger = consoleLogger;
            this.fileLogger = fileLogger;
            this.uname = _uname;
        }

        public Log78 Clone(){
            return new Log78(){
                serverLogger=this.serverLogger,
                fileLogger=this.fileLogger,
                consoleLogger=this.consoleLogger,
                uname=this.uname,               
                LevelApi=this.LevelApi,
                LevelConsole=this.LevelConsole,
                LevelFile=this.LevelFile             

            };
        }

        public void LogErr(Exception exception, string key1= "errwinpro", [CallerMemberName] string previousMethodName = "")
        {
            Log(exception.Message, 90, key1, previousMethodName, uname, exception.StackTrace);
        }

        public void Log(string message, int level = 50,  [CallerMemberName] string key1 = "", string key2 = "", string key3 = "", string content = "", string key4 = "", string key5 = "", string key6 = "")
        {
            if (string.IsNullOrEmpty(key1))
                key1 = "";
            if (string.IsNullOrEmpty(key2))
                key2 = "";
            if (string.IsNullOrEmpty(key3))
                key3 = uname;
            bool isdebug = false;
            string tmpkind;
            //是否debugkey
            for (int i = 0; i < 6; i++)
            {
                switch (i)
                {
                    case 0: tmpkind = key1; break;
                    case 1: tmpkind = key2; break;
                    case 2: tmpkind = key3; break;
                    case 3: tmpkind = key4; break;
                    case 4: tmpkind = key5; break;
                    default: tmpkind = key6; break;
                }
                for (int j = 0; j < debugKind.Length; j++)
                {
                    if (tmpkind == debugKind[j])
                    {
                        isdebug = true;
                        break;
                    }
                }
                if (isdebug) break;
            }

            if (isdebug || level >= LevelApi)            
                serverLogger?.LogToServer(message, key1, level, key2, key3, content, key4, key5, key6);
            
            string info = DateTime.Now.ToString() + "\t" + message + "~~" + content + "~~" + key1;
            if (isdebug || level >= LevelFile)            
                fileLogger?.LogToFile(info);
            

            if (isdebug || level >= LevelConsole)            
                consoleLogger?.WriteLine(info);
            
        }

        
    }
}
