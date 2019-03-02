using System;
using System.IO;
using System.Reflection;
using Newtonsoft.Json;

namespace Tools
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

        private string vuPlusSkinPath;

        [JsonProperty(PropertyName = "vuPlusSkinPath")]
        public string VuPlusSkinPath
        {
            get { return CreatePath(this.vuPlusSkinPath); }
            set { this.vuPlusSkinPath = value; }
        }


        public static Settings Load()
        {
            Settings settings;

            if (File.Exists(fileName))
            {
                using (StreamReader reader = new StreamReader(fileName))
                {
                    settings = (Settings)JsonConvert.DeserializeObject<Tools.Settings>(reader.ReadToEnd());
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
            
            foreach (PropertyInfo property in properties)
            {
                Console.WriteLine(String.Format("{0}: \t\t\t {1}", property.Name, property.GetValue(this, null)));
            }
            Console.WriteLine("------------------------------------------------------------------------");
            Console.WriteLine();
        }
    }
}
