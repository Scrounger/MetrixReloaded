using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;

namespace Tools
{
    public class MyVersion
    {
        private string version;

        const string fileName = "version.info";

        public string FileName
        {
            get { return fileName; }
        }

        private string fullFileName;
        public string FullFileName
        {
            get { return fullFileName; }
        }

        private int major;
        public int Major
        {
            get { return major; }
            set { this.major = value; }
        }

        private int minor;
        public int Minor
        {
            get { return minor; }
            set { this.minor = value; }
        }

        private int build;
        public int Build
        {
            get { return build; }
            set { this.build = value; }
        }

        public MyVersion()
        {
            //Prüfen ob version.info schon existiert
            Settings settings = Settings.Load();
            fullFileName = settings.SkinPath + fileName;

            Load();
        }

        public void IncreaseMinor()
        {
            this.minor = this.minor + 1;
        }

        public void IncreaseBuild()
        {
            this.build = this.build + 1;
        }

        public String Get()
        {
            return String.Format("{0}.{1}.{2}", major, minor, build);
        }

        public void Save()
        {
            System.IO.File.WriteAllText(fullFileName, Get());
        }

        public void Load()
        {
            if (File.Exists(fullFileName))
            {
                StreamReader sr = new StreamReader(fullFileName);
                version = sr.ReadLine();
                sr.Close();

                Regex r = new Regex(@"^(\d+).(\d+).(\d+)");
                Match m = r.Match(version);

                if (m.Success)
                {
                    major = int.Parse(m.Groups[1].ToString());
                    minor = int.Parse(m.Groups[2].ToString());
                    build = int.Parse(m.Groups[3].ToString());
                }
            }
        }
    }
}
