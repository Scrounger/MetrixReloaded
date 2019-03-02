using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;
using Helper;

namespace ImageFinder
{
    class ImageFinder
    {
        static void Main(string[] args)
        {
            try
            {
                Settings settings = Settings.Load();

                string skinFilePath = settings.SkinPath;
                string skinFileName = skinFilePath + "skin.xml";

                List<string> imageList = new List<string>(Directory.GetFiles(@skinFilePath, "*.png", System.IO.SearchOption.AllDirectories));

                Console.Write("{0} images found in {1}", imageList.Count(), skinFilePath);
                Console.WriteLine();
                Console.WriteLine();

                Console.Write("Not used images listed below:\n");
                XDocument xdoc = XDocument.Load(skinFileName);
                string skinXml = xdoc.ToString();

                foreach (string path in imageList)
                {
                    string fileName = Path.GetFileName(path);

                    if (!skinXml.Contains(fileName))
                    {
                        Console.Write("{0}:\n", path.Replace(skinFilePath, "\\"));
                    }
                }

                Console.WriteLine();
                Console.Write("Press any key to exit");
                Console.ReadKey();
            }
            catch (Exception ex)
            {
                Console.WriteLine();
                Console.WriteLine();
                Console.Write("Error: {0}\n", ex.Message);
                Console.Write("Error: {0}\n", ex.StackTrace);
                Console.WriteLine();
                Console.Write("Press any key to exit");
                Console.ReadKey();
            }
        }
    }
}
