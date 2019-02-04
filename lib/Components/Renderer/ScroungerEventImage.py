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
from Tools.ScroungerExtraData import getDataFromDatabase, getExtraData
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
        if not self.instance:
            return
        event = self.source.event
        self.hideimage()
        if event is None:
            self.eventid = None
            self.instance.hide()
            return
        if what[0] == self.CHANGED_CLEAR:
            self.eventid = None
        if what[0] != self.CHANGED_CLEAR:
            self.smallptr = False
            eventid = event.getEventId()
            starttime = event.getBeginTime()
            title = event.getEventName()

            # # Default Image aus Folder 'Default' über Title
            # defaultImage = self.getDefaultImage(title)
            # if (defaultImage != None):
            #     self.smallptr = True
            #     self.image.setPixmap(loadJPG(p1))
            #     self.image.setScale(self.scaletype)
            #     self.showimage()
            #     return

            # ExtraDaten aus db holen
            values = self.deserializeJson(getExtraData(self.source))

            if(values != None and len(values) > 0 and eventid):
                try:
                    if eventid != self.eventid:
                        size = ''
                        self.id = str(values['id'])

                        sizedImage = None
                        #sizedImage = self.getEventImage(starttime, self.id, True)
                        if (sizedImage != None):
                            # Image mit size des Widgets laden, sofern verfügbar
                            self.image.setPixmap(loadJPG(sizedImage))
                            self.image.setScale(self.scaletype)
                            self.showimage()
                            return
                        else:
                            # Image downloaden
                            self.downloadImage(
                                str(values['id']), int(starttime), event)

                    return
                except Exception as e:
                    self.log.error("changed: %s", str(e))
                    self.hideimage()

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
        try:
            url = 'http://capi.tvmovie.de/v1/broadcast/%s?fields=images.id,previewImage.id' % str(
                eventId)

            getPage(url).addCallback(self.response, self.DOWNOAD_IMAGE, eventId, startTime, event).addErrback(self.responseError)

        except Exception as e:
            self.log.error("downloadImage: %s", str(e))

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
                            self.response, self.SHOW_IMAGE, eventId, startTime, event).addErrback(self.responseError)

                    # TODO: Hier noch als alternative wenn Daten nicht vefügbar sind, smallImage von Platte laden

            except Exception as e:
                self.log.error("response: [%s] %s", response, str(e))
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
            except Exception as e:
                self.log.error("response: [%s] %s", response, str(e))
                self.hideimage()

    def responseError(self, e):
        self.log.error("responseError: %s", str(e))
        self.hideimage()

    def getEventImage(self, timestamp, eventId, withSize=False):
        # FileName für Image aus EpgShare Download Folder zurück geben
        try:
            path = os.path.join(self.epgShareImagePath, str(
                time.strftime('%D', time.localtime(int(timestamp)))).replace('/', '.'))

            size = ''
            if(withSize):
                # Size des Widgets berücksitigen
                size = '_%s_%s' % (str(self.WCover), str(self.HCover))

            imageFileName = '%s/%s%s.jpg' % (path, eventId, size)

            if (os.path.exists(imageFileName)):
                self.log.info(
                    'getSizedEventImage: image exist: %s', imageFileName)
                return imageFileName
            else:
                self.log.info(
                    'getSizedEventImage: image not exist: %s', imageFileName)

        except Exception as e:
            self.log.error("getSizedEventImage: %s", str(e))

        return None

    def getDefaultImage(self, title):
        # FileName für Image aus Default Folder zurückgeben
        try:
            # Image aus Default EpgShare Ordner holen, sofern existiert
            path = '%s/Default/' % (self.epgShareImagePath)
            title = title.decode(
                'utf-8').lower().split('(')[0].strip() + '.jpg'

            imageFileName = '%s%s' % (path, base64.b64encode(title))

            if (os.path.exists(imageFileName)):
                self.log.info(
                    'getDefaultImage: image exist: %s', imageFileName)
                return imageFileName
            else:
                self.log.info(
                    'getDefaultImage: image not exist: %s', imageFileName)
        except Exception as e:
            self.log.error("getDefaultImage: %s", str(e))

        return None

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
            self.log.error("deserializeJson: %s", str(e))
            return None

    def initializeLog(self):
        logger = logging.getLogger("ScroungerEventImage")
        logger.setLevel(logging.DEBUG)

        # create a file handler
        handler = logging.FileHandler('/tmp/ScroungerEventImage.log')
        handler.setLevel(logging.DEBUG)

        # create a logging format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s: [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(handler)

        logger.debug("logger initialized")

        return logger
