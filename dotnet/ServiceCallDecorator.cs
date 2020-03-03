using System.Collections.Generic;
using System.ServiceModel;
using System;
using System.ServiceModel.Channels;
using Newtonsoft.Json;

namespace Carina.ResourceCenter.Service
{
    public class ServiceCallDecorator:IDisposable
    {
        private string serviceCallName;
        private DateTime startTime;
        private DateTime endTime;
        private string IP;
        private Dictionary<string, object> loggedVariables = new Dictionary<string, object>();

        public ServiceCallDecorator(string serviceCallName)
        {
            this.serviceCallName = serviceCallName;
            startTime = DateTime.UtcNow;
            IP = ((RemoteEndpointMessageProperty)OperationContext.Current.IncomingMessageProperties[RemoteEndpointMessageProperty.Name]).Address;

            loggedVariables.Add("Call", serviceCallName);
            loggedVariables.Add("IP", IP);
        }

        public ServiceCallDecorator AddVaribale(string name, object obj)
        {
            loggedVariables[name] = obj;
            return this;
        }

        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }

        public void PrintLog()
        {
            endTime = DateTime.UtcNow;
            var ts = (int)((endTime - startTime).TotalMilliseconds);      
            loggedVariables.Add("Time", ts);
            Logger.Instance.Info("{0}", JsonConvert.SerializeObject(loggedVariables, Formatting.None));
        }

        bool disposed = false;
        protected virtual void Dispose(bool disposing)
        {
            if (disposed)
                return;

            if (disposing)
            {
                // Free any other managed objects here.
                PrintLog();
            }

            // Free any unmanaged objects here.
            disposed = true;
        }
    }
}
