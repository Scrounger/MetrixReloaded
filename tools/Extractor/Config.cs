using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Xml;
using System.Xml.Serialization;

namespace Extractor
{
    public class Config
    {

        const string fileName = "extractor.config";
        private string appPath = System.IO.Path.GetDirectoryName(Assembly.GetEntryAssembly().Location);

        public Config()
        {
        }

        #region "Properties"
        private string skinFilePath;
        [XmlAttribute(AttributeName = "skinFilePath")]
        public string SkinFilePath { get => skinFilePath; set => skinFilePath = value; }

        private string outputPath;
        [XmlAttribute(AttributeName = "outputPath")]
        public string OutputPath { get => outputPath; set => outputPath = value; }
        #endregion

        public static Config Load()
        {
            Config config;

            XmlSerializer deserializer = new XmlSerializer(typeof(Config));

            if (File.Exists(fileName))
            {
                using (XmlReader reader = XmlReader.Create(fileName))
                {
                    config = (Config)deserializer.Deserialize(reader);
                }

                return config;
            }

            return null;
        }

        public string getSkinFilePath()
        {
            if (this.SkinFilePath.StartsWith(".\\") || this.SkinFilePath.StartsWith("./"))
            {
                return appPath + this.SkinFilePath.Replace(".", "");
            }
            else
            {
                return this.SkinFilePath;
            }
        }

        public string getOutputPath()
        {
            if (this.OutputPath.StartsWith(".\\") || this.OutputPath.StartsWith("./"))
            {
                return appPath + this.OutputPath.Replace(".", "");
            }
            else
            {
                return this.OutputPath;
            }

        }
    }
}
