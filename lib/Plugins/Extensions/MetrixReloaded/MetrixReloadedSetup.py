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

import os

# MyLog
from Tools.MetrixReloadedHelper import initializeLog

#from Tools import Notifications


class MetrixReloadedSetup(Screen, ConfigListScreen):
    """Configuration of MetrixReloaded"""

    skin = """<screen name="EPGRefreshConfiguration" position="center,center" size="600,430">
		<ePixmap position="0,5" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
		<ePixmap position="140,5" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
		<ePixmap position="280,5" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" />
		<ePixmap position="420,5" size="140,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" />
		<ePixmap position="562,15" size="35,25" pixmap="skin_default/buttons/key_info.png" alphatest="on" />

		<widget source="key_red" render="Label" position="0,5" zPosition="1" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
		<widget source="key_green" render="Label" position="140,5" zPosition="1" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
		<widget source="key_yellow" render="Label" position="280,5" zPosition="1" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
		<widget source="key_blue" render="Label" position="420,5" zPosition="1" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />

		<widget name="config" position="5,50" size="590,275" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/div-h.png" position="0,335" zPosition="1" size="565,2" />
		<widget source="help" render="Label" position="5,345" size="590,83" font="Regular;21" />
	</screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.log = initializeLog("MetrixReloadedSetup")

        self.log.info("MetrixReloadedSetup open")

        # Summary
        self.setTitle("MetrixReloaded Configuration")
        self.onChangedEntry = []

        try:
            self.list = [
                getConfigListEntry(_("Online Modus"), config.plugins.MetrixReloaded.onlineMode, _(
                    "Wenn der Online Modus aktiviert ist, werden im Hintergrund zustzliche Informationen heruntergeladen")),
                getConfigListEntry(_("enable debug"), config.plugins.MetrixReloaded.debug),
                getConfigListEntry(_("Verzeichnis der Log Dateien"), config.plugins.MetrixReloaded.logDirectory, _(
                    "Bla Bla")),
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

            # Define Actions
            self["actions"] = ActionMap(["SetupActions", "ColorActions", "ChannelSelectEPGActions", "HelpActions"],
                                        {
                "cancel": self.keyCancel,
                "save": self.keySave,
                "yellow": self.keyYellow,
                # "blue": self.editServices,
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
            self.session.open(MessageBox, _("Sorry, but the plugin %s is not installed at your Vu+ STB! Please install it to use this function" % "AtileHD"), MessageBox.TYPE_ERROR)
    
    def keyOK(self):
        if (self['config'].getCurrent()[1] == config.plugins.MetrixReloaded.logDirectory):
            start_dir = config.plugins.MetrixReloaded.logDirectory.value
            self.session.openWithCallback(self.fileDirBrowserResponse, FileDirBrowser,initDir = start_dir, title = _("Choose folder"), getFile = False, getDir = True,showDirectories = True, showFiles = False)

    def fileDirBrowserResponse(self, path):
        if path:
            self["config"].getCurrent()[1].value = path

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