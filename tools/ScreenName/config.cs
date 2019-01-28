using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Xml;
using System.Xml.Serialization;

namespace ScreenName
{
    public class Config
    {

        const string fileName = "screenName.config";
        private string appPath = System.IO.Path.GetDirectoryName(Assembly.GetEntryAssembly().Location);

        public Config()
        {
        }

        #region "Properties"
        private string skinFileName;
        [XmlAttribute(AttributeName = "skinFile")]
        public string SkinFileName
        {
		    get
		    {
		        return this.skinFileName;
		    }
		    set
		    {
		        this.skinFileName = value;
		    }
        }

        private string screenNameElement;
        [XmlAttribute(AttributeName = "screenNameElement")]
        public string ScreenNameElement
        {
		    get
		    {
		        return this.screenNameElement;
		    }
		    set
		    {
		        this.screenNameElement = value;
		    }
        }
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

        public string getSkinFileName()
        {
            if (this.SkinFileName.StartsWith(".\\") || this.SkinFileName.StartsWith("./"))
            {
                return appPath + this.SkinFileName.Replace(".\\", "\\");
            }
            else
            {
                return this.SkinFileName;
            }
        }

        public string getScreenNameElement()
        {
            return this.screenNameElement;
        }
    }




}
