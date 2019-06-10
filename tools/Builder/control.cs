using System;
using System.IO;
using System.Reflection;
using Newtonsoft.Json;

namespace Builder
{
    public class Control
    {
        const string fileName = "control.json";

        private string package;
        [JsonProperty(PropertyName = "package")]
        public string Package
        {
            get { return this.package; }
            set { this.package = value; }
        }

        private string version;
        [JsonProperty(PropertyName = "version")]
        public string Version
        {
            get { return this.version; }
            set { this.version = value; }
        }

        private string description;
        [JsonProperty(PropertyName = "description")]
        public string Description
        {
            get { return this.description; }
            set { this.description = value; }
        }

        private string section;
        [JsonProperty(PropertyName = "section")]
        public string Section
        {
            get { return this.section; }
            set { this.section = value; }
        }

        private string priority;
        [JsonProperty(PropertyName = "priority")]
        public string Priority
        {
            get { return this.priority; }
            set { this.priority = value; }
        }

        private string maintainer;
        [JsonProperty(PropertyName = "maintainer")]
        public string Maintainer
        {
            get { return this.maintainer; }
            set { this.maintainer = value; }
        }

        private string architecture;
        [JsonProperty(PropertyName = "architecture")]
        public string Architecture
        {
            get { return this.architecture; }
            set { this.architecture = value; }
        }

        private string license;
        [JsonProperty(PropertyName = "license")]
        public string License
        {
            get { return this.license; }
            set { this.license = value; }
        }

        private string homepage;
        [JsonProperty(PropertyName = "homepage")]
        public string Homepage
        {
            get { return this.homepage; }
            set { this.homepage = value; }
        }

        private string source;
        [JsonProperty(PropertyName = "source")]
        public string Source
        {
            get { return this.source; }
            set { this.source = value; }
        }

        private string depends;
        [JsonProperty(PropertyName = "depends")]
        public string Depends
        {
            get { return this.depends; }
            set { this.depends = value; }
        }

        public static Control Load()
        {
            Control control;

            if (File.Exists(fileName))
            {
                using (StreamReader reader = new StreamReader(fileName))
                {
                    control = (Control)JsonConvert.DeserializeObject<Control>(reader.ReadToEnd());
                }

                return control;
            }

            return null;
        }
    }
}
