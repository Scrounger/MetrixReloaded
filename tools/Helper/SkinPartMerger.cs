using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace Helper
{
    public class SkinPartMerger
    {
        public static void Run(bool logSettings)
        {
            try
            {
                Settings settings = Settings.Load();

                if (logSettings)
                {
                    settings.LogSettings();
                }

                string allScreensPath = settings.SkinPath + "allScreens/";
                string skinPartsPath = settings.SkinPartsPath;

                Console.WriteLine();
                Console.WriteLine(String.Format("copy skinParts files: '{0}' to '{1}'", skinPartsPath, allScreensPath));
                Console.WriteLine("---------------------------------------------------------------------------------------------------");

                int i = 1;
                string[] dirList = Directory.GetFiles(allScreensPath, "*.*", SearchOption.AllDirectories);

                //alle skinParts zu erst löschen
                foreach (string newPath in dirList)
                {
                    File.Delete(newPath);
                    ProgressBar.Draw("deleting files...", i, dirList.Length);
                    i++;
                }

                i = 1;
                dirList = Directory.GetFiles(skinPartsPath, "*.*", SearchOption.AllDirectories);

                //alle skinParts kopieren
                foreach (string newPath in dirList)
                {
                    File.Copy(newPath, Path.Combine(allScreensPath, newPath.Remove(0, skinPartsPath.Length)), true);
                    ProgressBar.Draw("copy files...", i, dirList.Length);
                    i++;
                }
                Console.WriteLine();
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
