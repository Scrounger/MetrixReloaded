from Components.Converter.Converter import Converter
from Components.Element import cached

#Language #########################################################################################################################################
from Components.Language import language
import gettext
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from os import environ

# language
lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("MetrixReloaded", "%s%s" % (
    resolveFilename(SCOPE_PLUGINS), "Extensions/MetrixReloaded/locale/"))


def _(txt):
    t = gettext.dgettext("MetrixReloaded", txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t
###########################################################################################################################################

class MetrixReloadedTextTranslator(Converter, object):
	movecopy = 0
	currentlyrunning = 1
	itfollows = 2
	coming = 3
	runningsince = 4
	preview = 5
	runsuntil = 6
	clock = 7
	timeshiftactive = 8
	untillive = 9
	temperature = 10
	cpuload = 11
	satellite = 12
	fanspeed = 13
	avgload = 14
	signal = 15
	tuner = 16
	video = 17
	ecm = 18
	flash = 19
	ram = 20
	hdd = 21
	usb = 22
	sys = 23
	rm = 24
	cpu = 25
	load = 26
	sat = 27
	snr = 28
	temp = 29
	wind = 30
	clime = 31
	city = 32
	name = 33
	birthday = 34
	age = 35
	brsettings = 36
	brpath = 37
	

	def __init__(self, type):
		Converter.__init__(self, type)

		if type == "movecopy":
			self.type = self.movecopy
		elif type == "currentlyrunning":
			self.type = self.currentlyrunning
		elif type == "itfollows":
			self.type = self.itfollows
		elif type == "coming":
			self.type = self.coming
		elif type == "runningsince":
			self.type = self.runningsince
		elif type == "preview":
			self.type = self.preview
		elif type == "runsuntil":
			self.type = self.runsuntil
		elif type == "clock":
			self.type = self.clock
		elif type == "timeshiftactive":
			self.type = self.timeshiftactive
		elif type == "untillive":
			self.type = self.untillive
		elif type == "temperature":
			self.type = self.temperature
		elif type == "cpuload":
			self.type = self.cpuload
		elif type == "satellite":
			self.type = self.satellite
		elif type == "fanspeed":
			self.type = self.fanspeed
		elif type == "avgload":
			self.type = self.avgload
		elif type == "signal":
			self.type = self.signal
		elif type == "tuner":
			self.type = self.tuner
		elif type == "video":
			self.type = self.video
		elif type == "ecm":
			self.type = self.ecm
		elif type == "flash":
			self.type = self.flash
		elif type == "ram":
			self.type = self.ram
		elif type == "hdd":
			self.type = self.hdd
		elif type == "usb":
			self.type = self.usb
		elif type == "sys":
			self.type = self.sys
		elif type == "rm":
			self.type = self.rm
		elif type == "cpu":
			self.type = self.cpu
		elif type == "load":
			self.type = self.load
		elif type == "sat":
			self.type = self.sat
		elif type == "snr":
			self.type = self.snr
		elif type == "temp":
			self.type = self.temp
		elif type == "wind":
			self.type = self.wind
		elif type == "clime":
			self.type = self.clime
		elif type == "city":
			self.type = self.city
		elif type == "name":
			self.type = self.name
		elif type == "birthday":
			self.type = self.birthday
		elif type == "age":
			self.type = self.age
		elif type == "brsettings":
			self.type = self.brsettings
		elif type == "brpath":
			self.type = self.brpath

	@cached
	def getText(self):
		if self.type == self.movecopy:
			return _('Move/Copy')
		elif self.type == self.currentlyrunning:
			return _('currently running:')
		elif self.type == self.itfollows:
			return _('it follows:')
		elif self.type == self.coming:
			return _('coming:')
		elif self.type == self.runningsince:
			return _('running since')
		elif self.type == self.preview:
			return _('preview') + ":"
		elif self.type == self.runsuntil:
			return _('runs until')
		elif self.type == self.clock:
			return _('   ')
		elif self.type == self.timeshiftactive:
			return _('timeshift active')
		elif self.type == self.untillive:
			return _('until live:')
		elif self.type == self.temperature:
			return _('temperature') + ":"
		elif self.type == self.cpuload:
			return _('CPU load:')
		elif self.type == self.satellite:
			return _('satellite') + ":"
		elif self.type == self.fanspeed:
			return _('fanspeed:')
		elif self.type == self.avgload:
			return _('AVG load:')
		elif self.type == self.signal:
			return _('signal') + ":"
		elif self.type == self.tuner:
			return _('tuner') + ":"
		elif self.type == self.video:
			return _('video') + ":"
		elif self.type == self.ecm:
			return _('ECM:')
		elif self.type == self.flash:
			return _('Flash:')
		elif self.type == self.ram:
			return _('Ram:')
		elif self.type == self.hdd:
			return _('HDD:')
		elif self.type == self.usb:
			return _('USB:')
		elif self.type == self.sys:
			return _('SYS:')
		elif self.type == self.rm:
			return _('r/m:')
		elif self.type == self.cpu:
			return _('CPU:')
		elif self.type == self.load:
			return _('load') + ":"
		elif self.type == self.sat:
			return _('Sat:')
		elif self.type == self.snr:
			return _('SNR:')
		elif self.type == self.temp:
			return _('temp:')
		elif self.type == self.wind:
			return _('wind:')
		elif self.type == self.clime:
			return _('clime:')
		elif self.type == self.city:
			return _('city:')
		elif self.type == self.name:
			return _('Name')
		elif self.type == self.birthday:
			return _('Birthday')
		elif self.type == self.age:
			return _('Age')
		elif self.type == self.brsettings:
			return _('Birthday Reminder Settings')
		elif self.type == self.brpath:
			return _('Select a path for the birthday file')

	text = property(getText)
