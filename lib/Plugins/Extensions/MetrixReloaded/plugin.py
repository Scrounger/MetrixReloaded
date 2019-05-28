# -*- coding: utf-8 -*-
from MetrixReloadedUpdater import MetrixReloadedUpdater
from Tools.MetrixReloadedHelper import initializeLog, getVersion
from Plugins.Plugin import PluginDescriptor

from threading import Thread
from time import sleep

# Config
from Components.config import config, ConfigSubsection, ConfigOnOff, ConfigDirectory, ConfigNumber
from Screens.MessageBox import MessageBox

import os
import logging

import MetrixReloadedSetup
from MyScreens import MetrixReloadedEventView
from Tools.MetrixReloadedHelper import createPosterPaths, removePosters, removeLogs

# Screens für Mods
from Screens.EventView import EventViewBase


# Configuration
config.plugins.MetrixReloaded = ConfigSubsection()
config.plugins.MetrixReloaded.onlineMode = ConfigOnOff(default=True)
config.plugins.MetrixReloaded.checkNewVersionOnStartUp = ConfigOnOff(
    default=True)
config.plugins.MetrixReloaded.autoDownloadNewVersion = ConfigOnOff(
    default=True)
config.plugins.MetrixReloaded.debug = ConfigOnOff(default=False)
config.plugins.MetrixReloaded.logDirectory = ConfigDirectory(
    default='/mnt/hdd/MetrixReloaded/log/')
config.plugins.MetrixReloaded.logAutoRemove = ConfigNumber(default=10)
config.plugins.MetrixReloaded.showScreenNames = ConfigOnOff(default=False)
config.plugins.MetrixReloaded.showMenuEntryNames = ConfigOnOff(default=False)
config.plugins.MetrixReloaded.posterDownload = ConfigOnOff(default=True)
config.plugins.MetrixReloaded.posterDirectory = ConfigDirectory(
    default='/mnt/hdd/MetrixReloaded/poster/')
config.plugins.MetrixReloaded.posterAutoRemove = ConfigNumber(default=30)
config.plugins.MetrixReloaded.updated = ConfigOnOff(default=False)

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

# MyLog
# MyLog
log = initializeLog("Plugin")

session = None


def Plugins(**kwargs):
    return [PluginDescriptor(
            name="MetrixReloaded",
            description="MetrixReloaded Skin Einstellungen",
            where=PluginDescriptor.WHERE_PLUGINMENU,
            fnc=main
            ),
            PluginDescriptor(
            name="MetrixReloaded",
            description="MetrixReloaded Skin Einstellungen",
            where=[
                PluginDescriptor.WHERE_AUTOSTART,
                PluginDescriptor.WHERE_SESSIONSTART
            ],
            fnc=autoStart
            ),
            ]


def main(session, **kwargs):
    reload(MetrixReloadedSetup)
    try:
        session.open(MetrixReloadedSetup.MetrixReloadedSetup)
    except Exception as e:
        import traceback
        traceback.print_exc()


def autoStart(reason, **kwargs):
    try:
        global session
        if kwargs.has_key("session") and reason == 0:
            log.info("VU+ startUp")
            session = kwargs.get("session")
            config.misc.standbyCounter.addNotifier(
                onEnterStandby, initial_call=False)

            createPosterPaths()
            removePosters()
            removeLogs()

            # auf anderem Thread damit sleep nicht blockt
            Thread(target=checkNewVersion, args=(session,)).start()

            if(config.plugins.MetrixReloaded.updated.value):
                Thread(target=newVersionInstalled, args=(session,)).start()

        elif reason == 1:
            log.debug("VU+ shutdown / restart")
            session = None
    except Exception as e:
        log.exception("MetrixReloadedSetup: %s", str(e))


def onLeaveStandby():
    log.debug("leaving standy")
    if(session != None):
        createPosterPaths()
        removePosters()
        removeLogs()

        # auf anderem Thread damit sleep nicht blockt
        Thread(target=checkNewVersion, args=(session,)).start()

        if(config.plugins.MetrixReloaded.updated.value):
            Thread(target=newVersionInstalled, args=(session,)).start()
    else:
        log.debug("no session!")


def onEnterStandby(self):
    log.debug("enter standy")
    from Screens.Standby import inStandby
    inStandby.onClose.append(onLeaveStandby)


def checkNewVersion(session):
    # Updater verzögert ausführen
    if("MetrixReloaded" in config.skin.primary_skin.value):
        if(config.plugins.MetrixReloaded.checkNewVersionOnStartUp.value == True):
            try:
                log.debug("waiting")
                sleep(30)
                log.info("Call new version check")
                MetrixReloadedUpdater(session)
            except Exception as e:
                log.exception("MetrixReloadedSetup: %s", str(e))
        else:
            log.info("checkNewVersionOnStartUp: %s" % str(
                config.plugins.MetrixReloaded.checkNewVersionOnStartUp.value))
    else:
        log.debug("Primary skin is not MetrixReloaded")


def newVersionInstalled(session):
    if("MetrixReloaded" in config.skin.primary_skin.value):
        try:
            log.debug("waiting")
            sleep(200)
            log.info("new version installed")

            msg = _("MetrixReloaded has been successfully updated to version %s\n\nYou like the MetrixReloaded Skin?\n\nThen support the development in which you actively cooperate. All information can be found under the following link\nhttps://github.com/Scrounger/MetrixReloaded\n\nOr support the MetrixReloaded team with a small donation\n- by Paypal to:\tscrounger@gmx.net\n- via the website:\thttps://github.com/Scrounger/MetrixReloaded\n\nHave fun!\nYour MetrixReloaded Team")
            msg = msg % getVersion()

            session.open(
                MessageBox, msg, MessageBox.TYPE_INFO, timeout=60)

            config.plugins.MetrixReloaded.updated.value = False
            config.plugins.MetrixReloaded.updated.save()

        except Exception as e:
            log.exception("newVersionInstalled: %s", str(e))


if("MetrixReloaded" in config.skin.primary_skin.value):
    try:
        # Screen EventView Mod
        log.info("Initialize EventView Mod")
        EventViewBase.__init__ = MetrixReloadedEventView.init_new
        EventViewBase.setService = MetrixReloadedEventView.setService
        EventViewBase.setEvent = MetrixReloadedEventView.setEvent

    except Exception as e:
        log.exception("MetrixReloadedSetup: %s", str(e))
