# -*- coding: utf-8 -*-
import json
import os
import time
import base64
import skin
from Components.config import config
from Components.Sources.Event import Event
from enigma import eLabel, ePixmap, ePoint, eSize, eTimer, eWidget, loadJPG, loadPNG
from PIL import Image
from Renderer import Renderer
from skin import parseColor, parseFont
from twisted.web.client import downloadPage, getPage
from Components.Sources.ExtEvent import ExtEvent
from Components.Sources.ServiceEvent import ServiceEvent
from Tools.ScroungerHelper import getDataFromDatabase, getExtraData, getDefaultImage, getEventImage
import logging


class ScroungerEventImage(Renderer):
    DOWNOAD_IMAGE = "DOWNOAD_IMAGE"
    SHOW_IMAGE = "SHOW_IMAGE"

    def __init__(self):
        Renderer.__init__(self)

        # Log initialisieren
        self.log = self.initializeLog()

        self.eventid = None
        self.downloads = []
        self.name = ''
        self.id = None
        self.picname = ''
        self.imageheight = 0
        self.smallptr = False
        self.labeltop = 0
        self.scaletype = 2
        self.WCover = self.HCover = self.TCover = self.LCover = self.WPreview = self.HPreview = self.TPreview = self.LPreview = 0

        # ImagePath von EpgShare Plugin
        self.epgShareImagePath = str(
            config.plugins.epgShare.autocachelocation.value)

        return

    GUI_WIDGET = eWidget

    def applySkin(self, desktop, screen):
        if self.skinAttributes:
            attribs = []
            for attrib, value in self.skinAttributes:
                if attrib == 'size':
                    attribs.append((attrib, value))
                    x, y = value.split(',')
                    self.WCover, self.HCover = int(x), int(y)
                    self.labeltop = int(self.HCover * 0.64)
                elif attrib == 'foregroundColor':
                    self.fg = parseColor(str(value))
                elif attrib == 'scale':
                    self.scaletype = int(value)
                elif attrib == 'backgroundColor':
                    attribs.append((attrib, value))
                    self.bg = parseColor(str(value))
                else:
                    attribs.append((attrib, value))

            self.skinAttributes = attribs

        self.image.resize(eSize(self.WCover, self.HCover))

        self.labelheight = self.HCover - (10 + self.labeltop)
        self.text.resize(
            eSize(self.WCover, self.HCover - (10 + self.labeltop)))
        self.test_label.resize(
            eSize(self.WCover, self.HCover - (10 + self.labeltop)))
        self.text.move(ePoint(0, self.labeltop + 10))

        self.text.setVAlign(eLabel.alignTop)
        self.test_label.setVAlign(eLabel.alignTop)
        self.text.setHAlign(eLabel.alignCenter)
        self.test_label.setHAlign(eLabel.alignCenter)
        self.test_label.setNoWrap(0)
        self.test_label.hide()
        self.text.setBackgroundColor(self.bg)
        self.text.setForegroundColor(self.fg)
        self.text.setTransparent(1)
        ret = Renderer.applySkin(self, desktop, screen)
        return ret

    def changed(self, what):
        try:
            if not self.instance:
                return

            event = self.source.event
            try:
                #Prüfen ob eventId vorhanden ist
                eventid = event.getEventId()
            except Exception as e:
                #Fehler, dann ist event array
                event = self.source.event[0]

            self.hideimage()
            if event is None:
                self.eventid = None
                self.instance.hide()
                return
            if what[0] == self.CHANGED_CLEAR:
                self.eventid = None
            if what[0] != self.CHANGED_CLEAR:

                if event:
                    self.smallptr = False
                    eventid = event.getEventId()
                    startTime = event.getBeginTime()
                    title = event.getEventName()

                    # Default Image aus Folder 'Default' über Title
                    defaultImage = getDefaultImage(self, title)
                    if (defaultImage != None):
                        self.smallptr = True
                        self.image.setPixmap(loadJPG(defaultImage))
                        self.image.setScale(self.scaletype)
                        self.showimage()
                        return

                    # ExtraDaten aus db holen
                    values = self.deserializeJson(getExtraData(self.source, self.log))

                    if(values != None and len(values) > 0 and eventid):
                        try:
                            if eventid != self.eventid:
                                self.id = str(values['id'])

                                sizedImage = getEventImage(self, 
                                    startTime, self.id, True)
                                if (sizedImage != None):
                                    # Image mit size des Widgets laden, sofern verfügbar
                                    self.image.setPixmap(loadJPG(sizedImage))
                                    self.image.setScale(self.scaletype)
                                    self.showimage()
                                    return
                                else:
                                    # Image downloaden
                                    self.downloadImage(
                                        str(values['id']), int(startTime), event)

                                    # Bild bis Download abgeschlossen ist
                                    self.showSmallImage(startTime, self.id)

                            return
                        except Exception as e:
                            self.log.exception("changed: %s", str(e))
                            self.hideimage()

        except Exception as e:
            self.log.exception("changed: %s", str(e))
        
        return

    def GUIcreate(self, parent):
        self.instance = eWidget(parent)
        self.image = ePixmap(self.instance)
        self.text = eLabel(self.instance)
        self.test_label = eLabel(self.instance)

    def showimage(self):
        self.instance.show()
        self.image.show()

    def hideimage(self):
        self.labelheight = self.HCover
        self.image.hide()
        self.text.resize(eSize(self.WCover, self.HCover))
        self.text.move(ePoint(0, 0))

    def onShow(self):
        self.suspended = False

    def onHide(self):
        self.suspended = True

    def downloadImage(self, eventId, startTime, event):
        url = 'http://capi.tvmovie.de/v1/broadcast/%s?fields=images.id,previewImage.id' % str(
            eventId)
        getPage(url).addCallback(self.response, self.DOWNOAD_IMAGE, eventId, startTime,
                                 event).addErrback(self.responseError, self.DOWNOAD_IMAGE, startTime)

    def response(self, data, response, eventId, startTime, event):
        # Antwort für Async Task
        size = '_%s_%s' % (str(self.WCover), str(self.HCover))
        path = os.path.join(self.epgShareImagePath, str(
                            time.strftime('%D', time.localtime(startTime))).replace('/', '.'))
        imageFileName = '%s/%s%s.jpg' % (path, eventId, size)

        if (response == self.DOWNOAD_IMAGE):
            # Image downloaden
            try:
                values = self.deserializeJson(data)

                if(values != None and len(values) > 0):
                    # Images sind verfügbar
                    url = None
                    if 'previewImage' in values:
                        url = str(values['previewImage']['id'])
                    elif 'images' in values:
                        url = str(values['images'][0]['id'])

                    if (url != None):
                        # Images sind zum download verfügbar
                        url = 'http://images.tvmovie.de/%sx%s/Center/%s' % (
                            str(self.WCover), str(self.HCover), url)

                        # Image downloaden
                        downloadPage(url, imageFileName).addCallback(
                            self.response, self.SHOW_IMAGE, eventId, startTime, event).addErrback(self.responseError, response, startTime)
                    else:
                        # Kein Bild zum donwload vorhanden, auf Platte zurück greifen
                        self.showSmallImage(startTime, eventId)

                    # TODO: Hier noch als alternative wenn Daten nicht vefügbar sind, smallImage von Platte laden

            except Exception as e:
                self.log.exception("response: [%s] %s", response, str(e))
                self.hideimage()

        if (response == self.SHOW_IMAGE):
            # Image wurde heruntergeladen -> anzeigen
            try:
                if (os.path.exists(imageFileName)):
                    # img = Image.open(p).convert('RGBA')
                    # img.save(p)
                    if (eventId == self.id):
                        self.image.setPixmap(loadJPG(imageFileName))
                        self.image.setScale(self.scaletype)
                        self.showimage()
                    else:
                        # Kein Bild vorhanden, auf Platte zurück greifen
                        self.showSmallImage(startTime, eventId)
            except Exception as e:
                self.log.exception("response: [%s] %s", response, str(e))
                self.hideimage()

    def responseError(self, e, response, startTime):
        self.log.exception("response: [%s] %s", response, str(e))
        self.showSmallImage(startTime, self.id)

    def showSmallImage(self, startTime, eventId):
        smallImage = getEventImage(self, startTime, eventId)
        if (smallImage != None):
            # Bild bis Download abgeschlossen ist
            self.image.setPixmap(loadJPG(smallImage))
            self.image.setScale(self.scaletype)
            self.showimage()
        else:
            self.hideimage()

    def checkEpgShareAvailable(self):
        try:
            from Plugins.Extensions.EpgShare.main import getEPGDB
            return True
        except:
            return False

    def deserializeJson(self, data):
        # Daten aus DB deserializieren
        try:
            if str(data) != '':
                return json.loads(data)
        except Exception as e:
            self.log.exception("deserializeJson: %s", str(e))
            return None

    def initializeLog(self):
        logger = logging.getLogger("ScroungerEventImage")
        logger.setLevel(logging.DEBUG)

        # create a file handler
        dir = '/mnt/hdd/scroungerLog/'

        if not os.path.exists(dir):
            os.makedirs(dir)

        handler = logging.FileHandler('%sScroungerEventImage.log' % (dir))
        handler.setLevel(logging.DEBUG)

        # create a logging format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s: [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(handler)

        return logger
