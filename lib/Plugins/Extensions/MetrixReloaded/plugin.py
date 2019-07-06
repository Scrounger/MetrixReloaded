# -*- coding: utf-8 -*-
import os
import logging
from threading import Thread
from time import sleep

from Components.config import config
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox

# Screens für Mods
from Screens.EventView import EventViewBase


import MetrixReloadedSetup
import MetrixReloadedConfig
from MetrixReloadedTranslation import _
import MetrixReloadedHelper as myHelper
from MetrixReloadedUpdater import MetrixReloadedUpdater
from MyScreens import MetrixReloadedEventView
from Tools.MetrixReloadedHelper import createPosterPaths, removePosters, removeLogs, initializeLog

session = None

# MyLog
log = initializeLog("Plugin")
log.info("")
log.info("VU+ startUp --------------------------------------------------------")
log.info("verison: %s", myHelper.getVersion())


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
            session = kwargs.get("session")
            config.misc.standbyCounter.addNotifier(
                onEnterStandby, initial_call=False)

            MetrixReloadedConfig.logConfig(log)

            myHelper.createPosterPaths()
            myHelper.removePosters()
            myHelper.removeLogs()

            # auf anderem Thread damit sleep nicht blockt
            Thread(target=checkNewVersion, args=(session,)).start()

            if(config.plugins.MetrixReloaded.updated.value):
                Thread(target=newVersionInstalled, args=(session,)).start()

        elif reason == 1:
            log.debug(
                "VU+ shutdown / restart --------------------------------------------------------")
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
                log.debug("checkNewVersion: waiting")
                sleep(30)
                log.info("checkNewVersion: Call new version check")
                MetrixReloadedUpdater(session)
            except Exception as e:
                log.exception("checkNewVersion: %s", str(e))
        else:
            log.info("checkNewVersion: %s" % str(
                config.plugins.MetrixReloaded.checkNewVersionOnStartUp.value))
    else:
        log.debug("Primary skin is not MetrixReloaded")


def newVersionInstalled(session):
    if("MetrixReloaded" in config.skin.primary_skin.value):
        try:
            log.debug("newVersionInstalled: waiting")
            sleep(200)
            log.info("newVersionInstalled: load info screen")

            msg = _("MetrixReloaded has been successfully updated to version %s\n\nYou like the MetrixReloaded Skin?\n\nThen support the development in which you actively cooperate. All information can be found under the following link\nhttps://github.com/Scrounger/MetrixReloaded\n\nOr support the MetrixReloaded team with a small donation\n- by Paypal to:\tscrounger@gmx.net\n- via the website:\thttps://github.com/Scrounger/MetrixReloaded\n\nHave fun!\nYour MetrixReloaded Team")
            msg = msg % myHelper.getVersion()

            session.open(
                MessageBox, msg, MessageBox.TYPE_INFO)

            config.plugins.MetrixReloaded.updated.value = False
            config.plugins.MetrixReloaded.updated.save()

        except Exception as e:
            log.exception("newVersionInstalled: %s", str(e))


if("MetrixReloaded" in config.skin.primary_skin.value):
    try:
        # Screen EventView Mod
        log.info("Initialize Screen Mod for 'EventView'")
        EventViewBase.__init__ = MetrixReloadedEventView.init_new
        EventViewBase.setService = MetrixReloadedEventView.setService
        EventViewBase.setEvent = MetrixReloadedEventView.setEvent

    except Exception as e:
        log.exception("%s", str(e))
