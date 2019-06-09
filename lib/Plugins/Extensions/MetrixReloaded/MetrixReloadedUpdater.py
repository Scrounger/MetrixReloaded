# -*- coding: utf-8 -*-
import json
import os
import re
from twisted.web.client import downloadPage, getPage


from Screens.MessageBox import MessageBox
from Screens.Ipkg import Ipkg, PackageSelection
from Screens.Standby import TryQuitMainloop
from Components.config import config, getConfigListEntry
from Components.Ipkg import IpkgComponent


from Tools.MetrixReloadedHelper import initializeLog, getVersion
from MetrixReloadedTranslation import _

class MetrixReloadedUpdater:
    CHECK_VERSION = "CHECK_VERSION"
    DOWNLOAD = "DOWNLOAD"

    def __init__(self, session, manualMode=False):
        self.log = initializeLog("MetrixReloadedUpdater")
        self.session = session
        self.currentVersion = getVersion()
        self.manualMode = manualMode

        self.checkVersion()

    def checkVersion(self):
        self.log.info("check for new version - current version: %s (manualMode: %s)" %
                      (self.currentVersion, str(self.manualMode)))

        getPage('https://api.github.com/repos/Scrounger/MetrixReloaded/releases/latest').addCallback(
            self.response, self.CHECK_VERSION).addErrback(self.responseError, self.CHECK_VERSION)

    def response(self, data, response):
        if (response == self.CHECK_VERSION):
            jsonData = json.loads(data)

            self.releasedVersion = str(jsonData['tag_name'])
            self.log.debug("released version: %s" % self.releasedVersion)

            self.downloadUrl = str(jsonData['assets'][0]['browser_download_url'])
            self.fileName = str(jsonData['assets'][0]['name'])

            # Prüfen ob Version neuer ist
            # if(self.currentVersion != self.releasedVersion):
            if(self.compareVersions(self.releasedVersion, self.currentVersion) > 0):
                self.log.info("new version: %s avaiable" %
                              self.releasedVersion)

                if(config.plugins.MetrixReloaded.autoDownloadNewVersion.value == True and self.manualMode == False):
                    # AutoUpdate ist aktiviert und kein manueller aufruf
                    self.downloadNewVersion()
                else:
                    msg = _("A new version of MetrixReloaded skin is available!\n\nInstalled version:\t%s\nNew version:\t%s\n\nWould you like to download the new version in the background?") % (self.currentVersion, self.releasedVersion)

                    # User fragen ob version heruntergeladen werden soll
                    self.session.openWithCallback(
                        self.msgBoxResponseStartDownload, MessageBox, msg, MessageBox.TYPE_YESNO, timeout=30)
            else:
                self.log.info("current version %s is up to date!" %
                              self.currentVersion)

                if(self.manualMode):
                    self.session.open(MessageBox, _(
                        "No new version available.\nMetrixReloaded is up to date!"), MessageBox.TYPE_INFO, timeout=10)

        elif(response == self.DOWNLOAD):
            # Zum Ipkg Screen gehen -> Installation
            if (os.path.exists(self.targetFileName)):
                self.log.info("new version successful downloaded! filename: %s" % (
                    self.targetFileName))

                msg = _("MetrixReloaded version %s successful downloaded!\n\nWould you like to install the update?") % (
                    self.releasedVersion)

                self.session.openWithCallback(
                    self.msgBoxResponseStartInstallation, MessageBox, msg, MessageBox.TYPE_YESNO, timeout=30)

    def responseError(self, e, response):
        self.log.exception("response: [%s] %s", response, str(e))

        msg = _("Error: [%s] %s") % (response, str(e))

        self.session.open(MessageBox, msg, MessageBox.TYPE_ERROR, timeout=30)

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
            config.plugins.MetrixReloaded.updated.value = True
            config.plugins.MetrixReloaded.updated.save()

            cmdList.append((IpkgComponent.CMD_INSTALL, {
                           "package": self.targetFileName}))
            self.session.openWithCallback(
                self.restartGUI, Ipkg, cmdList=cmdList)

    def downloadNewVersion(self):
        # Donwload der neuen Version
        self.log.debug("download url: %s" % self.downloadUrl)

        self.targetFileName = "/tmp/%s" % self.fileName

        self.log.debug("downloading new version...")
        downloadPage(self.downloadUrl, self.targetFileName).addCallback(
            self.response, self.DOWNLOAD).addErrback(self.responseError, self.DOWNLOAD)

    def restartGUI(self):
        # Fragen ob Restart
        self.log.debug("Installation finished")
        restartbox = self.session.openWithCallback(self.msgBoxResponseRestart, MessageBox, _(
            "Restart necessary, restart GUI now?"), MessageBox.TYPE_YESNO)

    def msgBoxResponseRestart(self, answer):
        if answer is True:
            self.session.open(TryQuitMainloop, 3)

    def compareVersions(self, version1, version2):
        def normalize(v):
            return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]
        return self.cmp(normalize(version1), normalize(version2))

    def cmp(self, a, b):
        return (a > b) - (a < b)
