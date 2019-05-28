# -*- coding: utf-8 -*-
import json
import os
import time
import base64
import re
import urllib2
import codecs

import skin
from Components.config import config
from Components.Sources.Event import Event
from enigma import eLabel, ePixmap, ePoint, eSize, eTimer, eWidget, loadJPG, loadPNG
from Renderer import Renderer
from skin import parseColor, parseFont
from twisted.web.client import downloadPage, getPage
from Components.Sources.ExtEvent import ExtEvent
from Components.Sources.ServiceEvent import ServiceEvent
from Tools.MetrixReloadedHelper import getDataFromDatabase, getExtraData, getDefaultImage, getEventImage, getEpgShareImagePath, getChannelName, createPosterPaths, isOnlineMode, isDownloadPoster, getPosterDircetory, getPosterFileName, initializeLog
from Components.Converter.MetrixReloadedExtEventEPG import MetrixReloadedExtEventEPG
import logging


class MetrixReloadedEventImage(Renderer):
    DOWNOAD_IMAGE = "DOWNOAD_IMAGE"
    SHOW_IMAGE = "SHOW_IMAGE"
    DOWNLOAD_POSTER_INFOS = "DOWNLOAD_POSTER_INFOS"
    DOWNLOAD_POSTER_SERIES = "DOWNLOAD_POSTER_SERIES"
    DOWNLOAD_POSTER_MOVIE = "DOWNLOAD_POSTER_MOVIE"

    IMAGE = "Image"
    POSTER = "Poster"

    tmDbApiKey = "8789cfd3fbab7dccf1269c3d7d867aff"

    def __init__(self):
        Renderer.__init__(self)

        # Log initialisieren
        self.log = initializeLog("MetrixReloadedEventImage")
        self.logPrefix = ""

        self.eventid = None
        self.downloads = []
        self.name = ''
        self.id = None
        self.picname = ''
        self.imageheight = 0
        self.smallptr = False
        self.labeltop = 0
        self.scaletype = 1
        self.imageType = self.IMAGE
        self.WCover = self.HCover = self.TCover = self.LCover = self.WPreview = self.HPreview = self.TPreview = self.LPreview = 0

        return

    GUI_WIDGET = eWidget

    def applySkin(self, desktop, screen):

        if (isinstance(screen.skinName, str)):
            self.screenName = screen.skinName
        else:
            self.screenName = ', '.join(screen.skinName)

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
                elif attrib == 'imageType':
                    self.imageType = value
                else:
                    attribs.append((attrib, value))

            self.skinAttributes = attribs

        self.image.resize(eSize(self.WCover, self.HCover))

        ret = Renderer.applySkin(self, desktop, screen)
        return ret

    def changed(self, what):
        try:
            if not self.instance:
                return

            self.hideimage()

            if hasattr(self.source, 'getEvent'):
                # source is 'extEventInfo'
                event = self.source.getEvent()
            else:
                # source is 'ServiceEvent' / 'ExtEvent'
                event = self.source.event

            # Prüfen ob event tuple ist
            if (isinstance(event, tuple)):
                event = event[0]

            if event is None:
                self.hideimage()
                self.eventid = None
                self.instance.hide()
                return
            if what[0] == self.CHANGED_CLEAR:
                self.hideimage()
                self.eventid = None
            if what[0] != self.CHANGED_CLEAR:
                self.logPrefix = "[%s, %s, %s] " % (self.screenName, type(
                    self.source).__name__, getChannelName(self.source))

                if event:
                    if hasattr(self.source, 'getEvent'):
                        eventid = self.source.getEventId()
                    else:
                        eventid = event.getEventId()

                    self.smallptr = False
                    startTime = event.getBeginTime()
                    title = event.getEventName()

                    # ExtraDaten aus db holen
                    values = self.deserializeJson(
                        getExtraData(self.source, self.log, self.logPrefix))
                    try:
                        if(self.imageType == self.IMAGE):

                            # Default Image aus Folder 'Default' über Title
                            defaultImage = getDefaultImage(self, title)
                            if (defaultImage != None):
                                self.log.debug(
                                    "%schanged: load default image for '%s'", self.logPrefix, title)
                                self.smallptr = True
                                self.image.setPixmap(loadJPG(defaultImage))
                                self.image.setScale(self.scaletype)
                                self.showimage()
                                return

                            if(values != None and len(values) > 0 and eventid):
                                # EpgShare Daten sind vorhanden
                                if eventid != self.eventid:
                                    self.id = str(values['id'])

                                    sizedImage = getEventImage(self,
                                                               startTime, self.id, self.log, self.logPrefix, True)
                                    if (sizedImage != None):
                                        # Image mit size des Widgets laden, sofern verfügbar
                                        self.log.debug(
                                            "%schanged: load local image for '%s' (size: %sx%s)", self.logPrefix, title, self.WCover, self.HCover)
                                        self.image.setPixmap(
                                            loadJPG(sizedImage))
                                        self.image.setScale(self.scaletype)
                                        self.showimage()
                                        return
                                    else:
                                        # Image downloaden
                                        if(isOnlineMode()):
                                            self.downloadImage(
                                                str(values['id']), int(startTime), event)

                                            # Bild bis Download abgeschlossen ist
                                            self.showSmallImage(
                                                startTime, self.id)
                                        else:
                                            self.showSmallImage(
                                                startTime, self.id)
                                            self.log.debug(
                                                "%schanged: image: online mode is deactivated", self.logPrefix)
                            else:
                                self.hideimage()
                        elif(self.imageType == self.POSTER):

                            # Prüfen ob Poster lokal existiert
                            posterFileName = os.path.join(
                                getPosterDircetory(), getPosterFileName(title))
                            if (os.path.exists(posterFileName)):
                                self.log.debug(
                                    "%schanged: poster exist local ('%s')", self.logPrefix, posterFileName)
                                self.showPoster(posterFileName)
                            else:
                                # Poster muss heruntergeladen werden
                                if(isOnlineMode()):
                                    if(isDownloadPoster()):
                                        self.useMetrixReloadedExtEventEpg(
                                            values, event, event.getEventName())
                                    else:
                                        self.log.debug(
                                            "%schanged: poster: download posters is deactivated", self.logPrefix)
                                        self.hideimage()
                                else:
                                    self.log.debug(
                                        "%schanged: poster: online mode is deactivated", self.logPrefix)
                                    self.hideimage()

                        else:
                            self.log.warn(
                                "%schanged: imageType '%s' is unknown!", self.logPrefix, self.imageType)
                            self.hideimage()

                    except Exception as e:
                        self.log.exception(
                            "%schanged (1): %s", self.logPrefix, str(e))
                        self.hideimage()
                else:
                    self.hideimage()

        except Exception as e:
            self.log.exception("%schanged: %s", self.logPrefix, str(e))
            self.hideimage()

        return

    def GUIcreate(self, parent):
        self.instance = eWidget(parent)
        self.image = ePixmap(self.instance)

    def showimage(self):
        self.instance.show()
        self.image.show()

    def hideimage(self):
        self.labelheight = self.HCover
        self.image.hide()

    def onShow(self):
        self.suspended = False

    def onHide(self):
        self.suspended = True

    def useMetrixReloadedExtEventEpg(self, values, event, title, genre=None):

        if(genre == None):
            # Prüfen ob wir eine Serie sind
            episodeNum = MetrixReloadedExtEventEPG(
                "EpisodeNum").getEpisodeNum("EpisodeNum", event, values)
            if(episodeNum != None):
                genre = 'Serien'
                self.log.debug("%suseMetrixReloadedExtEventEpg: 'EpisodeNum' exist for '%s' -> using tvdb.com" %
                               (self.logPrefix, event.getEventName()))

        # Genre holen und in 'Serie' oder 'Spielfilm' umwandeln
        if(genre == None):
            genre = MetrixReloadedExtEventEPG(
                "Genre").getGenre("Genre", values, event)
            if(genre != None):
                if('serie' in genre.lower() or 'soap' in genre.lower() or 'reihe' in genre.lower()):
                    self.log.debug("%suseMetrixReloadedExtEventEpg: genre '%s' exist for '%s' -> using tvdb.com" %
                                   (self.logPrefix, genre, event.getEventName()))
                    genre = 'Serien'
                else:
                    self.log.debug("%suseMetrixReloadedExtEventEpg: genre '%s' exist for '%s' -> using themoviedb.org" %
                                   (self.logPrefix, genre, event.getEventName()))
                    genre = 'Spielfilm'

            else:
                # mit tmdb probieren
                genre = 'Spielfilm'

        if(genre != None):
            url = None
            # url bauen
            if(genre == 'Serien'):
                url = "http://thetvdb.com/api/GetSeries.php?seriesname=%s&language=de" % (
                    urllib2.quote(codecs.encode(title, 'utf-8')))
            else:
                url = "http://api.themoviedb.org/3/search/movie?api_key=%s&query=%s&language=de" % (
                    self.tmDbApiKey, urllib2.quote(codecs.encode(title, 'utf-8')))

                # schauen ob Jahr verfügbar
                year = MetrixReloadedExtEventEPG(
                    "Year").getYear("Year", values, event)
                if(year != None):
                    url += '&primary_release_year=%s&year=%s' % (year, year)

            self.downloadPosterInfos(url, genre, event, title, values)

        else:
            self.log.debug("%suseMetrixReloadedExtEventEpg: poster lookup: no url or genre avaiable for '%s'" % (
                self.logPrefix, event.getEventName()))
            self.hideimage()

    def downloadPosterInfos(self, url, genre, event, title, values):
        if(isOnlineMode()):
            if(url != None):
                self.log.debug("%sdownloadPoster: searching online infos for '%s', url: %s",
                               self.logPrefix, event.getEventName(), url)

                getPage(url).addCallback(self.responsePosterInfo, self.DOWNLOAD_POSTER_INFOS,
                                         genre, title, values, event).addErrback(self.reponsePosterError, self.DOWNLOAD_POSTER_INFOS, url)
            else:
                self.log.warn("%sdownloadPoster: no url for '%s'",
                              self.logPrefix, event.getEventName())

    def responsePosterInfo(self, data, response, genre, title, values, event):

        if (response == self.DOWNLOAD_POSTER_INFOS):
            if (genre == 'Serien' or genre == 'Reportage'):
                seriesId = re.findall('<seriesid>(.*?)</seriesid>', data, re.I)

                if seriesId:
                    self.downloadPoster(
                        str(seriesId[0]), self.DOWNLOAD_POSTER_SERIES, title)
                else:
                    self.log.debug(
                        "%sresponsePosterInfos: no infos found on tvdb.com for '%s'", self.logPrefix, title)
                    self.hideimage()

            elif genre == 'Spielfilm':
                jsonData = json.loads(data)

                if(jsonData['results']):
                    movieId = str(jsonData['results'][0]['id'])
                    moviePosterPath = str(
                        jsonData['results'][0]['poster_path'])

                    if moviePosterPath and moviePosterPath != "None" and movieId:
                        self.log.debug(
                            "%sresponsePosterInfos: movieId '%s', path: %s", self.logPrefix, movieId, moviePosterPath)
                        self.downloadPoster(
                            movieId, self.DOWNLOAD_POSTER_MOVIE, title, moviePosterPath)
                    else:
                        self.log.debug(
                            "%sresponsePosterInfos: no infos found on themoviedb.org for '%s', retry with tvdb.com", self.logPrefix, title)

                        # Nochmal mit tvdb.com probieren
                        self.useMetrixReloadedExtEventEpg(
                            values, event, event.getEventName(), 'Serien')
                        self.hideimage()
                else:
                    self.log.debug(
                        "%sresponsePosterInfos: no infos found on themoviedb.org for '%s', retry with tvdb.com", self.logPrefix, title)

                    # Nochmal mit tvdb.com probieren
                    self.useMetrixReloadedExtEventEpg(
                        values, event, event.getEventName(), 'Serien')
                    self.hideimage()

    def downloadPoster(self, id, posterTyp, title, moviePosterPath=None):

        if(posterTyp == self.DOWNLOAD_POSTER_SERIES):
            posterFileName = os.path.join(
                getPosterDircetory(), getPosterFileName(title))

            posterUrl = 'https://www.thetvdb.com/banners/posters/%s-1.jpg' % id

            downloadPage(posterUrl, posterFileName).addCallback(self.responsePosterDownload, self.DOWNLOAD_POSTER_SERIES,
                                                                id, posterFileName, posterUrl).addErrback(self.reponsePosterTvDbError, self.DOWNLOAD_POSTER_SERIES, posterUrl, posterFileName, id)

        elif(posterTyp == self.DOWNLOAD_POSTER_MOVIE):
            posterFileName = os.path.join(
                getPosterDircetory(), getPosterFileName(title))

            posterUrl = 'http://image.tmdb.org/t/p/w500%s' % moviePosterPath

            downloadPage(posterUrl, posterFileName).addCallback(self.responsePosterDownload, self.DOWNLOAD_POSTER_MOVIE,
                                                                id, posterFileName, posterUrl).addErrback(self.reponsePosterError, self.DOWNLOAD_POSTER_MOVIE, posterUrl)

    def responsePosterDownload(self, data, response, id, posterFileName, posterUrl):

        if (response == self.DOWNLOAD_POSTER_SERIES):
            self.log.debug(
                "%sdownloadPoster: download poster for seriesId '%s' successful, (url: %s)", self.logPrefix, id, posterUrl)

        if (response == self.DOWNLOAD_POSTER_MOVIE):
            self.log.debug(
                "%sdownloadPoster: download poster for moviesId '%s' successful, (url: %s)", self.logPrefix, id, posterUrl)

        if(response == self.DOWNLOAD_POSTER_SERIES or response == self.DOWNLOAD_POSTER_MOVIE):
            if (os.path.exists(posterFileName)):
                self.showPoster(posterFileName)

    def downloadImage(self, eventId, startTime, event):
        self.log.debug("%sdownloadImage: searching online image for '%s'",
                       self.logPrefix, event.getEventName())
        url = 'http://capi.tvmovie.de/v1/broadcast/%s?fields=images.id,previewImage.id' % str(
            eventId)
        getPage(url).addCallback(self.response, self.DOWNOAD_IMAGE, eventId, startTime,
                                 event).addErrback(self.responseError, self.DOWNOAD_IMAGE, startTime)

    def response(self, data, response, eventId, startTime, event):
        # Antwort für Async Task
        size = '_%s_%s' % (str(self.WCover), str(self.HCover))
        path = os.path.join(getEpgShareImagePath(self), str(
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
                        self.log.debug("%schanged: download image for '%s' (size: %sx%s)",
                                       self.logPrefix, event.getEventName(), self.WCover, self.HCover)

                        downloadPage(url, imageFileName).addCallback(
                            self.response, self.SHOW_IMAGE, eventId, startTime, event).addErrback(self.responseError, response, startTime)
                    else:
                        # Kein Bild zum donwload vorhanden, auf Platte zurück greifen
                        self.log.debug(
                            "%schanged: no online image exist for '%s'", self.logPrefix, event.getEventName())
                        self.showSmallImage(startTime, eventId)

                    # TODO: Hier noch als alternative wenn Daten nicht vefügbar sind, smallImage von Platte laden

            except Exception as e:
                self.log.exception(
                    "%sresponse: [%s] %s", self.logPrefix, response, str(e))
                self.hideimage()

        if (response == self.SHOW_IMAGE):
            # Image wurde heruntergeladen -> anzeigen
            try:
                if (os.path.exists(imageFileName)):
                    if (eventId == self.id):
                        self.log.debug("%schanged: load downloaded image for '%s' (size: %sx%s)",
                                       self.logPrefix, event.getEventName(), self.WCover, self.HCover)
                        self.image.setPixmap(loadJPG(imageFileName))
                        self.image.setScale(self.scaletype)
                        self.showimage()
                    else:
                        # Kein Bild vorhanden, auf Platte zurück greifen
                        self.showSmallImage(startTime, eventId)
            except Exception as e:
                self.log.exception(
                    "%sresponse: [%s] %s", self.logPrefix, response, str(e))
                self.hideimage()

    def responseError(self, e, response, startTime):
        self.log.exception(
            "%sresponse: [%s] %s", self.logPrefix, response, str(e))
        self.showSmallImage(startTime, self.id)

    def reponsePosterError(self, e, response, posterUrl):
        self.log.exception(
            "%sreponsePosterError: [%s] %s (url: %s)", self.logPrefix, response, str(e), posterUrl)
        self.hideimage()

    def reponsePosterTvDbError(self, e, response, posterUrl, posterFileName, id):
        self.log.exception(
            "%sreponsePosterTvDbError: [%s] %s", self.logPrefix, response, str(e))

        if("404 Not Found" in str(e)):
            posterUrl = posterUrl.replace("-1.jpg", "-2.jpg")

            self.log.debug(
                "%sdownloadPoster: retry download poster for '%s' with other url: %s", self.logPrefix, id, posterUrl)

            downloadPage(posterUrl, posterFileName).addCallback(self.responsePosterDownload, self.DOWNLOAD_POSTER_SERIES,
                                                                id, posterFileName, posterUrl).addErrback(self.reponsePosterError, self.DOWNLOAD_POSTER_SERIES, posterUrl)
        else:
            self.hideimage()

    def showSmallImage(self, startTime, eventId):
        smallImage = getEventImage(
            self, startTime, eventId, self.log, self.logPrefix)
        if (smallImage != None):
            # Bild bis Download abgeschlossen ist
            self.image.setPixmap(loadJPG(smallImage))
            self.image.setScale(self.scaletype)
            self.showimage()
        else:
            self.hideimage()

    def showPoster(self, posterFileName):

        self.image.setPixmap(loadJPG(posterFileName))
        self.image.setScale(self.scaletype)
        self.showimage()

    def deserializeJson(self, data):
        # Daten aus DB deserializieren
        try:
            if str(data) != '':
                return json.loads(data)
        except Exception as e:
            self.log.exception("%sdeserializeJson: %s", self.logPrefix, str(e))
            return None
