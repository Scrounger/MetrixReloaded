# -*- coding: utf-8 -*-
from Components.Sources.ExtEvent import ExtEvent

import json	
	
def getDataFromDatabase(self, service, eventid, beginTime=None, EventName= None):
	try:
		from Plugins.Extensions.EpgShare.main import getEPGDB
		data = None
		if "::" in str(service):
			service = service.split("::")[0] + ":"
		if "http" in str(service):
			service = service.split("http")[0]
		if not "1:0:0:0:0:0:0:0:0:0:" in service and not "4097:0:0:0:0:0:0:0:0:0:" in service:
			if beginTime and EventName:
				data = getEPGDB().selectSQL("SELECT * FROM epg_extradata WHERE ref = ? AND (eventid = ? or (LOWER(title) = ? and airtime BETWEEN ? AND ?))", [str(service), str(eventid),str(EventName.lower()).decode("utf-8"), str(int(beginTime) -120), str(int(beginTime) + 120) ])
			else:
				data = getEPGDB().selectSQL("SELECT * FROM epg_extradata WHERE ref = ? AND eventid = ?", [str(service), str(eventid)])
			if data and len(data) > 0:
				return data[0]
			else:
				return None
		else:
			return None
	except Exception, ex:
		print "DB Error: %s" % str(ex)
		return None
	except ImportError, exi:
		print "Import Error: %s" % str(exi)
		return None

def getExtraData(self):
	if self.source.event:
		if type(self.source) == ExtEvent:
			try:
				starttime = self.source.event.getBeginTime()
				title = self.source.event.getEventName()
				return json.dumps(getDataFromDatabase(self, str(self.source.service), str(self.source.event.getEventId()), starttime, title))
			except Exception, ex:
				#self.log.error('getExtraData (1): %s', str(ex))
				return "Error1: %s" % str(ex)
		elif str(type(self.source)) == "<class 'Components.Sources.extEventInfo.extEventInfo'>":
			try:
				return json.dumps(getDataFromDatabase(self, str(self.source.service), str(self.source.eventid)))
			except Exception, ex:
				#self.log.error('getExtraData (2): %s', str(ex))
				return "Error2: %s" % str(ex)
		elif hasattr(self.source, 'service'):
			try:
				service = self.source.getCurrentService()
				servicereference = ServiceReference(service)
				return json.dumps(getDataFromDatabase(self, str(servicereference), str(self.source.event.getEventId())))
			except Exception, ex:
				#self.log.error('getExtraData (2): %s', str(ex))
				return "Error3: %s" % str(ex)
		elif type(self.source) == Event:
			return self.source.event.getExtraEventData()
	return ""