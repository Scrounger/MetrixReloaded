# -*- coding: utf-8 -*-

# GUI (Screens)
from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Screens.MessageBox import MessageBox

# Configuration
from Components.config import config, getConfigListEntry

# GUI (Components)
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText

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
        self.log.debug("Debug: MetrixReloadedSetup open")
        self.log.debug(str(config.plugins.MetrixReloaded.debug.value))

        # Summary
        self.setTitle("MetrixReloaded Configuration")
        self.onChangedEntry = []

        try:
            self.list = [
                getConfigListEntry(_("Online Modus"), config.plugins.MetrixReloaded.onlineMode, _(
                    "Wenn der Online Modus aktiviert ist, werden im Hintergrund zustzliche Informationen heruntergeladen")),
                getConfigListEntry(_("Log Debug Modus"), config.plugins.MetrixReloaded.debug, _(
                    "Log Debug Modus aktivieren")),
                getConfigListEntry(_("Verzeichnis Log Dateien"), config.plugins.MetrixReloaded.logDirectory, _(
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
            self["key_green"] = StaticText(_("OK"))
            self["key_yellow"] = StaticText(_("Refresh now"))
            self["key_blue"] = StaticText(_("Edit Services"))

            self["help"] = StaticText()

            # Define Actions
            self["actions"] = ActionMap(["SetupActions", "ColorActions", "ChannelSelectEPGActions", "HelpActions"],
                                        {
                "cancel": self.keyCancel,
                "save": self.keySave,
                # "yellow": self.forceRefresh,
                # "blue": self.editServices,
                # "showEPGList": self.keyInfo,
                # "displayHelp": self.showHelp,
            }
            )

            # Trigger change
            self.changed()

            # self.onLayoutFinish.append(self.setCustomTitle)

            # self["myLabel"] = Label(_("please press OK"))
            # # Define Actions
            # self["myActionsMap"] = ActionMap(["SetupActions", "ColorActions"],
            #                                  {
            #     "ok": self.myMsg,
            #     "cancel": self.close,
            # }, -1)

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

    def updateHelp(self):
        cur = self["config"].getCurrent()
        if cur:
            self["help"].text = cur[2]

    def changed(self):
        for x in self.onChangedEntry:
            try:
                x()
            except Exception:
                pass