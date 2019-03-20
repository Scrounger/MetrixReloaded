# -*- coding: utf-8 -*-
from MetrixReloadedUpdater import MetrixReloadedUpdater
from Tools.MetrixReloadedHelper import initializeLog
from Plugins.Plugin import PluginDescriptor

# Config
from Components.config import config, ConfigSubsection, ConfigOnOff, ConfigDirectory

import os
import logging

import MetrixReloadedSetup

# Configuration
config.plugins.MetrixReloaded = ConfigSubsection()
config.plugins.MetrixReloaded.onlineMode = ConfigOnOff(default=True)
config.plugins.MetrixReloaded.autoDownloadNewVersion = ConfigOnOff(
    default=True)
config.plugins.MetrixReloaded.debug = ConfigOnOff(default=False)
config.plugins.MetrixReloaded.logDirectory = ConfigDirectory(
    default='/tmp/MetrixReloaded/log/')

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
    if kwargs.has_key("session") and reason == 0:
        log.debug("startUp")
        session = kwargs.get("session")
        config.misc.standbyCounter.addNotifier(
            onEnterStandby, initial_call=False)

        checkNewVersion(session)

    elif reason == 1:
        log.debug("shutdown / restart")
        session = None


def onLeaveStandby():
    log.debug("leaving standy")
    if(session != None):
        checkNewVersion(session)
    else:
        log.debug("keine session!")


def onEnterStandby(self):
    log.debug("enter standy")
    from Screens.Standby import inStandby
    inStandby.onClose.append(onLeaveStandby)


def checkNewVersion(session):
    # Updater ausführen
    log.info("Call new version check")
    MetrixReloadedUpdater(session)
