# -*- coding: utf-8 -*-
from Screens.ChoiceBox import ChoiceBox
from Screens.TimerEdit import TimerSanityConflict, TimerEditList
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap, HelpableActionMap
from Components.Button import Button
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.TimerList import TimerList
from Components.UsageConfig import preferredTimerPath
from enigma import eEPGCache, eTimer, eServiceReference
from RecordTimer import RecordTimerEntry, parseEvent, AFTEREVENT
from time import localtime
import Tools.AutoTimerHook as AutoTimerHook
from Components.Sources.ExtEvent import ExtEvent
from Components.Sources.ServiceEvent import ServiceEvent

from Tools.MetrixReloadedHelper import initializeLog


def init_new(self, Event, Ref, callback=None, similarEPGCB=None):

    self.log = initializeLog("MetrixReloadedEventView")

    self.log.info("Jaaaa Man")

    if not AutoTimerHook.CHECKAUTOTIMER:
        AutoTimerHook.initAutoTimerGlobals()
    self.screentitle = _("Eventview")
    self.similarEPGCB = similarEPGCB
    self.cbFunc = callback
    self.currentService = Ref
    path = Ref.ref.getPath()
    self.isRecording = (not Ref.ref.flags &
                        eServiceReference.isGroup) and path
    if path.find('://') != -1:
        self.isRecording = None
    self.event = Event
    self["epg_description"] = ScrollLabel()
    self["datetime"] = Label()
    self["channel"] = Label()
    self["duration"] = Label()
    self["key_red"] = Button("")

    # Mod by Scrounger
    self["ExtEvent"] = ExtEvent()
    self["Service"] = ServiceEvent()

    if similarEPGCB is not None:
        self.SimilarBroadcastTimer = eTimer()
        self.SimilarBroadcastTimer.callback.append(
            self.getSimilarEvents)
    else:
        self.SimilarBroadcastTimer = None
    self.key_green_choice = self.ADD_TIMER
    if self.isRecording:
        self["key_green"] = Button("")
    else:
        self["key_green"] = Button(_("Add timer"))
    self["key_yellow"] = Button("")
    self["key_blue"] = Button("")
    self["actions"] = ActionMap(["OkCancelActions", "EventViewActions"],
                                {
        "cancel": self.close,
        "ok": self.close,
        "pageUp": self.pageUp,
        "pageDown": self.pageDown,
        "prevEvent": self.prevEvent,
        "nextEvent": self.nextEvent,
        "timerAdd": self.timerAdd,
        "instantTimer": self.addInstantTimer,
        "openSimilarList": self.openSimilarList
    })

    self["menu_actions"] = HelpableActionMap(self, "MenuActions", {
        "menu": (self.menuClicked, _("Setup")),
    }, -2)

    self.onShown.append(self.onCreate)


def setService(self, service):
    self.currentService = service
    if self.isRecording:
        self["channel"].setText(_("Recording"))
    else:
        name = self.currentService.getServiceName()
        if name is not None:
            self["channel"].setText(name)
        else:
            self["channel"].setText(_("unknown service"))

    # Mod by Scrounger
    self["Service"].newService(service.ref)


def setEvent(self, event):
    self.event = event
    if event is None:
        return
    text = event.getEventName()
    short = event.getShortDescription()
    ext = event.getExtendedDescription()
    if short and short != text:
        text += '\n\n' + short
    if ext:
        if text:
            text += '\n\n'
        text += ext

    if not "epg_description" in self:
        return
    self["epg_description"].setText(text)
    self["datetime"].setText(event.getBeginTimeString())
    self["duration"].setText(_("%d min") % (event.getDuration()/60))
    self["key_red"].setText("")
    if self.SimilarBroadcastTimer is not None:
        self.SimilarBroadcastTimer.start(400, True)

    serviceref = self.currentService
    eventid = self.event.getEventId()
    refstr = serviceref.ref.toString()
    isRecordEvent = False
    for timer in self.session.nav.RecordTimer.timer_list:
        if timer.eit == eventid and timer.service_ref.ref.toString() == refstr:
            isRecordEvent = True
            break
    if isRecordEvent and self.key_green_choice != self.REMOVE_TIMER:
        self["key_green"].setText(_("Remove timer"))
        self.key_green_choice = self.REMOVE_TIMER
    elif not isRecordEvent and self.key_green_choice != self.ADD_TIMER:
        self["key_green"].setText(_("Add timer"))
        self.key_green_choice = self.ADD_TIMER

    # Mod by Scrounger
    self["ExtEvent"].newEvent(event)
    self["ExtEvent"].newService(serviceref)
