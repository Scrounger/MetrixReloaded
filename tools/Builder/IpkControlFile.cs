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
            string content =
                "Package: " + "enigma2-skin-metrixreloaded" + "\n"+
                "Version: " + version + "\n" +
                "Description: " + "Skin MetrixReloaded" + "\n" +
                "Section: " + "skin" + "\n" +
                "Priority: " + "optional" + "\n" +
                "Maintainer: " + "scrounger" + "\n" +
                "Architecture: " + "all" + "\n" +
                "License: " + "" + "\n" +
                "Homepage: " + "" + "\n" +
                "Source: " + "";

            System.IO.File.WriteAllText(filename, content);
        }
    }
}
