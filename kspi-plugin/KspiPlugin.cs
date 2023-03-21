using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Python.Runtime;
using UnityEngine;



namespace kspi_plugin
{
    [KSPAddon(KSPAddon.Startup.MainMenu, true)]
    public class KspiPlugin: MonoBehaviour
    {
        public void Awake()
        {
            var pathToPython = Path.GetFullPath(Path.Combine(Directory.GetCurrentDirectory(), @"KSP_x64_Data\python-3.11.2-embed-amd64\python311.dll"));
            Runtime.PythonDLL = pathToPython;

            Debug.Log("[KSPI]" + Runtime.PythonDLL);
            Debug.Log("[KSPI]" + PythonEngine.Platform);
            Debug.Log("[KSPI]" + PythonEngine.MinSupportedVersion);
            Debug.Log("[KSPI]" + PythonEngine.MaxSupportedVersion);
            Debug.Log("[KSPI]" + PythonEngine.BuildInfo);
            Debug.Log("[KSPI]" + PythonEngine.PythonPath);

            PythonEngine.Initialize();
            PythonEngine.BeginAllowThreads();

            using (Py.GIL())
            {
                dynamic server = Py.Import("kspi.rpc.server");

                server.Server.run();
            }
        }

        public void OnApplicationQuit()
        {
            dynamic server = Py.Import("kspi.rpc.server");

            server.Server.stop_and_join_server_thread();
        }
    }
}
