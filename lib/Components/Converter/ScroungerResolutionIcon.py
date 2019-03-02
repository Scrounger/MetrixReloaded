from enigma import iServiceInformation, iPlayableService
from Components.Converter.Converter import Converter
from Components.Element import cached
from Poll import Poll

class MetrixReloadedResolutionIcon(Poll, Converter, object):
	GET_RESOLUTION_ICON = 0
	GET_DEFINITION_ICON = 1

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.type = type
		self.poll_interval = 1000
		self.poll_enabled = True
		self.lastResolution = "invalid type"
		self.lastDefinition = "invalid type"
		self.type, self.interesting_events = {
				"ResolutionIcon": (self.GET_RESOLUTION_ICON, (iPlayableService.evUpdatedInfo,)),
				"DefinitionIcon": (self.GET_DEFINITION_ICON, (iPlayableService.evUpdatedInfo,)),
			}[type]

	def getResolutionIcon(self,info):
		try:
			videoHeight = info.getInfo(iServiceInformation.sVideoHeight)
			progressive = ("i", "p", "")[info.getInfo(iServiceInformation.sProgressive)]
			if (int(videoHeight) > 0 and len(progressive) > 0):
				self.lastResolution = str(videoHeight) + progressive

			return self.lastResolution
		except ValueError:
			return self.lastResolution

	def getDefinitionIcon(self,info):
		try:
			videoHeight = int(info.getInfo(iServiceInformation.sVideoHeight))

			if videoHeight >= 720 and videoHeight <= 1080:
				self.lastDefinition = "HD"
			elif videoHeight > 1081:
				self.lastDefinition = "UHD"
			elif videoHeight > 0 and videoHeight < 720:
				self.lastDefinition = "SD"

			return self.lastDefinition
		except ValueError:
			return self.lastDefinition

	@cached
	def getText(self):
		service = self.source.service
		if service:
			info = service and service.info()
			if info:
				if self.type == self.GET_RESOLUTION_ICON:
					return self.getResolutionIcon(info)
				elif self.type == self.GET_DEFINITION_ICON:
					return self.getDefinitionIcon(info)
		return _("invalid type")

	text = property(getText)

	def changed(self, what):
		if what[0] == self.CHANGED_SPECIFIC:
			if what[1] == iPlayableService.evVideoSizeChanged:
				Converter.changed(self, what)
		elif what[0] != self.CHANGED_SPECIFIC or what[1] in self.interesting_events:
			Converter.changed(self, what)