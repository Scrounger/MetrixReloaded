# -*- coding: utf-8 -*-
from Components.Sources.Event import Event
from Components.Sources.ExtEvent import ExtEvent
from Components.Sources.extEventInfo import extEventInfo
from ServiceReference import ServiceReference
from Components.config import config

import json
import os
import time
import base64
import logging

def getExtraData(source, logger):
    if source.event:
        if type(source) == ExtEvent:
            try:
                starttime = source.event.getBeginTime()
                title = source.event.getEventName()
                return json.dumps(getDataFromDatabase(str(source.service), str(source.event.getEventId()), logger, starttime, title))
            except Exception as ex:
                logger.exception("getExtraData (1): %s", str(ex))
                return "Error1: %s" % str(ex)
        elif str(type(source)) == "<class 'Components.Sources.extEventInfo.extEventInfo'>":
            try:
                return json.dumps(getDataFromDatabase(str(source.service), str(source.eventid), logger))
            except Exception as ex:
                logger.exception("getExtraData (2): %s", str(ex))
                return "Error2: %s" % str(ex)
        elif hasattr(source, 'service'):
            try:
                service = source.getCurrentService()
                servicereference = ServiceReference(service)
                return json.dumps(getDataFromDatabase(str(servicereference), str(source.event.getEventId()), logger))
            except Exception as ex:
                logger.exception("getExtraData (3): %s", str(ex))
                return "Error3: %s" % str(ex)
        elif type(source) == Event:
            return source.event.getExtraEventData()
    return ""


def getDataFromDatabase(service, eventid, logger, beginTime=None, EventName=None):
    try:
        from Plugins.Extensions.EpgShare.main import getEPGDB
        data = None
        if "::" in str(service):
            service = service.split("::")[0] + ":"
        if "http" in str(service):
            service = service.split("http")[0]
        if not "1:0:0:0:0:0:0:0:0:0:" in service and not "4097:0:0:0:0:0:0:0:0:0:" in service:
            if beginTime and EventName:
                data = getEPGDB().selectSQL("SELECT * FROM epg_extradata WHERE ref = ? AND (eventid = ? or (LOWER(title) = ? and airtime BETWEEN ? AND ?))",
                                            [str(service), str(eventid), str(EventName.lower()).decode("utf-8"), str(int(beginTime) - 120), str(int(beginTime) + 120)])
            else:
                data = getEPGDB().selectSQL("SELECT * FROM epg_extradata WHERE ref = ? AND eventid = ?",
                                            [str(service), str(eventid)])
            if data and len(data) > 0:
                return data[0]
            else:
                return None
        else:
            return None
    except Exception as ex:
        logger.exception("getDataFromDatabase: %s", str(ex))
        return None


def getEventImage(self, timestamp, eventId, withSize=False):
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
        pFile = open(versFile,"r")
        for line in pFile:
            version = line.rstrip()
        pFile.close()

    return version

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

        dir = '/mnt/hdd/MetrixReloaded/log/'
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
