from Components.VariableText import VariableText
from Renderer import Renderer

from enigma import eLabel

class MetrixReloadedClearFavName(VariableText, Renderer):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)

	GUI_WIDGET = eLabel

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))

	def changed(self, what):
		if what[0] == self.CHANGED_CLEAR:
			self.text = ""
		else:
			self.text = self.source.text.replace("(TV)", "").replace("(Radio)", "").replace("User - bouquets", "").replace("Bouquets", "").replace("/", "").replace( _("Channel Selection"), "")

