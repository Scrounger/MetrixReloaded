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
                myVersion.IncreaseMinor();
                Console.WriteLine(String.Format("(2) Increase version to {0}", myVersion.Get()));
                Console.WriteLine("---------------------------------------------------------------------------------------------------");
                Console.Write("-> ");

                ConsoleKey response = Console.ReadKey(false).Key;

                switch (response)
                {
                    case ConsoleKey.D1:
                        myVersion.Load();
                        break;
                    case ConsoleKey.D2:
                        myVersion.Save();
                        break;
                }

                Console.WriteLine();
                Console.WriteLine();

                Console.WriteLine(String.Format("Building version: {0}....", myVersion.Get()));
                Console.WriteLine();

                ScreenMerger.Run(false, false, false);

                string libPath = settings.BuildPath + libPathPrefix;
                string skinPath = settings.BuildPath + skinPathPrefix;

                ClearFolder(libPath);
                ClearFolder(skinPath);

                CopyAll(settings.LibPath, libPath);
                CopyAll(settings.SkinPath, skinPath);

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

        public static void CopyAll(string SourcePath, string DestinationPath)
        {
            Console.WriteLine();
            Console.WriteLine(String.Format("copy files from: {0}", SourcePath));
            Console.WriteLine("---------------------------------------------------------------------------------------------------");
            //Now Create all of the directories
            int i = 1;

            string[] dirList = Directory.GetDirectories(SourcePath, "*", SearchOption.AllDirectories);

            foreach (string dirPath in dirList)
            {
                Directory.CreateDirectory(Path.Combine(DestinationPath, dirPath.Remove(0, SourcePath.Length)));

                ProgressBar.Draw("create directories...", i, dirList.Length);
                i++;
            }
            Console.WriteLine();
            i = 1;
            dirList = Directory.GetFiles(SourcePath, "*.*", SearchOption.AllDirectories);

            //Copy all the files & Replaces any files with the same name
            foreach (string newPath in Directory.GetFiles(SourcePath, "*.*", SearchOption.AllDirectories))
            {
                File.Copy(newPath, Path.Combine(DestinationPath, newPath.Remove(0, SourcePath.Length)), true);
                ProgressBar.Draw("copy files...", i, dirList.Length);
                i++;
            }

            Console.WriteLine();
        }
    }
}
