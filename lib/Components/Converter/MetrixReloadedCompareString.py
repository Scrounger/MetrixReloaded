# -*- coding: utf-8 -*-
from Converter import Converter
from Components.Element import cached
import re

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
		#Prüfen ob Wert nicht null ist -> indivduelle Rückgabe
		parser = re.match(r'^[[]NotEmpty[(](.*)[)][]]', self.value)
		if(parser != None):
			if(self.source.text.lower() != None and self.source.text.lower() != ''):
				return parser.group(1)

		if(self.value == "[NotEmpty]"):
			if(self.source.text.lower() != None and self.source.text.lower() != ''):
				return self.source.text.lower()

		if(self.source.text.lower() == self.value.lower()):
			return self.source.text
		
		return ''
	
	text = property(getText)