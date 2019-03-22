from Renderer import Renderer
from Components.config import config

from enigma import eLabel

class MetrixReloadedScreenNameLabel(Renderer):
	def __init__(self):
		Renderer.__init__(self)

	GUI_WIDGET = eLabel

	def changed(self, what):
		if(config.plugins.MetrixReloaded.showScreenNames.value == False):
				self.hide()

