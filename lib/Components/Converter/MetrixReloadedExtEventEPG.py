# -*- coding: utf-8 -*-
from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.MetrixReloadedHelper import getDataFromDatabase, getExtraData, getDefaultImage, getEventImage, initializeLog

from Tools.MovieInfoParser import getExtendedMovieDescription

import json
import HTMLParser
import re
import os

import logging

class MetrixReloadedExtEventEPG(Converter, object):
	#Input Parameter per Skin
	IMAGEID = "ImageId"
	IS_IMAGE_AVAILABLE = "IsImageAvailable"
	IS_EPGSHARE_AVAILABLE = "IsEpgShareAvailable"
	EPGSHARE_RAW = "EpgShareRaw"
	EPISODE_NUM = "EpisodeNum"						# optional formatierung angeben -> z.B. EpisodeNum(Staffel [s] Episode[ee])
	TITLE = "Title"									# optional mit Prefix angabe -> z.B. Titel oder Titel(Titel:)
	SUBTITLE = "Subtitle"							# mit MaxWord angabe -> z.B. Subtitle(10)
	PARENTAL_RATING = "ParentalRating"				# optional mit Prefix angabe -> z.B. ParentalRating oder ParentalRating(FSK)
	GENRE = "Genre"									# optional mit Prefix angabe -> z.B. Genre oder Genre(Genre:)
	YEAR = "Year"									# optional mit Prefix angabe -> z.B. Year oder Year(Jahr:)
	COUNTRY = "Country"								# optional mit Prefix angabe -> z.B. Country oder Country(Land:)
	RATING = "Rating"								# (nur EpgShare) optional mit Prefix angabe -> z.B. Rating(Bewertung)
	RATING_STARS = "RatingStars"					# (nur EpgShare) optional mit Prefix angabe -> z.B. RatingStars(star) -> Output: 65 -> kann für Images verwendet werden
	CATEGORY = "Category"							# (nur EpgShare) optional mit Prefix angabe -> z.B. Category(Kategorie:)
	EXTENDED_DESCRIPTION = "ExtendedDescription"	# optional mit Prefix angabe -> z.B. ExtendedDescription oder ExtendedDescription(Land:)
	POWER_DESCRIPTION = "PowerDescription"		
	
	#Parser fuer Serien- und Episodennummer
	seriesNumParserList = [('(\d+)[.]\sStaffel[,]\sFolge\s(\d+)'), 
							_('(\d+)[.]\sStaffel[,]\sEpisode\s(\d+)'),
							_('(\d+)[.]\sEpisode\sder\s(\d+)[.]\sStaffel'),
							_('[(](\d+)[.](\d+)[)]')]
	
	htmlParser = HTMLParser.HTMLParser()
	
	
	SPECIAL_FORMAT_PARSED_DESCRIPTION_SUBTITLE = 0
	SPECIAL_FORMAT_PARSED_DESCRIPTION_GENRE = 1
	SPECIAL_FORMAT_PARSED_DESCRIPTION_YEAR = 2
	SPECIAL_FORMAT_PARSED_DESCRIPTION_COUNTRY = 3
	
	def __init__(self, type):
		Converter.__init__(self, type)
		
		self.log = initializeLog("MetrixReloadedExtEventEPG")
		self.logMissingGenre = initializeLog("MetrixReloadedExtEventEPG_MissingGenre")

		self.inputString = type
		self.types = str(type).split(",")
		
	@cached
	def getText(self):
		#self.log.info('getText: inputString: %s (%s)', str(self.inputString), len(self.types))
		
		extraData = getExtraData(self.source, self.log)
		
		try:
			event = self.source.event[0]
		except:
			try:
				event = self.source.event
			except:
				event = None
		
		values = self.deserializeJson(extraData)
		#values = None
		
		if self.types != '':
			result = []
			try:
				for type in self.types:
					type.strip()
					self.logType = type
					
					if type == self.IS_EPGSHARE_AVAILABLE:
						#Prüfen ob EpgShare Daten zur Verfügung stehen
						if(values != None and len(values) > 0):
							return 'true'
						else:
							return 'false'
					elif type == self.EPGSHARE_RAW:
						#alle Daten aus der Datenbank ausgeben
						return getExtraData(self.source, self.log)
					elif type == self.IMAGEID:
						#Nur EpgShare - Id des Images
						if(values != None and len(values) > 0):
							if len(str(values['id']).strip()) > 0:
								return str(values['id']).strip()
					elif type == self.IS_IMAGE_AVAILABLE:
						#Prüfen ob ein Image verfügbar ist
						if(values != None and len(values) > 0):
							return str(self.isImageAvailable(event, values))
						
						return str(False)
					elif self.POWER_DESCRIPTION in type:
						powerDescription = self.getPowerDescription(self.inputString, event, values)
						if(powerDescription != None):
							return powerDescription
						else:
							return ''
					elif self.EPISODE_NUM in type:
						episodeNum = self.getEpisodeNum(type, event, values)
						if (episodeNum != None):
							result.append(episodeNum)
					elif self.TITLE == type:
						title = self.getTitleWithPrefix(type, event, values)
						if(title != None and len(title) > 0 and title != ' '):
							result.append(title)					
					elif self.SUBTITLE in type:
						subtitle = self.getSubtitle(type, event, values)
						if(subtitle != None and len(subtitle) > 0 and subtitle != ' '):
							result.append(subtitle)
					elif self.PARENTAL_RATING in type:
						parentialRating = self.getParentalRating(type, event, values)
						if(parentialRating != None):
							result.append(parentialRating)
					elif self.RATING in type:
						rating = None
						if(self.RATING_STARS in type):
							#gerundetes Rating, kann z.B. für Rating Images verwendet werden
							rating = self.getRating(type, values, event, True)
						else:
							#Rating als Kommazahl
							rating = self.getRating(type, values, event, False)
						
						if(rating != None):
							result.append(rating)
					elif self.CATEGORY in type:
						category = self.getCategory(type, values)
						if(category != None):
							result.append(category)
					elif self.GENRE in type:
						genre = self.getGenre(type, values, event)
						if(genre != None):
							result.append(genre)
					elif self.YEAR in type:
						year = self.getYear(type, values, event)
						if(year != None):
							result.append(year)
					elif self.COUNTRY in type:
						country = self.getCountry(type, values, event)
						if(country != None):
							result.append(country)
					elif self.EXTENDED_DESCRIPTION in type:
						extendedDescription = self.getExtendedDescription(type, values, event)
						if(extendedDescription != None):
							result.append(extendedDescription)

					else:
						result.append("!!! invalid parameter '%s' !!!" % (type))

				sep = ' %s ' % str(self.htmlParser.unescape('&#xB7;'))
				return sep.join(result)					
			except Exception as e:
				self.log.exception("getText: '%s' %s", self.logType, str(e))
				return "[Error] getText: '%s' %s" % (self.logType, str(e))					
					
		return ""
		
	text = property(getText)

	def getPowerDescription(self, input, event, values):
		condition = None
		
		#InputParser ohne Condition
		inputParser = re.match(r'^PowerDescription[[](.*)[]$]', input, re.MULTILINE|re.DOTALL)

		#InputParser mit Condition
		inputParserWithCondition = re.match(r'^PowerDescription[[](True|False|true|false)[]][[](.*)[]$]', input, re.MULTILINE|re.DOTALL)

		if(inputParserWithCondition != None):
			condition = inputParserWithCondition.group(1)
			input = inputParserWithCondition.group(2)
		elif(inputParser != None):
			input = inputParser.group(1)
		else:
			input = None

		if(input != None):
			self.log.info("getPowerDescription: condition: %s" % (str(condition).lower()))
			self.log.info("getPowerDescription: input: %s" % (input))

			if(condition != None and str(self.isImageAvailable(event, values)).lower() != condition.lower()):
				#Zurück wenn Condition nicht erfüllt, sofern condition vorhanden
				return None

			if(self.TITLE in input):
				type = self.getParsedTyp(self.TITLE, input)
				
				self.log.info("getPowerDescription: title type: %s" % (type))

				title = self.getTitleWithPrefix(type, event, values)
				if(title != None and len(title) > 0 and title != ' '):
					input = input.replace(type, title)
				else:
					input = str(input).replace(type, "")
			
			if(self.SUBTITLE in input):
				type = self.getParsedTyp(self.SUBTITLE, input)

				self.log.info("getPowerDescription: subtitle type: %s" % (type))

				subtitle = self.getSubtitle(type, event, values)
				if(subtitle != None and len(subtitle) > 0 and subtitle != ' '):
					input = input.replace(type, subtitle)
				else:
					input = str(input).replace(type, "")
			
			if(self.GENRE in input):
				type = self.getParsedTyp(self.GENRE, input)

				genre = self.getGenre(type, values, event)
				if(genre != None):
					input = input.replace(type, genre)
				else:
					input = str(input).replace(type, "")
			
			if(self.EPISODE_NUM in input):
				type = self.getParsedTyp(self.EPISODE_NUM, input)		

				episodeNum = self.getEpisodeNum(type, event, values)
				if (episodeNum != None):
					input = input.replace(type, episodeNum)
				else:
					input = str(input).replace(type, "")
			
			if(self.CATEGORY in input):
				type = self.getParsedTyp(self.CATEGORY, input)

				category = self.getCategory(type, values)
				if (category != None):
					input = input.replace(type, category)
				else:
					input = str(input).replace(type, "")
			
			if(self.PARENTAL_RATING in input):
				type = self.getParsedTyp(self.PARENTAL_RATING, input)

				parentialRating = self.getParentalRating(type, event, values)
				if (parentialRating != None):
					input = input.replace(type, parentialRating)
				else:
					input = str(input).replace(type, "")
			
			if(self.RATING in input):
				type = self.getParsedTyp(self.RATING, input)

				rating = self.getRating(type, values, event, False)				
				if (rating != None):
					input = input.replace(type, rating)
				else:
					input = str(input).replace(type, "")
			
			if(self.YEAR in input):
				type = self.getParsedTyp(self.YEAR, input)
				
				year = self.getYear(type, values, event)
				if (year != None):
					input = input.replace(type, year)
				else:
					input = str(input).replace(type, "")

			if(self.COUNTRY in input):
				type = self.getParsedTyp(self.COUNTRY, input)

				country = self.getCountry(type, values, event)
				if (country != None):
					input = input.replace(type, country)
				else:
					input = str(input).replace(type, "")
			
			if(self.EXTENDED_DESCRIPTION in input):
				type = self.getParsedTyp(self.EXTENDED_DESCRIPTION, input)

				extendedDescription = self.getExtendedDescription(type, values, event)
				if (extendedDescription != None):
					input = input.replace(type, extendedDescription)
				else:
					input = str(input).replace(type, "")

			# '\,' in MiddleDot umwandeln
			middleDot = str(self.htmlParser.unescape('&#xB7;'))
			sep = ' %s ' % middleDot
			input = input.replace('\\,', sep)

			# Doppelte MiddleDot in einen umwandeln
			input = input.replace('%s  %s' % (middleDot, middleDot), middleDot)
			
			input = input.replace('%s \\n' % middleDot,"\\n")

			#falls input mit newline beginnt -> entfernen
			if(input.startswith('\\n\\n\\n')):
				return input[6:]
			elif(input.startswith('\\n\\n')):
				return input[4:]
			elif(input.startswith('\\n')):
				return input[2:]
			elif(input.startswith(sep)):
				return input[4:]
			else:
				return input

		else:
			return "Wrong format: %s" %(input)

	def getParsedTyp(self, type, input):
		parseString = r'(%s[(].*?[)])' % (type)

		parser = re.search(parseString, input)
		if(parser):
			type = parser.group(1)
			self.log.info("getPowerDescription: subtitle parser: %s" % (parser.group(1)))

			self.log.info("getPowerDescription: subtitle type: %s" % (type))

		return type
	
	def getCountry(self, type, values, event, useEPGShare = True):
		country = None
		
		if(values != None and len(values) > 0 and useEPGShare):
		#EpgShare Daten in DB vorhanden
			if 'country' in values:
				if len(str(values['country']).strip()) > 0:
					country = str(values['country']).strip()

		if (country == None and event != None):
		#Keine EpgShare Daten in DB vorhanden, aus Descriptions extrahieren	

			desc = event.getShortDescription()
			
			if(desc == ''):
				#Rückfalllösung über FullDescription
				desc = self.getFullDescription(event)
			
			if desc != "":			
				#Spezielle EPG Formate parsen
				parsedDesc = self.getSpecialFormatDescription(desc, self.SPECIAL_FORMAT_PARSED_DESCRIPTION_COUNTRY)				
				if(parsedDesc != None):
					country = parsedDesc

			#country aus FullDescription parsen -> Foromat ' xx Min.\n Land Jahr'
			if(country == None):
				country = self.getParsedCountryOrYear(self.SPECIAL_FORMAT_PARSED_DESCRIPTION_COUNTRY, event.getExtendedDescription(), event)					
					
		prefix = self.getPrefixParser(type)
		if(country != None and prefix != None):
			country = '%s%s' % (prefix, country)
			
		return country
	
	def getExtendedDescription(self, type, values, event):
		desc = None

		if(event != None):
			desc = event.getExtendedDescription()

			if(desc != "" and desc != None):

				if(desc == self.getSubtitleFromDescription(event,10)):
					desc = None

				prefix = self.getPrefixParser(type)
				if(desc != None and prefix != None):
					desc = '%s%s' % (prefix, desc)

		# Episoden Nummer entfernen
		if(desc != None and ". Staffel, Folge" in desc):
			episodeNum = self.getEpisodeNum("EpisodeNum([s]. Staffel, Folge [e]: )", event, values)
			if (episodeNum != None):
				desc = desc.replace(episodeNum, "")
		
		# ParentalRating entfernen
		if(desc != None and (" Jahren" in desc or " Jahre" in desc)):
			parentialRating = self.getParentalRating("ParentalRating", event, values, False)
			if (parentialRating != None):
				desc = desc.replace("Ab %s Jahren" % (parentialRating), "")
				desc = desc.replace("Ab %s Jahre" % (parentialRating), "")
		
		# Country und Year entfernen
		if(desc != None):
			country = self.getCountry("Country", values, event, False)
			year = self.getYear("Year", values, event, False)
			if(country != None and year != None):
				desc = desc.replace("%s %s. " % (country, year), "")
				desc = desc.replace("%s %s" % (country, year), "")

		return desc
	
	def getYear(self, type, values, event, useEPGShare = True):
		year = None

		if(values != None and len(values) > 0 and useEPGShare):
		#EpgShare Daten in DB vorhanden
			if 'year' in values:
				if len(str(values['year']).strip()) > 0:
					year = str(values['year']).strip()
					
		if (year == None and event != None):
		#Keine EpgShare Daten in DB vorhanden, aus Descriptions extrahieren
			
			desc = event.getShortDescription()
			
			if(desc == ''):
				#Rückfalllösung über FullDescription
				desc = self.getFullDescription(event)
			
			if desc != "":			
				#Spezielle EPG Formate parsen
				parsedDesc = self.getSpecialFormatDescription(desc, self.SPECIAL_FORMAT_PARSED_DESCRIPTION_YEAR)				
				if(parsedDesc != None):
					year = parsedDesc
					
			#Year aus FullDescription parsen -> Foromat ' xx Min.\n Land Jahr'
			if(year == None):
				year = self.getParsedCountryOrYear(self.SPECIAL_FORMAT_PARSED_DESCRIPTION_YEAR, event.getExtendedDescription(), event)
		
		prefix = self.getPrefixParser(type)
		if(year != None and prefix != None):
			year = '%s%s' % (prefix, year)
	
		return year
	
	def getGenre(self, type, values, event):
		genre = None

		if(values != None and len(values) > 0):
		#EpgShare Daten in DB vorhanden
			if 'genre' in values:
				if len(str(values['genre']).strip()) > 0:
					genre = str(values['genre']).strip()
					
		if (genre == None and event != None):
		#Keine EpgShare Daten in DB vorhanden, aus Descriptions extrahieren
			
			desc = event.getShortDescription()
			
			if(desc == ''):
				#Rückfalllösung über FullDescription
				desc = self.getFullDescription(event)

			if desc != "":			
				#Spezielle EPG Formate parsen
				parsedDesc = self.getSpecialFormatDescription(desc, self.SPECIAL_FORMAT_PARSED_DESCRIPTION_GENRE)				
				if(parsedDesc != None):
					genre = parsedDesc						

		prefix = self.getPrefixParser(type)
		if(genre != None and prefix != None):
			genre = '%s%s' % (prefix, genre)
		
		return genre

	def getCategory(self, type, values):
		category = None
		
		if(values != None and len(values) > 0):
		#EpgShare Daten in DB vorhanden
			if 'categoryName' in values:
				if len(str(values['categoryName']).strip()) > 0:
					category = str(values['categoryName']).strip()
					
		prefix = self.getPrefixParser(type)
		if(category != None and prefix != None):
			category = '%s%s' % (prefix, category)
		
		return category
	
	def getRating(self, type, values, event, isStars):
		rating = None
		
		if(values != None and len(values) > 0):
		#EpgShare Daten in DB vorhanden
			if 'vote' in values:
				if len(str(values['vote']).strip()) > 0:
					tmp = str(values['vote']).strip()
					rating = self.getRatingAsNumber(tmp, isStars)

		if (rating == None and event != None) or (rating == str(0) and  event != None):
			#Rating aus Description extrahieren
			desc = self.getFullDescription(event)

			parser = re.search(r'IMDb rating:\s(\d+\.\d+)[/]', desc)
			if(parser):
				tmp = str(parser.group(1))
				rating = self.getRatingAsNumber(tmp, isStars)

		prefix = self.getPrefixParser(type)
		if(rating != None and prefix != None):
			rating = '%s%s' % (prefix, rating)
					
		return rating

	def getRatingAsNumber(self, strRating, isStars):
		if(self.isNumber(strRating)):
        	# Nur anzeigen wenn Rating > 0
			if(float(strRating) > 0):
				if(isStars):
					return str(round(float(strRating) * 2) / 2).replace(".", "")
				else:
					return strRating.replace(".", ",")
			else:
				if(isStars):
					return ""
		else:
			if(isStars):
				return ""
	
	def getParentalRating(self, type, event, values, useEPGShare = True):				
		parentialRating = None
		
		if(values != None and len(values) > 0 and useEPGShare):
		#EpgShare Daten in DB vorhanden
			if 'ageRating' in values:
				if len(str(values['ageRating']).strip()) > 0:
					tmp = str(values['ageRating']).strip()
					
					if(tmp == 'OhneAltersbeschränkung'):
						parentialRating = str(0)
					elif(tmp == 'KeineJugendfreigabe'):
						parentialRating = str(18)
					elif(tmp != 'Unbekannt'):
						parentialRating = tmp
		
		if (parentialRating == None and event != None):
		#Keine EpgShare Daten in DB vorhanden, aus Descriptions extrahieren
			desc = self.getFullDescription(event)

			parser = re.search(r'Ab\s(\d+)\s[Jahren|Jahre]', desc)
			if(parser):
				parentialRating = parser.group(1)
		
		prefix = self.getPrefixParser(type)
		if(parentialRating != None and prefix != None):
			parentialRating = '%s%s' % (prefix, parentialRating)
		
		return parentialRating
			
	def getTitle(self, event, values):
		#Nur Title ohne Prefix, wird zum vergleichen benötigt
		title = None
				
		if(values != None and len(values) > 0):
		#EpgShare Daten in DB vorhanden				
			if len(str(values['title']).strip()) > 0:
				title = str(values['title']).strip()
						
		if (title == None and event != None):
		#Keine EpgShare Daten in DB vorhanden, aus Descriptions extrahieren
			title = event.getEventName()		
				
		return title
		
	def getTitleWithPrefix(self, type, event, values):
		title = self.getTitle(event, values)

		prefix = self.getPrefixParser(type)
		if(title != None and prefix != None):
			title = '%s%s' % (prefix, title)				
				
		return title		
	
	def getSubtitle(self, type, event, values):
		subtitle = None
		
		if(values != None and len(values) > 0):
		#EpgShare Daten in DB vorhanden	
			if len(str(values['subtitle']).strip()) > 0:
				subtitle= str(values['subtitle']).strip()
			
		if (subtitle == None and event != None):
		#Keine EpgShare Daten in DB vorhanden, aus Descriptions extrahieren
			try:
				maxWords = int(self.getMaxSubtitleWords(type))
				result = self.getSubtitleFromDescription(event, maxWords)
				if (result != None):						
					subtitle = result
			except Exception as ex:
				subtitle = str(ex)
		
		#Falls Subtitle = Title -> dann nichts zurück geben
		if (subtitle != None and subtitle.rstrip('.') == self.getTitle(event, values)):
			subtitle = None

		return subtitle
		
	def getSubtitleFromDescription(self, event, maxWords):
		try:		
			desc = event.getShortDescription()
			
			if(desc == ''):
				#Rückfalllösung über FullDescription
				desc = self.getFullDescription(event)

			if (desc != ""):				
				#Spezielle EPG Formate parsen
				parsedDesc = self.getSpecialFormatDescription(desc, self.SPECIAL_FORMAT_PARSED_DESCRIPTION_SUBTITLE)				
				if(parsedDesc != None):
					return parsedDesc

				#maxWords verwenden				
				self.log.debug("getSubtitleFromDescription")
				result = self.getMaxWords(desc, maxWords)			
				if(result != None):
					
					genre = self.getCompareGenreWithGenreList(result, None)
					if(genre != None):
					#Prüfen Subtitle = Genre, dann nichts zurück geben
						if(genre == result):
							self.log.debug("getSubtitleFromDescription (1): %s is genre: %s", desc, genre)
							return None
					
					self.log.debug("getSubtitleFromDescription (1): %s -> Subtitle: %s", desc, result)
					return result
				else:			
				#Wenn Wörter in shortDescription > maxWords, dann nach Zeichen suchen und bis dahin zurück geben und prüfen ob < maxWord EXPERIMENTAL
					return self.getSubtitleFromDescriptionUntilChar(event, desc, maxWords)

			else:
				return None
		except Exception as e:
			return "[Error] getSubtitleFromDescription: %s" % (str(e))
		
		return None
	
	def getSpecialFormatDescription(self, desc, resultTyp):
		#Spezielle Formate raus werfen
		desc = desc.replace("Thema u. a.: ","")
	
		wordList = desc.split(", ")
		
		#Format: 'Subtitle, Genre, Land Jahr'
		if len(wordList) == 3:		
			parser = re.match(r'^[^.:?;]+[,]\s[^.:?;]+[,]\s[^.:?;]+\s\d+$', desc)
			
			if (desc.count(", ") == 2 and parser):
				#Pruefen 2x ', ' vorhanden ist und ob letzter Eintrag im Format 'Land Jahr'
				#return desc.replace(", ", " %s " % str(self.htmlParser.unescape('&#xB7;')))				
				if(resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_SUBTITLE):
					self.log.debug("getSpecialFormatDescription (1): %s -> Subtitle: %s", desc, wordList[0])
					return wordList[0]
				elif (resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_GENRE):
					self.log.debug("getSpecialFormatDescription (1): %s -> Genre: %s", desc, wordList[1])
					return wordList[1]
				elif (resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_YEAR):
					year = self.getParsedCountryOrYear(resultTyp, wordList[2], None)
					if(year != None):
						self.log.debug("getSpecialFormatDescription (1): %s -> Year: %s", desc, year)
						return year
				elif (resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_COUNTRY):
					country = self.getParsedCountryOrYear(resultTyp, wordList[2], None)
					if(country != None):
						self.log.debug("getSpecialFormatDescription (1): %s -> Country: %s", desc, country)
						return country					
		
		#Format: 'Subtitle/Genre, Land Jahr' | 'Genre, Land Jahr' | 'Subtitle Genre, Land Jahr'
		#TODO: Abgleich mit Genre einfügen
		elif len(wordList) == 2:
			parser = re.match(r'^[^.:?!;]+[,]\s[^.:?!;]+\s\d+$', desc)
			
			if (desc.count(", ") == 1 and parser):

				genre = self.getCompareGenreWithGenreList(wordList[0], ', ')
				if(genre != None):
				#Format 'Genre, Land Jahr'
				#Prüfen ob Wort vor Koma in Genre List ist -> Genre
					if(resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_SUBTITLE):
						self.log.debug("getSpecialFormatDescription (2): %s -> Subtitle: %s", desc, None)
						return ''
					elif (resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_GENRE):
						self.log.debug("getSpecialFormatDescription (2): %s -> Genre: %s", desc, wordList[0])
						return wordList[0]
					elif (resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_YEAR):
						year = self.getParsedCountryOrYear(resultTyp, wordList[1], None)
						if(year != None):
							self.log.debug("getSpecialFormatDescription (2): %s -> Year: %s", desc, year)
							return year
					elif (resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_COUNTRY):
						country = self.getParsedCountryOrYear(resultTyp, wordList[1], None)
						if(country != None):
							self.log.debug("getSpecialFormatDescription (2): %s -> Country: %s", desc, country)
							return country

				#Format 'Subtitle Genre, Land Jahr'
				#Genre herausfiltern						
				genre = self.getCompareGenreWithGenreList(wordList[0], None)
				if(genre != None):
					subtitle = wordList[0].replace(genre + ". ","").replace(genre,"").strip()
					
					if(resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_SUBTITLE):
						if(len(subtitle) > 0):
							self.log.debug("getSpecialFormatDescription (3): %s -> Subtitle: %s", desc, subtitle)
						else:
							self.log.debug("getSpecialFormatDescription (3): %s -> Subtitle: %s", desc, None)
							
						return subtitle
					elif (resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_GENRE):
						self.log.debug("getSpecialFormatDescription (3): %s -> Genre: %s", desc, genre)
						return genre
						
					elif (resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_YEAR):
						year = self.getParsedCountryOrYear(resultTyp, wordList[1], None)
						if(year != None):
							self.log.debug("getSpecialFormatDescription (3): %s -> Year: %s", desc, year)
							return year
					
					elif (resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_COUNTRY):
						country = self.getParsedCountryOrYear(resultTyp, wordList[1], None)
						if(country != None):
							self.log.debug("getSpecialFormatDescription (3): %s -> Country: %s", desc, country)
							return country						
				
				if(resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_SUBTITLE):
				#Format 'Subtitle, Land Jahr'
					self.log.debug("getSpecialFormatDescription (4): %s -> Subtitle: %s", desc, wordList[0])
					return wordList[0]					
		
		#Wird nur für Genre angewendet
		if(resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_GENRE):
			genre = self.getCompareGenreWithGenreList(desc, None)
			if(genre != None):
				self.log.debug("getSpecialFormatDescription (5): %s -> Genre: %s", desc, genre)
				return genre
					
		return None
	
	def getSubtitleFromDescriptionUntilChar(self, event, desc, maxWords):
		#Wenn Wörter in shortDescription > maxWords, dann nach Zeichen suchen und bis dahin zurück geben und prüfen ob < maxWord EXPERIMENTAL		
		firstChar = re.findall(r'[.]\s|[?]\s|[:]\s|$', desc)[0]
		if(firstChar != "" and len(firstChar) > 0):
			firstCharPos = desc.find(firstChar)
			result = desc[0:firstCharPos]			
			
			#Kann ggf. Genre sein, dann raus filtern
			genre = self.getCompareGenreWithGenreList(result, ". ")
			if(genre != None):
				if(genre == result):
					#genre = genre + "."
					desc = desc.replace(genre + ". ","")
					firstCharPos = desc.find(firstChar)
					result = desc[0:firstCharPos]
					
					#maxWords verwenden
					result = self.getMaxWords(result, maxWords)			
					if(result != None):
						self.log.debug("getSubtitleFromDescriptionUntilChar (1): %s -> Subtitle: %s", desc, result)
						return result
					
			#maxWords verwenden
			if(result != None):
				result = self.getMaxWords(result, maxWords)			
				if(result != None):
					self.log.debug("getSubtitleFromDescriptionUntilChar (2): %s -> Subtitle: %s", desc, result)
					return result
		
		return None
		
	def getMaxWords(self, desc, maxWords):
		try:			
			wordList = desc.split(" ")
			if (len(wordList) <= maxWords):
				del wordList[maxWords:len(wordList)]
				sep = ' '
				result = sep.join(wordList)	
				
				return result
		
		except Exception as e:
			self.log.exception("getMaxWords: %s", (str(e)))
			return "[Error] getMaxWords: %s" % (str(e))
			
		return None
	
	def getMaxSubtitleWords(self, type):
		#max Anzahl an erlaubten Wörten aus Parameter von Skin lesen
		maxSubtitleWordsParser = r'Subtitle[(](\d+)[)]'
		maxSubtitleWords = re.search(maxSubtitleWordsParser, type)
		
		if(maxSubtitleWords):
			return maxSubtitleWords.group(1)
		else:
			return "!!! invalid type '%s' !!!" % (type)
	
	def getEpisodeNum(self, type, event, values):
		episodeNum = None
		sNum = None
		eNum = None
		
		if(values != None and len(values) > 0):
			#EpgShare Daten sind in DB vorhanden
			if 'season' in values and 'episode' in values:
				if len(str(values['season']).strip()) > 0 and len(str(values['episode']).strip()) > 0:
					sNum = str(values['season'])
					eNum = str(values['episode'])
	
		if (episodeNum == None and event != None):
			#Keine EpgShare Daten in DB vorhanden, versuch über Parser	
			desc = self.getFullDescription(event)

			for parser in self.seriesNumParserList:
				extractSeriesNums = re.search(parser, desc)

				if(extractSeriesNums):
					sNum = extractSeriesNums.group(1)
					eNum = extractSeriesNums.group(2)

		#individuelle Formatierung extrahieren
		episodeFormat = self.getPrefixParser(type)
		self.log.info("EpisodePrefix: %s" % episodeFormat)
		if(sNum != None and eNum != None):
			if(episodeFormat != None):
				#Staffel Format parsen
				sFormatParser = re.search(r"[[]([s]+|[s])[]]", episodeFormat)
				if(sFormatParser != None):
					sFormat = sFormatParser.group(1)
					sDigits = len(sFormat)

					episodeNum = episodeFormat.replace('[%s]' % (sFormat), sNum.zfill(sDigits))

				#Episoden Format parsen
				eFormatParser = re.search(r"[[]([e]+|[e])[]]", episodeFormat)
				if(eFormatParser != None):
					eFormat = eFormatParser.group(1)
					eDigits = len(eFormat)

					episodeNum = episodeNum.replace('[%s]' % (eFormat), eNum.zfill(eDigits))
			else:
				#Standard falls kein individuelles Format angeben ist
				episodeNum = 'S%sE%s' % (sNum.zfill(2), eNum.zfill(2))

		return episodeNum
		
	def getFullDescription(self, event):
	
		desc = None
		ext_desc = event.getExtendedDescription()
		short_desc = event.getShortDescription()
		if short_desc == "":
			return ext_desc
		elif ext_desc == "":
			return short_desc
		else:
			return "%s\n\n%s" % (short_desc, ext_desc)

	def getPrefixParser(self, type):
		#Prefix aus Parameter von Skin lesen
		prefixParser = '.*[(](.*)[)]'
		prefix = re.search(prefixParser, type)
		
		if(prefix):
			return prefix.group(1)
		else:
			return None			

	def deserializeJson(self, extraData):
		#Daten aus DB deserializieren
		try:
			if str(extraData) != '':
				return json.loads(extraData)
		except Exception as ex:
			return None	

	def isNumber(self, inp):
		try:
			val = int(inp)
			return True
		except ValueError:
			try:
				val = float(inp)
				return True
			except ValueError:
				return False
		
	def getCompareGenreWithGenreList(self, desc, splitChar):

		if(splitChar == None):
			desc = re.sub('[.,]', '', desc)			#Hinter Genre kann direkt ein Zeichen folgen
			descWordList = desc.split(' ')
		else:
			descWordList = desc.split(splitChar)		#WortList zum Vergleichen erzeugen

		setWordList = set(descWordList)
		
		fileName = "/usr/lib/enigma2/python/Components/Converter/MetrixReloadedExtEventEPG_Genre.json"
		if (os.path.isfile(fileName)):
			with open(fileName) as file:
				jsonString = str(file.read())

				# in Uncode umwandeln, da sonst json parsing nicht möglich
				jsonString = jsonString.decode("iso-8859-1")
				genreData = json.loads(jsonString)

				#exakten Treffer suchen
				for genre in genreData:
					# in utf-8 zurück wandeln
					genre = genre.encode('utf-8')

					setGenre = set([genre])
					if setGenre & setWordList:
						#zurück in utf-8 umwandeln
						return genre
		else:
			self.log.Error("File not exist! %s" % fileName)		

		# #exakten Treffer suchen
		# for genre in self.AVAILABLE_GENRES_EPG:
		# 	setGenre = set([genre])
		# 	if setGenre & setWordList:
		# 		return genre
		
		#if(desc in self.AVAILABLE_GENRES_EPG):
		#Description ist Genre (ein Wort)
			#return desc
		
		#for genre in self.AVAILABLE_GENRES_EPG:
			#Genre herausfiltern
			#if(genre in desc):
				#return genre

		if(len(descWordList) == 1):
			# Fehlende Genre in log schreiben, in uft-8
			self.logMissingGenre.info(str(descWordList))

		return None
		
	def getParsedCountryOrYear(self, resultTyp, desc, event):
		
		if(event == None):
		#verwendet von getSpecialFormatDescription
			parser = re.match(r'^([^.:?; ]+)\s(\d+)$', desc)
			if(parser):
				if(resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_COUNTRY):
					return parser.group(1)
				elif(resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_YEAR):
					return parser.group(2)
		else:
			if(desc != ""):
				parser = re.search(r'\s\d+\s[Min.]+\n([^.:?;]+)\s(\d+)', desc)
				if(parser):
					if(resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_COUNTRY):
						return parser.group(1)
					elif(resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_YEAR):
						return parser.group(2)
				
				parser =re.search(r'\s\d+\s[Min.]+\n(\d+)', desc)
				if(parser):
					if(resultTyp == self.SPECIAL_FORMAT_PARSED_DESCRIPTION_YEAR):
						return parser.group(1)
				
		
		return None

	def isImageAvailable(self, event, values):
		#Schauen ob Default Image existiert

		if(event != None):
			image = getDefaultImage(self, event.getEventName())

			if(image == None and values != None):
				#Schauen ob Image existiert
				image = getEventImage(self, event.getBeginTime(), str(values['id']))

			if(image != None):
				return True
		
		return False