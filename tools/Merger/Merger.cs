using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using Tools;


namespace Merger
{
    class Merger
    {
        static void Main(string[] args)
        {
            try
            {
                Settings settings = Settings.Load();
                settings.LogSettings();

                string skinFileName = settings.SkinPath + "skin.xml";
                string skinProductionFileName = settings.VuPlusSkinPath + "skin.xml";

                System.IO.DirectoryInfo directory = new System.IO.DirectoryInfo(settings.ScreenFilesPath);

                String skinFileString = "<skin>";

                foreach (System.IO.FileInfo file in directory.GetFiles())
                {
                    if (file.Name.Contains(".xml") & !file.Name.Equals("skin.xml"))
                    {
                        Console.Write(String.Format("Reading {0}\n", file.Name));

                        String fileString = File.ReadAllText(file.FullName);
                        skinFileString = String.Format("{0}\n{1}", skinFileString, File.ReadAllText(file.FullName));
                    }
                }
                Console.Write("\n-------------------------------------------------------------\n");
                Console.Write(String.Format("Merging xml files in {0}\n", skinFileName));

                skinFileString = String.Format("{0}\n</skin>", skinFileString, FileMode.Create);

                File.WriteAllText(skinFileName, skinFileString);

                MyVersion myVersion = new MyVersion();
                myVersion.IncreaseBuild();
                myVersion.Save();
                myVersion.Load();
                Console.WriteLine(String.Format("Version: {0}", myVersion.Get()));

                if (Directory.Exists(settings.VuPlusSkinPath))
                {
                    File.Copy(skinFileName, skinProductionFileName, true);
                    File.Copy(myVersion.FullFileName, settings.VuPlusSkinPath + myVersion.FileName, true);
                    Thread.Sleep(2000);
                }
                else
                {
                    Console.WriteLine();
                    Console.WriteLine();
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine(String.Format("path not exist: {0}", settings.VuPlusSkinPath));
                    Console.WriteLine();
                    Console.Write("Press any key to exit");
                    Console.ReadKey();
                }
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
    }
}
