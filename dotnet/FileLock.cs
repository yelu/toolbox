using System;
using System.IO;
using System.Threading;

namespace Utils
{
    public class FileLock
    {
        FileStream lockFS;
        string filePath;
        public FileLock(string path)
        {
            filePath = path;
        }

        public bool Lock(int lockWaitMilliSeconds = 2000)
        {
            string lockFileDir = Path.GetDirectoryName(filePath);
            if (!Directory.Exists(lockFileDir)) { Directory.CreateDirectory(lockFileDir); }
            int waitTime = 100;
            int timeEslaped = 0;
            bool locked = false;
            do
            {
                try
                {
                    this.lockFS = new FileStream(filePath, FileMode.OpenOrCreate, FileAccess.ReadWrite, FileShare.None);
                    locked = true;
                    break;
                }
                catch (Exception e)
                {
                    string msg = e.Message;
                    Thread.Sleep(waitTime);
                    timeEslaped += waitTime;
                }
            } while (timeEslaped < lockWaitMilliSeconds);

            if (!locked)
            {
                return false;
            }
            return true;
        }

        public void Release()
        {
            if (lockFS != null)
            {
                lockFS.Close();
                lockFS = null;
            }
        }


    }

}
