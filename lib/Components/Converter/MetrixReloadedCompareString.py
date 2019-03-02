from Converter import Converter
from Components.Element import cached

class MetrixReloadedCompareString(Converter, object):
	def __init__(self, arg):
		Converter.__init__(self, arg)
		self.value = arg

	@cached
	def getBoolean(self):
		return self.source.text.lower() == self.value.lower()

	boolean = property(getBoolean)

	@cached
	def getText(self):
		if(self.source.text.lower() == self.value.lower()):
			return self.source.text
		
		return ''
	
	text = property(getText)