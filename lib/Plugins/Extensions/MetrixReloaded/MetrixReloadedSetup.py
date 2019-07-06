# -*- coding: utf-8 -*-
from os import listdir, remove, rename, system, path, symlink, chdir, makedirs, popen
from twisted.web.client import downloadPage, getPage

# GUI (Screens)
from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Screens.MessageBox import MessageBox
from Screens.FileDirBrowser import FileDirBrowser
from Screens.Standby import TryQuitMainloop

# Configuration
from Components.config import config, getConfigListEntry, NoSave, ConfigNothing, ConfigSelection, ConfigDescription

# GUI (Components)
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Pixmap import Pixmap

# MetrixReloaded imports
from MetrixReloadedTranslation import _
import MetrixReloadedHelper as myHelper
from MetrixReloadedUpdater import MetrixReloadedUpdater
from Tools.MetrixReloadedHelper import initializeLog

#OpenConverter
#from Plugins.Extensions.OpenConverter.OpenConverterSetup import OpenConverterSetup


cur_skin = config.skin.primary_skin.value.replace('/skin.xml', '')

class MetrixReloadedSetup(Screen, ConfigListScreen):
    TYPE_COLOR = 1
    TYPE_FONT = 2

    def __init__(self, session):
        Screen.__init__(self, session)
        self.log = initializeLog("MetrixReloadedSetup")

        self.log.info("MetrixReloadedSetup open")

        self.skinParts_changed = False

        # Summary
        self.setTitle(_("MetrixReloaded Configuration"))
        self.onChangedEntry = []

        try:
            self.getInitConfig()
            self.list = []

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

                if self["config"].getCurrent() == self.set_color:
                    self.setPicture(self.myColorScheme.value, self.TYPE_COLOR)
                elif self["config"].getCurrent() == self.set_font:
                    self.setPicture(self.myFont.value, self.TYPE_FONT)
                else:
                    self["Picture"].hide()

            self["config"].selectionChanged = selectionChanged
            self["config"].onSelectionChanged.append(self.updateHelp)

            # Initialize Buttons
            self["key_red"] = StaticText(_("Cancel"))
            self["key_green"] = StaticText(_("Save"))
            self["key_yellow"] = StaticText(_("SkinParts configuration"))
            self["key_blue"] = StaticText(_("Check for updates"))

            self["help"] = StaticText()
            self["version"] = StaticText(_("version: %s") % myHelper.getVersion())

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

            self["Picture"] = Pixmap()

            self.generateList()

            # Trigger change
            self.changed()

        except Exception as e:
            self.log.exception("MetrixReloadedSetup: %s", str(e))
            self.close()

    def generateList(self):
        self.list = []

        # Liste Einträge als var, die später gebracuht werden
        self.set_color = getConfigListEntry(_("Color scheme:"), self.myColorScheme, _("Choose your color scheme"))
        self.set_font = getConfigListEntry(_("Font"), self.myFont)

        self.onlineMode = getConfigListEntry(_("Download additional data"),
                                            config.plugins.MetrixReloaded.onlineMode, _("Download additional data such as images. Requires internet connection!"))

        self.posterDownload = getConfigListEntry(_("download posters"), config.plugins.MetrixReloaded.posterDownload, _(
                "Download addtional posters from themoviedb.org or thetvddb.com"))

        self.checkForUpdates = getConfigListEntry(_("Check for skin update on startup"), config.plugins.MetrixReloaded.checkNewVersionOnStartUp, _(
            "Checks on startup (boot or standby) if a new skin version is available to download. Requires internet connection!"))

        # Listen Einträge erstellen
        self.list.append(getConfigListEntry(
            _('skin options'), ConfigDescription(), None))

        self.list.append(self.set_color)
        self.list.append(self.set_font)
        self.list.append(self.onlineMode)

        if(config.plugins.MetrixReloaded.onlineMode.value):
            self.list.append(self.posterDownload)

            if(config.plugins.MetrixReloaded.posterDownload.value):
                self.list.append(getConfigListEntry(_("poster dircetory"), config.plugins.MetrixReloaded.posterDirectory, _(
                    "choose the directory where posters are stored")))

                self.list.append(getConfigListEntry(_("posters older than x days remove"), config.plugins.MetrixReloaded.posterAutoRemove, _("use 0 for deactivation")))


        # Updates
        self.list.append(getConfigListEntry(
            _('update options'), ConfigDescription(), None))
        
        self.list.append(self.checkForUpdates)

        if(config.plugins.MetrixReloaded.checkNewVersionOnStartUp.value):
            self.list.append(getConfigListEntry(_("Auto download new version"), config.plugins.MetrixReloaded.autoDownloadNewVersion, _(
                "New version of MetrixReloaded skin will be automatically downloaded. You will get an information if new version is ready to install")))


        # Debug Options
        self.list.append(getConfigListEntry(
            _('debug options'), ConfigDescription(), None))
        self.list.append(getConfigListEntry(_("enable debug"),
                                            config.plugins.MetrixReloaded.debug, _("show additional log informations")))
        self.list.append(getConfigListEntry(_("log files directory"), config.plugins.MetrixReloaded.logDirectory, _(
            "choose the directory where log files of skin, components, etc are stored")))
        self.list.append(getConfigListEntry(
                    _("log files older than x days remove"), config.plugins.MetrixReloaded.logAutoRemove, _("use 0 for deactivation")))            

        # Developer Options
        self.list.append(getConfigListEntry(
            _('developer options'), ConfigDescription(), None))
        self.list.append(getConfigListEntry(_("show screen names"), config.plugins.MetrixReloaded.showScreenNames, _(
            "Shows the name of the current screen in the bottom right corner")))
        self.list.append(getConfigListEntry(_("show selected menu entry name"), config.plugins.MetrixReloaded.showMenuEntryNames, _(
            "Shows the name of the current selected menu entry")))

        self.list.append(getConfigListEntry(
            _('OpenConverter'), config.plugins.MetrixReloaded.openConverter))

        # Liste anzeigen
        self['config'].setList(self.list)

    def getInitConfig(self):
        self.skin_base_dir = "/usr/share/enigma2/%s/" % cur_skin

        # Farbstile
        self.default_color_file = "colors_Original.xml"
        self.color_file = "skin_user_colors.xml"

        current_color = self.getCurrentColor()
        color_choices = self.getPossibleColor()
        default_color = ("default", _("Default"))
        if current_color is None:
            current_color = default_color
        if default_color not in color_choices:
            color_choices.append(default_color)
        current_color = current_color[0]

        self.myColorScheme = NoSave(ConfigSelection(
            default=current_color, choices=color_choices))

        # Schriftart
        self.default_font_file = "font_Original.xml"
        self.font_file = "skin_user_header.xml"

        current_font = self.getCurrentFont()
        font_choices = self.getPossibleFont()
        default_font = ("default", _("Default"))
        if current_font is None:
            current_font = default_font
        if default_font not in font_choices:
            font_choices.append(default_font)
        current_font = current_font[0]

        self.myFont = NoSave(ConfigSelection(
            default=current_font, choices=font_choices))

    def keyCancel(self):
        # Screen schließen, mit Prüfung ob es Änderungen an den Einstellungen gab -> Ja -> Fragen ob schließen ohne speichern
        if self["config"].isChanged():
            self.showMsgBoxCancelConfirm()
        elif(self.skinParts_changed):
            self.showMsgBoxCancelConfirm()
        else:
            self.close(self.session)

    def keySave(self):
        # Einstellungen speichern
        if self["config"].isChanged():
            for x in self["config"].list:
                x[1].save()

            chdir(self.skin_base_dir)

            if path.exists(self.font_file):
                remove(self.font_file)
            elif path.islink(self.font_file):
                remove(self.font_file)
            if self.myFont.value != 'default':
                symlink(self.myFont.value, self.font_file)

            if path.exists(self.color_file):
                remove(self.color_file)
            elif path.islink(self.color_file):
                remove(self.color_file)
            if self.myColorScheme.value != 'default':
                symlink(self.myColorScheme.value, self.color_file)

            self.restartGUI()
        elif(self.skinParts_changed):
            self.restartGUI()
        else:
            self.close()

    def keyYellow(self):
        if (path.exists("/usr/lib/enigma2/python/Plugins/Extensions/AtileHD/plugin.py")):

            if not path.exists("mySkin_off") and path.exists("mySkin"):
                rename("mySkin", "mySkin_off")

            if not path.exists("mySkin") and path.exists("mySkin_off"):
                symlink("mySkin_off", "mySkin")

            # Atile_HD_Config Screen öffnen
            from Plugins.Extensions.AtileHD.plugin import *
            self.session.openWithCallback(
                self.AtileHDScreenResponse, AtileHDScreens)
        else:
            msg = _(
                "Sorry, but the plugin %s is not installed at your Vu+ STB! Please install it to use this function") % "AtileHD"
            self.session.open(MessageBox, msg, MessageBox.TYPE_ERROR)

    def keyBlue(self):
        # Updater ausführen
        MetrixReloadedUpdater(self.session, True)

    def keyOK(self):
        if (self['config'].getCurrent()[1] == config.plugins.MetrixReloaded.logDirectory):
            # FileDirBrowser bei Click 'ok' ausführen
            start_dir = config.plugins.MetrixReloaded.logDirectory.value
            self.session.openWithCallback(self.fileDirBrowserResponse, FileDirBrowser, initDir=start_dir, title=_(
                "Choose folder"), getFile=False, getDir=True, showDirectories=True, showFiles=False)

        if (self['config'].getCurrent()[1] == config.plugins.MetrixReloaded.posterDirectory):
            # FileDirBrowser bei Click 'ok' ausführen
            start_dir = config.plugins.MetrixReloaded.posterDirectory.value
            self.session.openWithCallback(self.fileDirBrowserResponse, FileDirBrowser, initDir=start_dir, title=_(
                "Choose folder"), getFile=False, getDir=True, showDirectories=True, showFiles=False)
        
        # if (self['config'].getCurrent()[1] == config.plugins.MetrixReloaded.openConverter):
        #     self.session.open(OpenConverterSetup)

    def showMsgBoxCancelConfirm(self):
        self.session.openWithCallback(
            self.cancelConfirm,
            MessageBox,
            _("Really close without saving settings?")
        )

    def fileDirBrowserResponse(self, path):
        if path:
            # Antwort vom FileDirBrowser -> ausgewähltes Verzeichnis
            self["config"].getCurrent()[1].value = path + '/'

    def restartGUI(self):
        # Fragen ob Restart
        restartbox = self.session.openWithCallback(self.msgBoxResponseRestart, MessageBox, _(
            "Restart necessary, restart GUI now?"), MessageBox.TYPE_YESNO)

    def msgBoxResponseRestart(self, answer):
        if (answer):
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close()

    def updateHelp(self):
        # Zusatzinfos anzeigen
        cur = self["config"].getCurrent()
        if cur and len(cur) > 2:
            self["help"].text = cur[2]
        else:
            self["help"].text = ""

    def getPossibleColor(self):
        color_list = []
        for f in sorted(listdir(self.skin_base_dir), key=str.lower):
            search_str = 'colors_'
            if f.endswith('.xml') and f.startswith(search_str):
                friendly_name = f.replace(search_str, "")
                friendly_name = friendly_name.replace(".xml", "")
                friendly_name = friendly_name.replace("_", " ")
                color_list.append((f, friendly_name))
        return color_list

    def getPossibleFont(self):
        font_list = []
        for f in sorted(listdir(self.skin_base_dir), key=str.lower):
            search_str = 'font_'
            if f.endswith('.xml') and f.startswith(search_str):
                friendly_name = f.replace(search_str, "")
                friendly_name = friendly_name.replace(".xml", "")
                friendly_name = friendly_name.replace("_", " ")
                font_list.append((f, friendly_name))
        return font_list

    def getCurrentColor(self):
        myfile = self.skin_base_dir + self.color_file
        if not path.exists(myfile):
            if path.exists(self.skin_base_dir + self.default_color_file):
                if path.islink(myfile):
                    remove(myfile)
                chdir(self.skin_base_dir)
                symlink(self.default_color_file, self.color_file)
            else:
                return None
        filename = path.realpath(myfile)
        filename = path.basename(filename)

        search_str = 'colors_'
        friendly_name = filename.replace(search_str, "")
        friendly_name = friendly_name.replace(".xml", "")
        friendly_name = friendly_name.replace("_", " ")
        return (filename, friendly_name)

    def getCurrentFont(self):
        myfile = self.skin_base_dir + self.font_file
        if not path.exists(myfile):
            if path.exists(self.skin_base_dir + self.default_font_file):
                if path.islink(myfile):
                    remove(myfile)
                chdir(self.skin_base_dir)
                symlink(self.default_font_file, self.font_file)
            else:
                return None
        filename = path.realpath(myfile)
        filename = path.basename(filename)

        search_str = 'font_'
        friendly_name = filename.replace(search_str, "")
        friendly_name = friendly_name.replace(".xml", "")
        friendly_name = friendly_name.replace("_", " ")
        return (filename, friendly_name)

    def setPicture(self, f, type):
        if(f == "default"):
            if(type == self.TYPE_COLOR):
                pic = "colors_Default.png"
            else:
                pic = "font_Default.png"
        else:
            pic = f.replace(".xml", ".png")

        preview = self.skin_base_dir + "preview/preview_" + pic
        if path.exists(preview):
            self["Picture"].instance.setPixmapFromFile(preview)
            self["Picture"].show()
        else:
            self["Picture"].hide()

    def AtileHDScreenResponse(self):
        self.skinParts_changed = True

    def changed(self):
        # Änderungen in der Liste übernehmen
        if self["config"].getCurrent() == self.set_color:
            self.setPicture(self.myColorScheme.value, self.TYPE_COLOR)
        elif self["config"].getCurrent() == self.set_font:
            self.setPicture(self.myFont.value, self.TYPE_FONT)
        elif self["config"].getCurrent() == self.checkForUpdates:
            self.generateList()
        elif self["config"].getCurrent() == self.onlineMode:
            self.generateList()
        elif self["config"].getCurrent() == self.posterDownload:
            self.generateList()

        for x in self.onChangedEntry:
            try:
                x()
            except Exception:
                pass
