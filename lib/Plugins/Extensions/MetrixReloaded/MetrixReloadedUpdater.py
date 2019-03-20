# -*- coding: utf-8 -*-

from Tools.MetrixReloadedHelper import initializeLog, getVersion
from twisted.web.client import downloadPage, getPage

from Screens.MessageBox import MessageBox
from Screens.Ipkg import PackageSelection

# Configuration
from Components.config import config, getConfigListEntry

#Language #########################################################################################################################################
from Components.Language import language
import gettext
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from os import environ, path

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
    DOWNLOAD = "DOWNLOAD"

    def __init__(self, session, manualMode = False):
        self.log = initializeLog("MetrixReloadedUpdater")
        self.session = session
        self.currentVersion = getVersion()
        self.manualMode = manualMode

        self.checkVersion()

    def checkVersion(self):
        self.log.info("check for new version - current version: %s (manualMode: %s)" % (self.currentVersion, str(self.manualMode)))

        getPage('https://raw.githubusercontent.com/Scrounger/MetrixReloaded/master/version.released').addCallback(
            self.response, self.CHECK_VERSION).addErrback(self.responseError, self.CHECK_VERSION)

    def response(self, data, response):
        if (response == self.CHECK_VERSION):
            self.releasedVersion = data
            self.log.debug("released version: %s" % self.releasedVersion)

            #Prüfen ob Version neuer ist
            if(self.currentVersion != self.releasedVersion):
                self.log.info("new version: %s avaiable" % self.releasedVersion)

                if(config.plugins.MetrixReloaded.autoDownloadNewVersion.value == True and self.manualMode == False):
                    #AutoUpdate ist aktiviert und kein manueller aufruf
                    self.downloadNewVersion()
                else:
                    msg = _("A new version of MetrixReloaded skin is available!\n\nInstalled version:\t%s\nNew version:\t%s\n\nWould you like to download the new version in the background?") % (
                        self.currentVersion, self.releasedVersion)

                    #User fragen ob version heruntergeladen werden soll
                    self.session.openWithCallback(
                        self.msgBoxResponseStartDownload, MessageBox, msg, MessageBox.TYPE_YESNO)
            else:
                self.log.info("current version %s is up to date!" % self.currentVersion)

                if(self.manualMode):
                    self.session.open(MessageBox, _("No new version available.\nMetrixReloaded is up to date!"), MessageBox.TYPE_INFO, timeout=10)

        elif(response == self.DOWNLOAD):
            #Zum Ipkg Screen gehen -> Installation
            if (path.exists(self.targetFileName)):
                self.log.info("new version successful downloaded! filename: %s" % (self.targetFileName))

                msg = _("MetrixReloaded version %s successful downloaded!\n\nWould you like to open the installation screen?") %(self.releasedVersion)
                
                self.session.openWithCallback(
                    self.msgBoxResponseStartInstallation, MessageBox, msg, MessageBox.TYPE_YESNO)

    def responseError(self, e, response):
        self.log.exception("response: [%s] %s", response, str(e))

    def msgBoxResponseStartDownload(self, result):
        if result:
            self.downloadNewVersion()
    
    def msgBoxResponseStartInstallation(self, result):
        if result:
            self.session.open(PackageSelection, '/tmp/')
    
    def downloadNewVersion(self):
            #Donwload der neuen Version
            fileName = "enigma2-skin-metrixreloaded_%s_all.ipk" % (self.releasedVersion)
            url = "https://github.com/Scrounger/MetrixReloaded/releases/download/%s/%s" % (self.releasedVersion, fileName)
            self.log.debug("download url: %s" % url)

            self.targetFileName = "/tmp/%s" % fileName

            self.log.debug("downloading new version...")
            downloadPage(url, self.targetFileName).addCallback(
                            self.response, self.DOWNLOAD).addErrback(self.responseError, self.DOWNLOAD)
            
