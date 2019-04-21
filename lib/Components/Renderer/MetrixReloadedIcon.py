from Renderer import Renderer
from enigma import ePixmap
from Tools.Directories import fileExists, SCOPE_CURRENT_SKIN, resolveFilename
import os

class MetrixReloadedIcon(Renderer):
	searchPaths = (resolveFilename(SCOPE_CURRENT_SKIN), '/usr/share/enigma2/skin_default/')
	skinpath = '/usr/share/enigma2/'
	
	def __init__(self):
		Renderer.__init__(self)
		self.size = None
		self.nameResCache = { }
		self.pngname = ""
		self.path = ""

	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "path":
				self.path = value
				if value.endswith("/"):
					self.path = value
				else:
					self.path = value + "/"
			else:
				attribs.append((attrib,value))
			if attrib == "size":
				value = value.split(',')
				if len(value) == 2:
					self.size = value[0] + "x" + value[1]
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	def changed(self, what):
		if self.instance:
			pngname = ""
			if what[0] != self.CHANGED_CLEAR:
				sname = self.source.text
				pngname = self.nameResCache.get(sname, "")
				if pngname == "":
					pngname = self.findIcon(sname)
					if pngname != "":
						self.nameResCache[sname] = pngname
			if pngname == "":
				self.instance.hide()
			else:
				self.instance.show()
			if pngname != "" and self.pngname != pngname:
				self.instance.setPixmapFromFile(pngname)
				self.pngname = pngname

	def findIcon(self, resName):
		pngname = self.skinpath + self.path + resName + ".png"
		if os.path.exists(pngname):
			return pngname
		else:
			if("media/logos/resolution" in self.path):
				pngname = self.skinpath + self.path + resName.replace("i", "").replace("p", "") + ".png"
				if os.path.exists(pngname):
					return pngname
			elif("media/icons/menu" in self.path):
				pngname = self.skinpath + self.path + "no_image.png"
				if os.path.exists(pngname):
					return pngname				
		
		return ""