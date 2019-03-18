# -*- coding: utf-8 -*-

# GUI (Screens)
from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Screens.MessageBox import MessageBox
from Screens.FileDirBrowser import FileDirBrowser


# Configuration
from Components.config import config, getConfigListEntry

# GUI (Components)
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.Label import Label

from twisted.web.client import downloadPage, getPage

import os

import MetrixReloadedUpdater

# MyLog
from Tools.MetrixReloadedHelper import initializeLog, getVersion

#from Tools import Notifications


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

class MetrixReloadedSetup(Screen, ConfigListScreen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.log = initializeLog("MetrixReloadedSetup")

        self.log.info("MetrixReloadedSetup open")

        # Summary
        self.setTitle(_("MetrixReloaded Configuration"))
        self.onChangedEntry = []

        try:
            self.list = [
                getConfigListEntry(_("Download additional data"), config.plugins.MetrixReloaded.onlineMode, _(
                    "Download additional data such as images. Requires internet connection!")),
                getConfigListEntry(_("enable debug"), config.plugins.MetrixReloaded.debug, _("show additional log informations")),
                getConfigListEntry(_("log files directory"), config.plugins.MetrixReloaded.logDirectory, _(
                    "choose the directory where log files of skin, components, etc are stored")),
            ]

            ConfigListScreen.__init__(
                self, self.list, session=session, on_change=self.changed)

            def selectionChanged():
                if self["config"].current:
                    self["config"].current[1].onDeselect(self.session)
                self["config"].current = self["config"].getCurrent()
                if self["config"].current:
                    self["config"].current[1].onSelect(self.session)
                for x in self["config"].onSelectionChanged:
                    x()

            self["config"].selectionChanged = selectionChanged
            self["config"].onSelectionChanged.append(self.updateHelp)

            # Initialize Buttons
            self["key_red"] = StaticText(_("Cancel"))
            self["key_green"] = StaticText(_("Save"))
            self["key_yellow"] = StaticText(_("Personalize your Skin"))
            self["key_blue"] = StaticText()

            self["help"] = StaticText()
            self["version"] = StaticText(_("version: %s") % getVersion())

            # Define Actions
            self["actions"] = ActionMap(["SetupActions", "ColorActions", "ChannelSelectEPGActions", "HelpActions"],
                                        {
                "cancel": self.keyCancel,
                "save": self.keySave,
                "yellow": self.keyYellow,
                "blue": self.keyBlue,
                # "showEPGList": self.keyInfo,
                # "displayHelp": self.showHelp,
            }
            )

            # Trigger change
            self.changed()

            # self.onLayoutFinish.append(self.setCustomTitle)

        except Exception as e:
            self.log.exception("MetrixReloadedSetup: %s", str(e))
            self.close()

    def myMsg(self):
        self.session.open(MessageBox, _("Hello World!"), MessageBox.TYPE_INFO)

    def keyCancel(self):
        if self["config"].isChanged():
            self.session.openWithCallback(
                self.cancelConfirm,
                MessageBox,
                _("Really close without saving settings?")
            )
        else:
            self.close(self.session)

    def keySave(self):
        for x in self["config"].list:
            x[1].save()

        self.close(self.session)
    
    def keyYellow(self):
        if (os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/AtileHD/plugin.py")):
            from Plugins.Extensions.AtileHD.plugin import *
            self.session.open(AtileHD_Config)
        else:
            msg = _("Sorry, but the plugin %s is not installed at your Vu+ STB! Please install it to use this function") % "AtileHD"
            self.session.open(MessageBox, msg, MessageBox.TYPE_ERROR)
    
    def keyBlue(self):
        test = MetrixReloadedUpdater.MetrixReloadedUpdater(self.session)

    def keyOK(self):
        if (self['config'].getCurrent()[1] == config.plugins.MetrixReloaded.logDirectory):
            start_dir = config.plugins.MetrixReloaded.logDirectory.value
            self.session.openWithCallback(self.fileDirBrowserResponse, FileDirBrowser,initDir = start_dir, title = _("Choose folder"), getFile = False, getDir = True,showDirectories = True, showFiles = False)

    def fileDirBrowserResponse(self, path):
        if path:
            self["config"].getCurrent()[1].value = path + '/'

    def updateHelp(self):
        cur = self["config"].getCurrent()
        if cur and len(cur) > 2:
            self.log.debug(cur[0])
            self.log.debug(cur[1].value)
            self["help"].text = cur[2]
        else:
            self["help"].text = ""

    def changed(self):
        for x in self.onChangedEntry:
            try:
                x()
            except Exception:
                pass