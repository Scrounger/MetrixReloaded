# -*- coding: utf-8 -*-
import os
import time

import MetrixReloadedConfig as myConfig


def getVersion():
    grepcommand = 'opkg list-installed | grep enigma2-plugin-skin-metrixreloaded | cut -d " " -f 3'
    out = os.popen(grepcommand).readlines()
    try:
        return str(out[0]).strip()
    except:
        return str(out).strip()


def createPosterPaths():
    dir = myConfig.getPosterDircetory()
    if not os.path.exists(dir):
        os.makedirs(dir)


def removePosters():
    removeFilesFromPath(myConfig.getPosterDircetory(),
                        myConfig.getPosterAutoRemove())


def removeLogs():
    removeFilesFromPath(myConfig.getLogDirectory(),
                        myConfig.getLogAutoRemove())


def removeFilesFromPath(path, days):
    now = time.time()

    for filename in os.listdir(path):
        if os.path.getctime(os.path.join(path, filename)) < now - days * 86400:
            if os.path.isfile(os.path.join(path, filename)):
                print(filename)
                os.remove(os.path.join(path, filename))
