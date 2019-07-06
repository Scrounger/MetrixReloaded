# -*- coding: utf-8 -*-
from Components.config import config, ConfigSubsection, ConfigOnOff, ConfigDirectory, ConfigNumber, ConfigSelection, ConfigNothing

from MetrixReloadedTranslation import _


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
config.plugins.MetrixReloaded.updated = ConfigOnOff(default=True)
config.plugins.MetrixReloaded.openConverter = ConfigNothing()


def getPosterDircetory():
    return config.plugins.MetrixReloaded.posterDirectory.value

def getPosterAutoRemove():
    return config.plugins.MetrixReloaded.posterAutoRemove.value

def getLogDirectory():
    return config.plugins.MetrixReloaded.logDirectory.value

def getLogAutoRemove():
    return config.plugins.MetrixReloaded.logAutoRemove.value


def logConfig(logger):
    logger.debug("")

    dic = config.plugins.MetrixReloaded.content
    for key in dic.items.keys():
        if(dic.items[key].__class__.__name__ != "ConfigNothing"):
            logger.debug("{config} %s %s", key.ljust(40), dic.items[key].value)

    logger.debug("")
