from Renderer import Renderer
from Components.config import config

from enigma import eLabel

class MetrixReloadedScreenNameLabel(Renderer):
	def __init__(self):
		Renderer.__init__(self)

	GUI_WIDGET = eLabel

	def changed(self, what):
		showScreenNames = False
		try:
			showScreenNames = config.plugins.MetrixReloaded.showScreenNames.value
		except Exception as e:
			pass

		if(showScreenNames == False):
				self.hide()

