from Converter import Converter
from Components.Element import cached

class MetrixReloadedCompareBoolean(Converter, object):
	def __init__(self, arg):
		Converter.__init__(self, arg)
		self.value = arg

	@cached
	def getBoolean(self):
		return str(self.source.boolean).lower() == self.value.lower()

	boolean = property(getBoolean)