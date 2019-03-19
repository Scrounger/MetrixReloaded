# -*- coding: utf-8 -*-

from Tools.MetrixReloadedHelper import initializeLog, getVersion
from twisted.web.client import downloadPage, getPage

from Screens.MessageBox import MessageBox

#Language #########################################################################################################################################
from Components.Language import language
import gettext
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from os import environ

#language
lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("MetrixReloaded", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/MetrixReloaded/locale/"))

def _(txt):
	t = gettext.dgettext("MetrixReloaded", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

###########################################################################################################################################

class MetrixReloadedUpdater:
    CHECK_VERSION = "CHECK_VERSION"

    def __init__(self, session):
        self.log = initializeLog("MetrixReloadedUpdater")
        self.session = session
        self.currentVersion = getVersion()

        self.checkVersion()

    def checkVersion(self):
        self.log.info("check for new version")
        self.log.info("current version: %s" % self.currentVersion)
        getPage('https://raw.githubusercontent.com/Scrounger/MetrixReloaded/master/version.released').addCallback(
            self.response, self.CHECK_VERSION).addErrback(self.responseError, self.CHECK_VERSION)

    def response(self, data, response):
        if (response == self.CHECK_VERSION):
            releasedVersion = data

            if(self.currentVersion != releasedVersion):
                self.log.info("new version: %s avaiable" % releasedVersion)

                msg = _("A new version of MetrixReloaded skin is available!\n\nInstalled version:\t%s\nNew version:\t%s\n\nWould you like to download the new version?") % (
                    self.currentVersion, releasedVersion)

                self.session.openWithCallback(
                    self.msgBoxResponse, MessageBox, msg, MessageBox.TYPE_YESNO)
            else:
                self.log.info("current version %s is uptodate!" % self.currentVersion)

    def responseError(self, e, response):
        self.log.exception("response: [%s] %s", response, str(e))

    def msgBoxResponse(self, result):
        if result:
            self.log.info("runter laden")
