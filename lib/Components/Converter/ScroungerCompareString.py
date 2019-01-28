from Converter import Converter
from Components.Element import cached

class ScroungerCompareString(Converter, object):
	def __init__(self, arg):
		Converter.__init__(self, arg)
		self.value = arg

	@cached
	def getBoolean(self):
		return self.source.text.lower() == self.value.lower()

	boolean = property(getBoolean)