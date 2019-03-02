﻿using Helper;
using System;
using System.IO;
using System.Threading;


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

                FileInfo[] fileList = directory.GetFiles();

                Console.WriteLine(String.Format("Merging xml files in {0}", skinFileName));
                Console.WriteLine("---------------------------------------------------------------------------------------------------");

                int i = 1;
                foreach (System.IO.FileInfo file in fileList)
                {
                    if (file.Name.Contains(".xml") & !file.Name.Equals("skin.xml"))
                    {
                        String fileString = File.ReadAllText(file.FullName);
                        skinFileString = String.Format("{0}\n{1}", skinFileString, File.ReadAllText(file.FullName));

                        ProgressBar.Draw("merging screen files to skin.xml", i, fileList.Length);
                        i++;
                    }
                }

                Console.WriteLine();

                skinFileString = String.Format("{0}\n</skin>", skinFileString, FileMode.Create);

                File.WriteAllText(skinFileName, skinFileString);

                MyVersion myVersion = new MyVersion();
                myVersion.IncreaseBuild();
                myVersion.Save();
                myVersion.Load();
                Console.WriteLine(String.Format("version: {0}", myVersion.Get()));

                Console.WriteLine();
                if (Directory.Exists(settings.VuPlusSkinPath))
                {
                    File.Copy(skinFileName, skinProductionFileName, true);
                    File.Copy(myVersion.FullFileName, settings.VuPlusSkinPath + myVersion.FileName, true);
                    Thread.Sleep(2000);
                }
                else
                {
                    Console.WriteLine();
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine(String.Format("Warn: path not exist: {0}", settings.VuPlusSkinPath));
                    Console.WriteLine();
                    Console.ForegroundColor = ConsoleColor.White;
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
