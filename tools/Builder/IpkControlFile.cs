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
                "Package: " + "enigma2-plugin-skin-metrixreloaded" + "\n" +
                "Version: " + version + "\n" +
                "Description: " + "Skin MetrixReloaded" + "\n" +
                "Section: " + "skin" + "\n" +
                "Priority: " + "optional" + "\n" +
                "Maintainer: " + "scrounger" + "\n" +
                "Architecture: " + "all" + "\n" +
                "License: " + "GNU GPLv3" + "\n" +
                "Homepage: " + "https://github.com/Scrounger/MetrixReloaded" + "\n" +
                "Source: " + "https://github.com/Scrounger/MetrixReloaded" + "\n" +
                "Depends: " + "enigma2-python (>=vti-14)" + "," + "enigma2-plugin-systemplugins-exteventinfohandler";

            System.IO.File.WriteAllText(filename, content);
        }
    }
}
