using System;
using System.Collections.Generic;
using System.Configuration;
using System.IO;
using System.Text;

namespace DLISDeployment
{
    public class Logger
    {
        private static readonly Lazy<Logger> logger = new Lazy<Logger>(() => new Logger());
        public static Logger Instance { get { return logger.Value; } }

        private Logger()
        {
            string logFile = ConfigurationManager.AppSettings["logFile"];

            if (!Directory.Exists(Path.GetDirectoryName(logFile)))
            {
                Directory.CreateDirectory(Path.GetDirectoryName(logFile));
            }
            var sw = File.AppendText(logFile);

            TextWriter tw = TextWriter.Synchronized(sw);
            logListeners.Add(tw);
        }

        /// <summary>
        /// Defeines the severity for logging messages.
        /// </summary>
        public enum Severity { INFO, WARNING, ERROR, FATAL };

        public void WriteLine(string s, params object[] args)
        {
            WriteLine(Severity.INFO, true, s, args);
        }

        public void Info(string s, params object[] args)
        {
            WriteLine(Severity.INFO, true, s, args);
        }
        public void Error(string s, params object[] args)
        {
            WriteLine(Severity.ERROR, true, s, args);
        }

        public void Warning(string s, params object[] args)
        {
            WriteLine(Severity.WARNING, true, s, args);
        }

        public void WriteLine(Severity severity,
                                     bool header,
                                     string s, params object[] args)
        {
            StringBuilder sb = new StringBuilder();
            DateTime now = DateTime.Now;
            if (header)
            {
                sb.AppendFormat("[{0:D4}/{1:D2}/{2:D2} {3:D2}:{4:D2}:{5:D2}][{6}] ",
                    now.Year,
                    now.Month,
                    now.Day,
                    now.Hour,
                    now.Minute,
                    now.Second,
                    severity.ToString());
            }

            foreach (var stream in logListeners)
            {
                sb.AppendFormat(s, args);
                string traceLine = sb.ToString();
                stream.WriteLine(traceLine);
                stream.Flush();
            }
        }

        private static List<TextWriter> logListeners = new List<TextWriter>();
    }
}
