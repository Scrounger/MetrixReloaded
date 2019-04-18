from Components.VariableText import VariableText
from Components.config import config
from Renderer import Renderer
from skin import parseFont
from enigma import fontRenderClass

from enigma import eLabel

class MetrixReloadedScreenNameLabel(VariableText, Renderer):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)

		self.screenName = None
		self.screenWidth = None
		self.screenHeight = None

	GUI_WIDGET = eLabel

	def applySkin(self, desktop, screen):

		if (isinstance(screen.skinName, str)):
			self.screenName = screen.skinName
		else:
			self.screenName = ', '.join(screen.skinName)
		
		# rechts bissle Platz
		self.screenName = "%s  " % self.screenName

		if screen.skinAttributes:
			for (attrib, value) in screen.skinAttributes:
				if attrib == "size":
					self.screenWidth = value[0]
					self.screenHeight = value[1]

		if self.skinAttributes:
			attribs = [ ]
			for (attrib, value) in self.skinAttributes:
				#if attrib == "size":
					# attribs.append((attrib, "%d,25" % (len(self.screenName)*20)))
				if attrib == "position":
					attribs.append((attrib, "0,0"))
				elif attrib == "font":
					attribs.append((attrib, value))
					self.font = parseFont(value, ((1,1),(1,1)))
				else:
					attribs.append((attrib,value))
		
			# Width des Labels aus Schriftart bestimmen
			labelWidth = (self.font.pointSize / 1.8) * len(self.screenName)

			# Height des Labels aus Schriftart bestimmen
			labelHeight = fontRenderClass.getInstance().getLineHeight(self.font)
			
			# Size setzen
			attribs.append(("size", "%d,%d" % (labelWidth, labelHeight)))

			# Position in Abhngigkeit von screen size setzen
			posX = self.screenWidth - labelWidth + 1
			posY = self.screenHeight - labelHeight
			attribs.append(("position", "%d,%d" % (posX, posY)))

			self.skinAttributes = attribs

		return Renderer.applySkin(self, desktop, screen)

	def connect(self, source):
		Renderer.connect(self, source)

	def doSuspend(self, suspended):
		if suspended:
			self.changed((self.CHANGED_CLEAR,))
		else:
			self.changed((self.CHANGED_DEFAULT,))

	def changed(self, what):
		if not self.instance:
			return

		self.text = self.screenName

		showScreenNames = True
		try:
			showScreenNames = config.plugins.MetrixReloaded.showScreenNames.value
		except Exception as e:
			pass

		if(showScreenNames == False):
			self.hide()