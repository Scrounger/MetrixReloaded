from Components.Converter.Converter import Converter
from Components.Element import cached

class MetrixReloadedVersion(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = str(type)
	
	@cached
	def getText(self):
		versFile = "/usr/share/enigma2/MetrixReloaded/version.info"
		pFile = open(versFile,"r")
		for line in pFile:
			return "Version: " + line.rstrip()
		pFile.close()
	
	text = property(getText)
