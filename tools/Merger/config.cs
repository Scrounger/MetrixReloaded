using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Xml;
using System.Xml.Serialization;

namespace Merger
{
    public class Config
    {

        const string fileName = "merger.config";
        private string appPath = System.IO.Path.GetDirectoryName(Assembly.GetEntryAssembly().Location);

        public Config()
        {
        }

        #region "Properties"
        private string skinFilePath;
        [XmlAttribute(AttributeName = "skinFilePath")]
        public string SkinFilePath { get => skinFilePath; set => skinFilePath = value; }

        private string inputPath;
        [XmlAttribute(AttributeName = "inputPath")]
        public string InputPath { get => inputPath; set => inputPath = value; }

        private string productionPath;
        [XmlAttribute(AttributeName = "productionPath")]
        public string ProductionPath { get => productionPath; set => productionPath = value; }
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

        public string getInputPath()
        {
            if (this.InputPath.StartsWith(".\\") || this.InputPath.StartsWith("./"))
            {
                return appPath + this.InputPath.Replace(".", "");
            }
            else
            {
                return this.InputPath;
            }
        }

        public string getProductionPath()
        {
            if (this.ProductionPath.StartsWith(".\\") || this.ProductionPath.StartsWith("./"))
            {
                return appPath + this.ProductionPath.Replace(".", "");
            }
            else
            {
                return this.ProductionPath;
            }
        }
    }




}
