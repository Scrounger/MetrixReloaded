from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Sources.Event import Event
from Components.Sources.ExtEvent import ExtEvent
from Components.Sources.extEventInfo import extEventInfo
from Components.Sources.ServiceEvent import ServiceEvent
from Tools.MovieInfoParser import getExtendedMovieDescription
from Plugins.Extensions.FluidNextSetup.fluidnext import get_Extradata
from ServiceReference import ServiceReference
import json

class ScroungerExtEventName(Converter, object):
    NAME = 0
    SHORT_DESCRIPTION = 1
    EXTENDED_DESCRIPTION = 2
    ID = 3
    FULL_DESCRIPTION = 4
    EVENT_EXTRADATA = 5
    EPG_SOURCE = 6

    def __init__(self, type):
        Converter.__init__(self, type)
        self.type = self.EVENT_EXTRADATA

    @cached
    def getText(self):
        if self.source.event:
            event = None
            try:
                event = self.source.event[0]
            except:
                pass

            if event is None or self.type == self.EVENT_EXTRADATA:
                if hasattr(self.source, 'service') and (self.type == self.EXTENDED_DESCRIPTION or self.type == self.FULL_DESCRIPTION):
                    service = self.source.service
                    if service:
                        ret = getExtendedMovieDescription(service)
                        return ret[1]
                elif self.type == self.NAME and hasattr(self.source, 'service'):
                    service = self.source.getCurrentService()
                    if service:
                        if isinstance(service, basestring):
                            sname = service.split('/')[-1].rsplit('.', 1)[0].replace('_', ' ')
                        else:
                            sname = service.getPath().split('/')[-1].rsplit('.', 1)[0].replace('_', ' ')
                        return sname
                elif type(self.source) == ExtEvent:
                    if self.type == self.ID:
                        return str(self.source.event.getEventId())
                    try:
                        starttime = self.source.event.getBeginTime()
                        title = self.source.event.getEventName()
                        return get_Extradata(str(self.source.service), str(self.source.event.getEventId()), starttime, title)
                    except Exception as ex:
                        return ''

                elif str(type(self.source)) == "<class 'Components.Sources.extEventInfo.extEventInfo'>":
                    if self.type == self.ID:
                        return str(self.source.eventid)
                    else:
                        return self.source.extradata
                elif hasattr(self.source, 'service') and self.type == self.EVENT_EXTRADATA:
                    try:
                        service = self.source.getCurrentService()
                        servicereference = ServiceReference(service)
                        return get_Extradata(str(servicereference), str(self.source.event.getEventId()))
                    except Exception as ex:
                        return ''

                elif type(self.source) == Event:
                    if self.type == self.ID:
                        return str(self.source.event.getEventId())
                    else:
                        return self.source.event.getExtraEventData()
                return ''
            ret = ''
            if self.type == self.NAME:
                ret = event.getEventName()
            elif self.type == self.SHORT_DESCRIPTION:
                ret = event.getShortDescription()
            elif self.type == self.EXTENDED_DESCRIPTION:
                ret = event.getExtendedDescription()
            elif self.type == self.FULL_DESCRIPTION:
                ext_desc = event.getExtendedDescription()
                short_desc = event.getShortDescription()
                if short_desc == '':
                    ret = ext_desc
                elif ext_desc == '':
                    ret = short_desc
                else:
                    ret = '%s\n\n%s' % (short_desc, ext_desc)
            elif self.type == self.ID:
                ret = str(event.getEventId())
            elif self.type == self.EVENT_EXTRADATA:
                ret = event.getExtraEventData()
            elif self.type == self.EPG_SOURCE:
                ret = event.getEPGSource()
            return ret
        else:
            return

    text = property(getText)