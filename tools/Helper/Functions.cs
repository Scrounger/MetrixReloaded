using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace Helper
{
    public class Functions
    {
        public static void CopyAll(string SourcePath, string DestinationPath, bool createDirs, String message = null)
        {
            Console.WriteLine();
            if (message == null)
            {
                Console.WriteLine(String.Format("copy files: '{0}' to '{1}'", SourcePath, DestinationPath));
            }
            else
            {
                Console.WriteLine(message);
            }
            Console.WriteLine("---------------------------------------------------------------------------------------------------");
            //Now Create all of the directories
            int i = 1;

            string[] dirList = Directory.GetDirectories(SourcePath, "*", SearchOption.AllDirectories);
            if (createDirs)
            {
                foreach (string dirPath in dirList)
                {
                    Directory.CreateDirectory(Path.Combine(DestinationPath, dirPath.Remove(0, SourcePath.Length)));

                    ProgressBar.Draw("create directories...", i, dirList.Length);
                    i++;
                }
                Console.WriteLine();
            }
            i = 1;
            dirList = Directory.GetFiles(SourcePath, "*.*", SearchOption.AllDirectories);

            //Copy all the files & Replaces any files with the same name
            foreach (string newPath in dirList)
            {
                File.Copy(newPath, Path.Combine(DestinationPath, newPath.Remove(0, SourcePath.Length)), true);
                ProgressBar.Draw("copy files...", i, dirList.Length);
                i++;
            }

            Console.WriteLine();
        }
    }
}
