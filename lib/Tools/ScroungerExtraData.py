# -*- coding: utf-8 -*-
from Components.Sources.Event import Event
from Components.Sources.ExtEvent import ExtEvent
from Components.Sources.extEventInfo import extEventInfo
from ServiceReference import ServiceReference

import json


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
