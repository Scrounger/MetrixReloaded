import json
import os
import time
import base64
import skin
from Tools.FluidNextEventNameCleaner import cleanEventName
from Components.config import config
from Components.Sources.Event import Event
from enigma import eLabel, ePixmap, ePoint, eSize, eTimer, eWidget, loadJPG, loadPNG
from PIL import Image
from Renderer import Renderer
from skin import parseColor, parseFont
from twisted.web.client import downloadPage, getPage
from Plugins.Extensions.FluidNextSetup.fluidnext import get_Extradata, get_defaultepgimage
from Components.Sources.ExtEvent import ExtEvent
from Components.Sources.ServiceEvent import ServiceEvent

class ScroungerEventImage(Renderer):

    def __init__(self):
        Renderer.__init__(self)
        self.eventid = None
        self.downloads = []
        self.name = ''
        self.force = False
        self.id = None
        self.picname = ''
        self.imageheight = 0
        self.defaultptr = get_defaultepgimage()
        self.smallptr = False
        self.usedefault = False
        self.labeltop = 0
        self.scaletype = 2
        self.showtitle = True
        self.WCover = self.HCover = self.TCover = self.LCover = self.WPreview = self.HPreview = self.TPreview = self.LPreview = 0
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
                elif attrib == 'font':
                    self.txfont = parseFont(value, ((1, 1), (1, 1)))
                elif attrib == 'foregroundColor':
                    self.fg = parseColor(str(value))
                elif attrib == 'showtitle':
                    if int(value) == 0:
                        self.showtitle = False
                elif attrib == 'scale':
                    self.scaletype = int(value)
                elif attrib == 'usedefault':
                    if int(value) == 1:
                        self.usedefault = True
                elif attrib == 'force':
                    if int(value) == 1:
                        self.force = True
                elif attrib == 'backgroundColor':
                    attribs.append((attrib, value))
                    self.bg = parseColor(str(value))
                else:
                    attribs.append((attrib, value))

            self.skinAttributes = attribs
        if self.showtitle:
            self.image.resize(eSize(self.WCover, self.labeltop))
        else:
            self.image.resize(eSize(self.WCover, self.HCover))
        self.labelheight = self.HCover - (10 + self.labeltop)
        self.text.resize(eSize(self.WCover, self.HCover - (10 + self.labeltop)))
        self.test_label.resize(eSize(self.WCover, self.HCover - (10 + self.labeltop)))
        self.text.move(ePoint(0, self.labeltop + 10))
        self.text.setFont(self.txfont)
        self.test_label.setFont(self.txfont)
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

    def setText(self):
        title = self.name
        if self.test_label is not None and self.name != '':
            self.test_label.setText(str(title))
            text_size = self.test_label.calculateSize()
            if text_size.height() > self.labelheight:
                resizing = True
                i = -1
                while resizing:
                    self.test_label.setText('%s%s' % (title[:i], '...'))
                    if self.test_label.calculateSize().height() < self.labelheight:
                        text_size = self.test_label.calculateSize()
                        title = '%s%s' % (title[:i], '...')
                        resizing = False
                    else:
                        i -= 1

        self.text.setText(title)
        return

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
            p1 = cleanEventName(title)
            ExtraEventData = None
            if self.showtitle:
                self.name = str(self.build_eventstr(title, starttime))
                self.setText()
            try:
                ExtraEventData = get_Extradata(str(self.source.service), str(self.source.event.getEventId()), starttime, title)
            except Exception as ex:
                print 'Error FluidNextEventImage: %s' % str(ex)

            if ExtraEventData and eventid:
                try:
                    if eventid != self.eventid:
                        size = ''
                        self.id = str(ExtraEventData['id'])
                        if self.force:
                            size = '_%s_%s' % (str(self.WCover), str(self.HCover))
                        smalltarget = self.getimagesubfolder(int(starttime)) + '/' + str(ExtraEventData['id'] + '.jpg')
                        target = self.getimagesubfolder(int(starttime)) + '/' + str(ExtraEventData['id'] + size + '.jpg')
                        if not os.path.exists(target):
                            u = 'http://capi.tvmovie.de/v1/broadcast/%s?fields=images.id,previewImage.id' % str(ExtraEventData['id'])
                            if not config.plugins.FluidNextSetup.offlinemode.value:
                                getPage(u).addCallback(self.gotcover, 0, str(ExtraEventData['id']), int(starttime), event).addErrback(self.dlerror)
                            if os.path.exists(smalltarget):
                                self.smallptr = True
                                self.image.setPixmap(loadJPG(smalltarget))
                                self.image.setScale(self.scaletype)
                                self.showimage()
                            elif os.path.exists(p1):
                                self.smallptr = True
                                self.image.setPixmap(loadJPG(p1))
                                self.image.setScale(self.scaletype)
                                self.showimage()
                        else:
                            self.image.setPixmap(loadJPG(target))
                            self.image.setScale(self.scaletype)
                            self.showimage()
                except Exception as ex:
                    self.colorprint('Error in Eventimage: %s' % str(ex))
                    try:
                        if os.path.exists(p1):
                            self.smallptr = True
                            self.image.setPixmap(loadJPG(p1))
                            self.image.setScale(self.scaletype)
                            self.showimage()
                        else:
                            self.hideimage()
                    except:
                        self.hideimage()

            elif os.path.exists(p1):
                self.smallptr = True
                self.image.setPixmap(loadJPG(p1))
                self.image.setScale(self.scaletype)
                self.showimage()
            else:
                self.hideimage()
            return
        else:
            return

    def GUIcreate(self, parent):
        self.instance = eWidget(parent)
        self.image = ePixmap(self.instance)
        self.text = eLabel(self.instance)
        self.test_label = eLabel(self.instance)

    def build_eventstr(self, title, starttime):
        begin = time.localtime(starttime)
        return '%02d:%02d\n%s' % (begin[3], begin[4], title)

    def gotcover(self, data, type, id, starttime, item):
        if type == 0:
            try:
                i = json.loads(str(data))
                link = None
                if 'previewImage' in i:
                    link = str(i['previewImage']['id'])
                elif 'images' in i:
                    link = str(i['images'][0]['id'])
                if link:
                    size = ''
                    if self.force:
                        size = '_%s_%s' % (str(self.WCover), str(self.HCover))
                    url = 'http://images.tvmovie.de/%sx%s/Center/%s' % (str(self.WCover), str(self.HCover), link)
                    target = self.getimagesubfolder(int(starttime)) + '/' + id + size + '.jpg'
                    downloadPage(url, target).addCallback(self.gotcover, 1, id, starttime, item).addErrback(self.dlerror)
            except Exception as ex:
                self.colorprint('Error loading cover: %s' % str(ex))
                if self.smallptr is False:
                    self.hideimage()

        else:
            try:
                size = ''
                if self.force:
                    size = '_%s_%s' % (str(self.WCover), str(self.HCover))
                p = self.getimagesubfolder(int(starttime)) + '/' + id + size + '.jpg'
                if os.path.exists(p):
                    img = Image.open(p).convert('RGBA')
                    img.save(p)
                    if id == self.id:
                        self.image.setPixmap(loadJPG(p))
                        self.image.setScale(self.scaletype)
                        self.showimage()
            except Exception as ex:
                print 'Error loading cover: %s' % str(ex)
                if self.smallptr is False:
                    self.hideimage()

        return

    def dlerror(self, error):
        if self.smallptr is False:
            self.image.hide()

    def showimage(self):
        self.instance.show()
        self.image.show()
        if self.showtitle:
            self.labelheight = self.HCover - (10 + self.labeltop)
            self.setText()
            self.text.resize(eSize(self.WCover, self.HCover - (10 + self.labeltop)))
            self.text.move(ePoint(0, self.labeltop + 10))

    def hideimage(self):
        if self.usedefault:
            self.image.setPixmap(self.defaultptr)
            self.image.setScale(self.scaletype)
            self.showimage()
        else:
            self.labelheight = self.HCover
            self.setText()
            self.image.hide()
            self.text.resize(eSize(self.WCover, self.HCover))
            self.text.move(ePoint(0, 0))

    def getimagesubfolder(self, timestamp):
        foldername = os.path.join(str(config.plugins.FluidNextSetup.imagelocation.value), str(time.strftime('%D', time.localtime(int(timestamp)))).replace('/', '.'))
        if not os.path.exists(foldername):
            os.mkdir(foldername)
        return foldername

    def onShow(self):
        self.suspended = False

    def onHide(self):
        self.suspended = True

    def colorprint(self, stringvalue):
        color_print = '\x1b[92m'
        color_end = '\x1b[0m'
        print color_print + '[FluidNextInfobarCover Cover] ' + str(stringvalue) + color_end