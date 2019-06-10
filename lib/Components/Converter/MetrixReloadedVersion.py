from Components.Converter.Converter import Converter
from Components.Element import cached

from Plugins.Extensions.MetrixReloaded.MetrixReloadedHelper import getVersion

class MetrixReloadedVersion(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = str(type)
	
	@cached
	def getText(self):
		return "Version: %s" % getVersion()
	
	text = property(getText)
