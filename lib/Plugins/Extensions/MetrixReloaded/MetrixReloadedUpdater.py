# -*- coding: utf-8 -*-

from Tools.MetrixReloadedHelper import initializeLog, getVersion
from twisted.web.client import downloadPage, getPage

from Screens.MessageBox import MessageBox
from Screens.Ipkg import Ipkg, PackageSelection
from Screens.Standby import TryQuitMainloop

# Configuration
from Components.config import config, getConfigListEntry

from Components.Ipkg import IpkgComponent

#Language #########################################################################################################################################
from Components.Language import language
import gettext
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from os import environ, path
import re

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
            #if(self.currentVersion != self.releasedVersion):
            if(self.compareVersions(self.releasedVersion, self.currentVersion) > 0):
                self.log.info("new version: %s avaiable" % self.releasedVersion)

                if(config.plugins.MetrixReloaded.autoDownloadNewVersion.value == True and self.manualMode == False):
                    #AutoUpdate ist aktiviert und kein manueller aufruf
                    self.downloadNewVersion()
                else:
                    msg = _("A new version of MetrixReloaded skin is available!\n\nInstalled version:\t%s\nNew version:\t%s\n\nWould you like to download the new version in the background?") % (
                        self.currentVersion, self.releasedVersion)

                    #User fragen ob version heruntergeladen werden soll
                    self.session.openWithCallback(
                        self.msgBoxResponseStartDownload, MessageBox, msg, MessageBox.TYPE_YESNO, timeout = 30)
            else:
                self.log.info("current version %s is up to date!" % self.currentVersion)

                if(self.manualMode):
                    self.session.open(MessageBox, _("No new version available.\nMetrixReloaded is up to date!"), MessageBox.TYPE_INFO, timeout=10)

        elif(response == self.DOWNLOAD):
            #Zum Ipkg Screen gehen -> Installation
            if (path.exists(self.targetFileName)):
                self.log.info("new version successful downloaded! filename: %s" % (self.targetFileName))

                msg = _("MetrixReloaded version %s successful downloaded!\n\nWould you like to install the update?") %(self.releasedVersion)
                
                self.session.openWithCallback(
                    self.msgBoxResponseStartInstallation, MessageBox, msg, MessageBox.TYPE_YESNO, timeout = 30)

    def responseError(self, e, response):
        self.log.exception("response: [%s] %s", response, str(e))

    def msgBoxResponseStartDownload(self, answer):
        if answer:
            self.downloadNewVersion()
    
    def msgBoxResponseStartInstallation(self, answer):
        if answer:
            self.installUpdate()

    def installUpdate(self):
        self.log.debug("Start installation")
        cmdList = []

        if self.targetFileName and self.session:
            cmdList.append((IpkgComponent.CMD_INSTALL, {"package": self.targetFileName}))
            self.session.openWithCallback(self.restartGUI, Ipkg, cmdList = cmdList)
    
    def downloadNewVersion(self):
            #Donwload der neuen Version
            fileName = "enigma2-skin-metrixreloaded_%s_all.ipk" % (self.releasedVersion)
            url = "https://github.com/Scrounger/MetrixReloaded/releases/download/%s/%s" % (self.releasedVersion, fileName)
            self.log.debug("download url: %s" % url)

            self.targetFileName = "/tmp/%s" % fileName

            self.log.debug("downloading new version...")
            downloadPage(url, self.targetFileName).addCallback(
                            self.response, self.DOWNLOAD).addErrback(self.responseError, self.DOWNLOAD)

    def restartGUI(self):
        #Fragen ob Restart
        self.log.debug("Installation finished")
        restartbox = self.session.openWithCallback(self.msgBoxResponseRestart,MessageBox,_("Restart necessary, restart GUI now?"), MessageBox.TYPE_YESNO)        

    def msgBoxResponseRestart(self, answer):
        if answer is True:
            self.session.open(TryQuitMainloop, 3)

    def compareVersions(self, version1, version2):
        def normalize(v):
            return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
        return self.cmp(normalize(version1), normalize(version2))
    
    def cmp(self, a, b):
        return (a > b) - (a < b)
            
