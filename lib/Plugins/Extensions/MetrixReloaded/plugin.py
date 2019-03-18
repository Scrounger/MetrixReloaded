# -*- coding: utf-8 -*-
from Plugins.Plugin import PluginDescriptor

# Config
from Components.config import config, ConfigSubsection, ConfigOnOff, ConfigDirectory

import os
import logging

import MetrixReloadedSetup

#Configuration
config.plugins.MetrixReloaded = ConfigSubsection()
config.plugins.MetrixReloaded.onlineMode = ConfigOnOff(default = True)
config.plugins.MetrixReloaded.debug = ConfigOnOff(default = False)
config.plugins.MetrixReloaded.logDirectory = ConfigDirectory(default = '/tmp/MetrixReloaded/log/')

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
	log = initializeLog()

	if kwargs.has_key("session") and reason == 0:
		log.info("startUp")
		config.misc.standbyCounter.addNotifier(onEnterStandby, initial_call = False)
	elif reason == 1:
		log.info("shutdown / restart")

def onLeaveStandby():
    log = initializeLog()
    log.info("leaving standy")

def onEnterStandby(self):
	log = initializeLog()
	log.info("enter standy")
	from Screens.Standby import inStandby
	inStandby.onClose.append(onLeaveStandby)		

def initializeLog():
	logger = logging.getLogger("Plugin")
	logger.setLevel(logging.DEBUG)

	# create a file handler
	dir = '/mnt/hdd/MetrixReloaded/log/'

	if not os.path.exists(dir):
		os.makedirs(dir)

	handler = logging.FileHandler('%sPlugin.log' % (dir))
	handler.setLevel(logging.DEBUG)

	# create a logging format
	formatter = logging.Formatter('%(asctime)s - %(name)s: [%(levelname)s] %(message)s')
	handler.setFormatter(formatter)

	# add the handlers to the logger
	logger.addHandler(handler)
		
	return logger
