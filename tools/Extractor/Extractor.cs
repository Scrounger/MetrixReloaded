using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Xml;
using System.Xml.Linq;

namespace Extractor
{
    class Extractor
    {
        static void Main(string[] args)
        {
            try
            {
                Config config = Config.Load();

                string skinFilePath = config.getSkinFilePath();
                string skinFileName = skinFilePath + "skin.xml";

                XDocument xdoc = XDocument.Load(skinFileName);
                int index = 0;

                Console.Write("Skin file loaded from '{0}'\n", skinFilePath);

                System.IO.DirectoryInfo directory = new System.IO.DirectoryInfo(@config.getOutputPath());

                Console.Write("Cleaning output directory '{0}'\n\n", directory);
                foreach (FileInfo file in directory.GetFiles())
                {
                    if (file.Name.Contains(".xml"))
                    {
                        file.Delete();
                    }
                }

                XmlWriterSettings settings = new XmlWriterSettings
                {
                    Indent = true,
                    OmitXmlDeclaration = true
                };

                foreach (var element in xdoc.Root.Elements())
                {
                    String fileName;

                    if (element.Attribute("name") != null)
                    {
                        fileName = directory + element.Attribute("name").Value + ".xml";
                    }
                    else
                    {
                        fileName = directory.FullName + element.Name + ".xml";
                        if (File.Exists(fileName))
                        {
                            fileName = directory.FullName + element.Name + "_" + ++index + ".xml";
                        }
                    }

                    using (XmlWriter writer = XmlWriter.Create(fileName, settings))
                    {
                        Console.Write("Creating '{0}'\n", fileName);
                        element.Save(writer);
                    }
                }

                Thread.Sleep(2000);
            }
            catch(Exception ex)
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
