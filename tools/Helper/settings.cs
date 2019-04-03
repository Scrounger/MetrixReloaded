using System;
using System.IO;
using System.Reflection;
using Newtonsoft.Json;

namespace Helper
{
    public class Settings
    {
        const string fileName = "settings.cfg";

        private string projectPath;

        [JsonProperty(PropertyName = "projectPath")]
        public string ProjectPath
        {
            get { return CreatePath(this.projectPath); }
            set { this.projectPath = value; }
        }

        private string skinPath;

        [JsonProperty(PropertyName = "skinPath")]
        public string SkinPath
        {
            get { return CreatePath(this.skinPath); }
            set { this.skinPath = value; }
        }

        private string screenFilesPath;

        [JsonProperty(PropertyName = "screenFilesPath")]
        public string ScreenFilesPath
        {
            get { return CreatePath(this.screenFilesPath); }
            set { this.screenFilesPath = value; }
        }

        private string skinPartsPath;

        [JsonProperty(PropertyName = "skinPartsPath")]
        public string SkinPartsPath
        {
            get { return CreatePath(this.skinPartsPath); }
            set { this.skinPartsPath = value; }
        }

        private string vuPlusSkinPath;

        [JsonProperty(PropertyName = "vuPlusSkinPath")]
        public string VuPlusSkinPath
        {
            get { return CreatePath(this.vuPlusSkinPath); }
            set { this.vuPlusSkinPath = value; }
        }

        private string libPath;

        [JsonProperty(PropertyName = "libPath")]
        public string LibPath
        {
            get { return CreatePath(this.libPath); }
            set { this.libPath = value; }
        }

        private string buildPath;

        [JsonProperty(PropertyName = "buildPath")]
        public string BuildPath
        {
            get { return CreatePath(this.buildPath); }
            set { this.buildPath = value; }
        }

        private string screenNameElement;

        [JsonProperty(PropertyName = "screenNameElement")]
        public string ScreenNameElement
        {
            get { return this.screenNameElement; }
            set { this.screenNameElement = value; }
        }

        private string screenNameElementMetrixReloaded;

        [JsonProperty(PropertyName = "screenNameElementMetrixReloaded")]
        public string ScreenNameElementMetrixReloaded
        {
            get { return this.screenNameElementMetrixReloaded; }
            set { this.screenNameElementMetrixReloaded = value; }
        }

        private string openSkinDesignerSkinPath;

        [JsonProperty(PropertyName = "openSkinDesignerSkinPath")]
        public string OpenSkinDesignerSkinPath
        {
            get { return CreatePath(this.openSkinDesignerSkinPath); }
            set { this.openSkinDesignerSkinPath = value; }
        }

        public static Settings Load()
        {
            Settings settings;

            if (File.Exists(fileName))
            {
                using (StreamReader reader = new StreamReader(fileName))
                {
                    settings = (Settings)JsonConvert.DeserializeObject<Helper.Settings>(reader.ReadToEnd());
                }

                return settings;
            }

            return null;
        }

        private string CreatePath(string path)
        {
            path = path.Replace("\\", "/");

            if (path.StartsWith(".\\") || path.StartsWith("./"))
            {
                path = projectPath + path.Replace(".\\", "\\").Replace("./", "/").Replace("//", "/");
            }

            if (!path.EndsWith("/"))
            {
                path = path + "/";
            }

            return path;
        }

        public void LogSettings()
        {
            Type type = this.GetType();
            PropertyInfo[] properties = type.GetProperties();

            Console.WriteLine("load settings...");
            Console.WriteLine();

            foreach (PropertyInfo property in properties)
            {
                string seperator = "\t";
                if (property.Name.Length < 12)
                {
                    seperator = seperator + "\t";
                }
                Console.WriteLine(String.Format("{0}: {1} {2}", property.Name, seperator, property.GetValue(this, null)));
            }
            Console.WriteLine("---------------------------------------------------------------------------------------------------");
            Console.WriteLine();
        }
    }
}
