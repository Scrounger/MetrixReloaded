# -*- coding: utf-8 -*-
from MetrixReloadedUpdater import MetrixReloadedUpdater
from Tools.MetrixReloadedHelper import initializeLog
from Plugins.Plugin import PluginDescriptor

from threading import Thread
from time import sleep

# Config
from Components.config import config, ConfigSubsection, ConfigOnOff, ConfigDirectory

import os
import logging

import MetrixReloadedSetup
from MyScreens import MetrixReloadedEventView

# Screens für Mods
from Screens.EventView import EventViewBase


# Configuration
config.plugins.MetrixReloaded = ConfigSubsection()
config.plugins.MetrixReloaded.onlineMode = ConfigOnOff(default=True)
config.plugins.MetrixReloaded.checkNewVersionOnStartUp = ConfigOnOff(default=True)
config.plugins.MetrixReloaded.autoDownloadNewVersion = ConfigOnOff(default=True)
config.plugins.MetrixReloaded.debug = ConfigOnOff(default=False)
config.plugins.MetrixReloaded.logDirectory = ConfigDirectory(default='/tmp/MetrixReloaded/log/')
config.plugins.MetrixReloaded.showScreenNames = ConfigOnOff(default=False)
config.plugins.MetrixReloaded.showMenuEntryNames = ConfigOnOff(default=False)

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

			#auf anderem Thread damit sleep nicht blockt
			Thread(target=checkNewVersion, args=(session,)).start()

		elif reason == 1:
			log.debug("VU+ shutdown / restart")
			session=None
	except Exception as e:
		log.exception("MetrixReloadedSetup: %s", str(e))


def onLeaveStandby():
    log.debug("leaving standy")
    if(session != None):
        #auf anderem Thread damit sleep nicht blockt
        Thread(target=checkNewVersion, args=(session,)).start()
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
            log.info("checkNewVersionOnStartUp: %s" %str(config.plugins.MetrixReloaded.checkNewVersionOnStartUp.value))
    else:
        log.debug("Primary skin is not MetrixReloaded")

if("MetrixReloaded" in config.skin.primary_skin.value):
    try:
        # Screen EventView Mod
        log.info("Initialize EventView Mod")
        EventViewBase.__init__ = MetrixReloadedEventView.init_new
        EventViewBase.setService = MetrixReloadedEventView.setService
        EventViewBase.setEvent = MetrixReloadedEventView.setEvent

    except Exception as e:
        log.exception("MetrixReloadedSetup: %s", str(e))
