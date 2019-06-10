using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Builder
{
    class IpkControlFile
    {
        private string version;
        private string filename;

        public IpkControlFile(string folder, string version)
        {
            this.version = version;
            this.filename = folder + "control";

        }

        public void Generate()
        {
            Control control = Control.Load();

            string content =
                "Package: " + control.Package + "\n" +
                "Version: " + version + "\n" +
                "Description: " + control.Description + "\n" +
                "Section: " + control.Section + "\n" +
                "Priority: " + control.Priority + "\n" +
                "Maintainer: " + control.Maintainer + "\n" +
                "Architecture: " + control.Architecture + "\n" +
                "License: " + control.License + "\n" +
                "Homepage: " + control.Homepage + "\n" +
                "Source: " + control.Source + "\n" +
                "Depends: " + control.Depends;

            System.IO.File.WriteAllText(filename, content);
        }
    }
}
