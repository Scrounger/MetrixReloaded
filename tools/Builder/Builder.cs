using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Helper;

namespace Builder
{
    class Builder
    {
        private const string libPathPrefix = "usr/lib/enigma2/python";
        private const string skinPathPrefix = "usr/share/enigma2/MetrixReloaded";

        static void Main(string[] args)
        {
            try
            {
                Settings settings = Settings.Load();
                settings.LogSettings();

                MyVersion myVersion = new MyVersion();

                Console.WriteLine("(1) Do nothing, stay at version {0}", myVersion.Get());
                myVersion.IncreaseBuild();
                Console.WriteLine(String.Format("(2) Increase build version to {0}", myVersion.Get()));
                myVersion.IncreaseMinor();
                Console.WriteLine(String.Format("(3) Increase minor version to {0}", myVersion.Get()));
                myVersion.IncreaseMajor();
                Console.WriteLine(String.Format("(4) Increase major version to {0}", myVersion.Get()));

                Console.WriteLine("---------------------------------------------------------------------------------------------------");
                Console.Write("-> ");

                ConsoleKey response = Console.ReadKey(false).Key;

                switch (response)
                {
                    case ConsoleKey.D1:
                        myVersion.Load();
                        break;
                    case ConsoleKey.D2:
                        myVersion.Load();
                        myVersion.IncreaseBuild();
                        myVersion.Save();
                        break;
                    case ConsoleKey.D3:
                        myVersion.Load();
                        myVersion.IncreaseMinor();
                        myVersion.Save();
                        break;
                    case ConsoleKey.D4:
                        myVersion.Load();
                        myVersion.IncreaseMajor();
                        myVersion.Save();
                        break;
                }

                Console.WriteLine();
                Console.WriteLine();

                Console.WriteLine(String.Format("Building version: {0}....", myVersion.Get()));
                Console.WriteLine();

                if (settings.IsSkin)
                {
                    ScreenMerger.Run(false, false, false);
                }
                

                string libPath = settings.BuildPath + libPathPrefix;
                string skinPath = settings.BuildPath + skinPathPrefix;

                ClearFolder(libPath);

                if (settings.IsSkin)
                {
                    ClearFolder(skinPath);
                }

                Functions.CopyAll(settings.LibPath, libPath, true);

                if (settings.IsSkin)
                {
                    Functions.CopyAll(settings.SkinPath, skinPath, true);
                }

                Console.WriteLine();

                IpkControlFile ipkControlFile = new IpkControlFile(settings.BuildPath, myVersion.Get());
                ipkControlFile.Generate();
                Console.WriteLine("Ipk control file created");

                //myVersion.Save(settings.ProjectPath + "version.released");

                Console.WriteLine();
                Console.WriteLine("successful finished!");

                Thread.Sleep(5000);
            }
            catch (Exception ex)
            {
                Console.WriteLine();
                Console.WriteLine();
                Console.ForegroundColor = ConsoleColor.Red;
                Console.Write("Error: {0}\n", ex.Message);
                Console.Write("Error: {0}\n", ex.StackTrace);
                Console.WriteLine();
                Console.Write("Press any key to exit");
                Console.ReadKey();
            }
        }

        private static void ClearFolder(string folder)
        {
            if (Directory.Exists(folder))
            {
                Directory.Delete(folder, true);
            }

            Directory.CreateDirectory(folder);
        }

        internal class Control
        {
        }
    }
}
