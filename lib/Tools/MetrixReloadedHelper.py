# -*- coding: utf-8 -*-
from Components.Sources.Event import Event
from Components.Sources.ExtEvent import ExtEvent
from Components.Sources.extEventInfo import extEventInfo
from ServiceReference import ServiceReference
from Components.config import config
from enigma import iPlayableServicePtr
from ServiceReference import ServiceReference

from Tools.Alternatives import GetWithAlternative

import json
import os
import time
import base64
import logging
import socket


def getExtraData(source, logger, logPrefix=""):
    if source.event:
        if type(source) == ExtEvent:
            try:
                starttime = source.event.getBeginTime()
                title = source.event.getEventName()

                return json.dumps(getDataFromDatabase(str(source.service), str(source.event.getEventId()), logger, logPrefix, starttime, title))
            except Exception as ex:
                logger.exception("%sgetExtraData (1): %s", logPrefix, str(ex))
                return "Error1: %s" % str(ex)
        elif str(type(source)) == "<class 'Components.Sources.extEventInfo.extEventInfo'>":
            try:
                return json.dumps(getDataFromDatabase(str(source.service), str(source.eventid), logger, logPrefix))
            except Exception as ex:
                logger.exception("%sgetExtraData (2): %s", logPrefix, str(ex))
                return "Error2: %s" % str(ex)
        elif hasattr(source, 'service'):
            try:
                service = source.getCurrentService()
                servicereference = ServiceReference(service)
                return json.dumps(getDataFromDatabase(str(servicereference), str(source.event.getEventId()), logger, logPrefix))
            except Exception as ex:
                logger.exception("%sgetExtraData (3): %s", logPrefix, str(ex))
                return "Error3: %s" % str(ex)
        elif type(source) == Event:
            return source.event.getExtraEventData()
    return ""


def getDataFromDatabase(service, eventid, logger, logPrefix="", beginTime=None, EventName=None):
    try:
        from Plugins.Extensions.EpgShare.main import getEPGDB
        data = None
        if "::" in str(service):
            service = service.split("::")[0] + ":"
        if "http" in str(service):
            service = service.split("http")[0]

        # Bug Fix, if channel has alternatives
        if str(service).startswith("1:134"):
            service = GetWithAlternative(str(service))

        if not "1:0:0:0:0:0:0:0:0:0:" in service and not "4097:0:0:0:0:0:0:0:0:0:" in service:
            if beginTime and EventName:
                queryPara = "ref: %s, eventId: %s, title:: %s, beginTime: %s" % (str(service), str(
                    eventid), str(EventName.lower()).decode("utf-8"), str(int(beginTime)))
                logger.debug("%sgetDataFromDatabase: %s", logPrefix, queryPara)

                data = getEPGDB().selectSQL("SELECT * FROM epg_extradata WHERE ref = ? AND (eventid = ? or (LOWER(title) = ? and airtime BETWEEN ? AND ?))",
                                            [str(service), str(eventid), str(EventName.lower()).decode("utf-8"), str(int(beginTime) - 120), str(int(beginTime) + 120)])
            else:
                queryPara = "ref: %s, eventId: %s" % (
                    str(service), str(eventid))
                logger.debug("%sgetDataFromDatabase: %s", logPrefix, queryPara)

                data = getEPGDB().selectSQL("SELECT * FROM epg_extradata WHERE ref = ? AND eventid = ?",
                                            [str(service), str(eventid)])
            if data and len(data) > 0:
                return data[0]
            else:
                return None
        else:
            return None
    except Exception as ex:
        logger.exception("%sgetDataFromDatabase: %s", logPrefix, str(ex))
        return None


def getEventImage(self, timestamp, eventId, logger, logPrefix="", withSize=False, existCheck=False):
    # FileName für Image aus EpgShare Download Folder zurück geben
    try:
        path = os.path.join(getEpgShareImagePath(self), str(
            time.strftime('%D', time.localtime(int(timestamp)))).replace('/', '.'))

        size = ''
        if(withSize):
            # Size des Widgets berücksitigen
            size = '_%s_%s' % (str(self.WCover), str(self.HCover))

        imageFileName = '%s/%s%s.jpg' % (path, eventId, size)

        if (os.path.exists(imageFileName)):
            return imageFileName

        if(existCheck):
            # Falls kein size mitgeliefert wird (z.B. bei Converter)
            files = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path, i)) and
                     i.startswith("%s_" % eventId)]

            if(len(files) > 0):
                imageFileName = '%s/%s' % (path, files[0])

                if (os.path.exists(imageFileName)):
                    return imageFileName

    except Exception as e:
        self.log.exception("getEventImage: %s", str(e))

    return None


def getDefaultImage(self, title):
    # FileName für Image aus Default Folder zurückgeben
    try:
        # Image aus Default EpgShare Ordner holen, sofern existiert
        path = '%s/Default/' % (getEpgShareImagePath(self))
        title = title.decode(
            'utf-8').lower().split('(')[0].strip() + '.jpg'

        imageFileName = '%s%s' % (path, base64.b64encode(title))

        if (os.path.exists(imageFileName)):
            return imageFileName

    except Exception as e:
        self.log.exception("getDefaultImage: %s", str(e))

    return None


def getEpgShareImagePath(self):
    try:
        return str(config.plugins.epgShare.autocachelocation.value)
    except Exception as e:
        self.log.exception("getEpgShareImagePath: %s", str(e))

    return None


def getVersion():
    versFile = "/usr/share/enigma2/MetrixReloaded/version.info"
    version = "Error: version file not exist!"

    if (os.path.exists(versFile)):
        pFile = open(versFile, "r")
        for line in pFile:
            version = line.rstrip()
        pFile.close()

    return version


def getChannelName(source):
    service = source.service
    if isinstance(service, iPlayableServicePtr):
        info = service and service.info()
        ref = None
    elif type(source) == ExtEvent:
        ref = service
    elif str(type(source)) == "<class 'Components.Sources.extEventInfo.extEventInfo'>":
        ref = service
    else:  # reference
        info = service and source.info
        ref = service

    try:
        name = ref and info.getName(ref)
    except Exception:
        name = ServiceReference(str(ref)).getServiceName()

    return name.replace('\xc2\x86', '').replace('\xc2\x87', '')


def isconnected(logger, logPrefix="", host='8.8.8.8', port=53, timeout=1):
    try:
        socket.setdefaulttimeout(timeout)
        host = socket.gethostbyname('www.google.com')
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        logger.warn("%s no internet connection!", logPrefix)
        return False


def createPosterPaths():
    dir = os.path.join(getPosterDircetory(), "movies/")
    if not os.path.exists(dir):
        os.makedirs(dir)

    dir = os.path.join(getPosterDircetory(), "series/")
    if not os.path.exists(dir):
        os.makedirs(dir)


def isOnlineMode():
    try:
        return config.plugins.MetrixReloaded.onlineMode.value
    except Exception:
        # falls nicht von MetrixReloaded skin verwendet wird
        return True


def isDownloadPoster():
    try:
        return config.plugins.MetrixReloaded.posterDownload.value
    except Exception:
        # falls nicht von MetrixReloaded skin verwendet wird
        return True


def getPosterDircetory():
    try:
        return config.plugins.MetrixReloaded.posterDirectory.value
    except Exception:
        # falls nicht von MetrixReloaded skin verwendet wird
        dir = '/tmp/MetrixReloaded/poster/movies/'
        if not os.path.exists(dir):
            os.makedirs(dir)

        dir = '/tmp/MetrixReloaded/poster/series/'
        if not os.path.exists(dir):
            os.makedirs(dir)

        return '/tmp/MetrixReloaded/poster/'


def removePosters():
    removeFilesFromPath(getPosterDircetory() + 'series/',
                        config.plugins.MetrixReloaded.posterAutoRemove.value)
    removeFilesFromPath(getPosterDircetory() + 'movies/',
                        config.plugins.MetrixReloaded.posterAutoRemove.value)


def removeLogs():
    removeFilesFromPath(config.plugins.MetrixReloaded.logDirectory.value,
                        config.plugins.MetrixReloaded.logAutoRemove.value)


def removeFilesFromPath(path, days):
    now = time.time()

    for filename in os.listdir(path):
        if os.path.getctime(os.path.join(path, filename)) < now - days * 86400:
            if os.path.isfile(os.path.join(path, filename)):
                print(filename)
                os.remove(os.path.join(path, filename))


def initializeLog(fileName):
    logger = logging.getLogger(fileName)

    if (not len(logger.handlers)):

        debug = True
        try:
            debug = config.plugins.MetrixReloaded.debug.value
        except:
            pass

        if(debug):
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        dir = '/tmp/MetrixReloaded/log/'
        try:
            dir = config.plugins.MetrixReloaded.logDirectory.value
        except:
            pass

        # create a file handler
        if not os.path.exists(dir):
            os.makedirs(dir)

        handler = logging.FileHandler('%s%s.log' % (dir, fileName))

        # create a logging format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s: [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(handler)

    return logger
