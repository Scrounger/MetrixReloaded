# -*- coding: utf-8 -*-

# GUI (Screens)
from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Screens.MessageBox import MessageBox
from Screens.FileDirBrowser import FileDirBrowser
from Screens.Standby import TryQuitMainloop

# Configuration
from Components.config import config, getConfigListEntry, NoSave, ConfigNothing, ConfigSelection

# GUI (Components)
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Pixmap import Pixmap

from twisted.web.client import downloadPage, getPage

from os import listdir, remove, rename, system, path, symlink, chdir, makedirs
import HTMLParser

# MetrixReloaded imports
from MetrixReloadedUpdater import MetrixReloadedUpdater
from Tools.MetrixReloadedHelper import initializeLog, getVersion


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


cur_skin = config.skin.primary_skin.value.replace('/skin.xml', '')


class MetrixReloadedSetup(Screen, ConfigListScreen):
    htmlParser = HTMLParser.HTMLParser()

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

            self.set_color = getConfigListEntry(self.htmlParser.unescape(_("  &#8226;  Color scheme:")), self.myColorScheme, _("Choose your color scheme")) 

            self.list = [
                getConfigListEntry(
                    _("skin options -------------------------------------------------------------------------------------------------------------"), NoSave(ConfigNothing())),
                self.set_color,
                getConfigListEntry(self.htmlParser.unescape(_("  &#8226;  Download additional data")), config.plugins.MetrixReloaded.onlineMode, _(
                    "Download additional data such as images. Requires internet connection!")),
                getConfigListEntry(self.htmlParser.unescape(_("  &#8226;  Check for skin update on startup")), config.plugins.MetrixReloaded.checkNewVersionOnStartUp, _(
                    "Checks on startup (boot or standby) if a new skin version is available to download. Requires internet connection!")),
                getConfigListEntry(self.htmlParser.unescape(_("  &#8226;  Auto download new version")), config.plugins.MetrixReloaded.autoDownloadNewVersion, _(
                    "New version of MetrixReloaded skin will be automatically downloaded. You will get an information if new version is ready to install")),
                getConfigListEntry("",NoSave(ConfigNothing())),
                getConfigListEntry(
                    _("debug options -------------------------------------------------------------------------------------------------------------"), NoSave(ConfigNothing())),
                getConfigListEntry(self.htmlParser.unescape(_("  &#8226;  enable debug")),
                                   config.plugins.MetrixReloaded.debug, _("show additional log informations")),
                getConfigListEntry(self.htmlParser.unescape(_("  &#8226;  log files directory")), config.plugins.MetrixReloaded.logDirectory, _(
                    "choose the directory where log files of skin, components, etc are stored")),
                getConfigListEntry("",NoSave(ConfigNothing())),
                getConfigListEntry(
                    _("developer options -------------------------------------------------------------------------------------------------------------"), NoSave(ConfigNothing())),
                getConfigListEntry(self.htmlParser.unescape(_("  &#8226;  show screen names")), config.plugins.MetrixReloaded.showScreenNames, _(
                    "Shows the name of the current screen in the bottom right corner")),
                getConfigListEntry(self.htmlParser.unescape(_("  &#8226;  show selected menu entry name")), config.plugins.MetrixReloaded.showMenuEntryNames, _(
                    "Shows the name of the current selected menu entry")),
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
                
                if self["config"].getCurrent() == self.set_color:
                    self.setPicture(self.myColorScheme.value)
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

            self["Picture"] = Pixmap()

            # Trigger change
            self.changed()

        except Exception as e:
            self.log.exception("MetrixReloadedSetup: %s", str(e))
            self.close()

    def getInitConfig(self):
        self.skin_base_dir = "/usr/share/enigma2/%s/" % cur_skin
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
                symlink("mySkin_off","mySkin")

            # Atile_HD_Config Screen öffnen
            from Plugins.Extensions.AtileHD.plugin import *
            self.session.openWithCallback(self.AtileHDScreenResponse, AtileHDScreens)
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
        restartbox = self.session.openWithCallback(self.msgBoxResponseRestart,MessageBox,_("Restart necessary, restart GUI now?"), MessageBox.TYPE_YESNO)

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

    def setPicture(self, f):
        if(f == "default"):
            pic= "colors_Default.png"
        else:
            pic = f.replace(".xml", ".png")
        
        preview = self.skin_base_dir + "preview/preview_" + pic
        self.log.debug(preview)
        if path.exists(preview):
            self.log.debug(preview)
            self["Picture"].instance.setPixmapFromFile(preview)
            self["Picture"].show()
        else:
            self["Picture"].hide()

    def AtileHDScreenResponse(self):
        self.skinParts_changed = True

    def changed(self):
        # Änderungen in der Liste übernehmen
        if self["config"].getCurrent() == self.set_color:
            self.setPicture(self.myColorScheme.value)
        for x in self.onChangedEntry:
            try:
                x()
            except Exception:
                pass