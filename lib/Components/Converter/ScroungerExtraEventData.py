from Components.Converter.Converter import Converter
from Components.Element import cached
import json
import HTMLParser

class ScroungerExtraEventData(Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)
        self.type = str(type).split()

    @cached
    def getValue(self):
        if self.type != '':
            rets = []
            ret = ''
            gotevent = False
            if self.source.text:
                values = self.source.text
                gotevent = True
            ret = False
            if gotevent and values:
                for field in self.type:
                    if field == 'TRAILER':
                        if 'trailer' in values:
                            if len(str(values['trailer']).strip()) > 0 and str(values['trailer']).strip().endswith('.mp4'):
                                ret = True

            return ret

    @cached
    def getText(self):
        h = HTMLParser.HTMLParser()
        if self.type != '':
            rets = []
            ret = ''
            gotevent = False
            if self.source.text:
                values = self.source.text
                gotevent = True
            if gotevent and values:
                for field in self.type:
                    try:
                        if field == 'IMAGE':
                            if len(str(values['id']).strip()) > 0:
                                return str(values['id']).strip()
                        elif field == 'TITLE':
                            if len(str(values['title']).strip()) > 0:
                                rets.append(str(values['title']).strip())
                        elif field == 'SUBTITLE':
                            if len(str(values['subtitle']).strip()) > 0:
                                rets.append(str(values['subtitle']).strip())
                        elif field == 'SERIESINFO':
                            if 'season' in values and 'episode' in values:
                                if len(str(values['season']).strip()) > 0 and len(str(values['episode']).strip()) > 0:
                                    rets.append('S%sE%s' % (str(values['season']).zfill(2), str(values['episode']).zfill(2)))
                        elif field == 'CATEGORY':
                            if 'categoryName' in values:
                                if len(str(values['categoryName']).strip()) > 0:
                                    rets.append(str(values['categoryName']).strip())
                        elif field == 'GENRE':
                            if 'genre' in values:
                                if len(str(values['genre']).strip()) > 0:
                                    rets.append(str(values['genre']).strip())
                        elif field == 'AGE':
                            if 'ageRating' in values:
                                if len(str(values['ageRating']).strip()) > 0:
                                    rets.append(str(values['ageRating']).strip())
                        elif field == 'YEAR':
                            if 'year' in values:
                                if len(str(values['year']).strip()) > 0:
                                    rets.append(str(values['year']).strip())
                        elif field == 'COUNTRY':
                            if 'country' in values:
                                if len(str(values['country']).strip()) > 0:
                                    rets.append(str(values['country']).strip())
                        elif field == 'IMDB':
                            if 'vote' in values:
                                if len(str(values['vote']).strip()) > 0 and str(values['vote']).strip() != 'None':
                                    rets.append('IMDB: %s' % str(values['vote']).strip())
                        elif field == 'EPISODENAME':
                            subtitle = ''
                            seriesnum = ''
                            if len(str(values['subtitle']).strip()) > 0:
                                subtitle = str(values['subtitle']).strip()
                            if 'season' in values and 'episode' in values:
                                if len(str(values['season']).strip()) > 0 and len(str(values['episode']).strip()) > 0:
                                    seriesnum = ( '(%s.%s)' % (str(values['season']), str(values['episode'])))
                            rets.append('%s %s' % (subtitle, seriesnum))
                    except:
                        pass

                sep = ' %s ' % str(h.unescape('&#xB7;'))
                ret = sep.join(rets)
        return ret

    text = property(getText)
    boolean = property(getValue)