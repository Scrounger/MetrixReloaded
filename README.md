# MetrixReloaded
[![GitHub release](https://img.shields.io/github/release/Scrounger/MetrixReloaded.svg)](https://github.com/Scrounger/MetrixReloaded/releases)
[![GitHub All Releases](https://img.shields.io/github/downloads/Scrounger/MetrixReloaded/total.svg)](https://github.com/Scrounger/MetrixReloaded/releases)
[![GitHub Releases (by Release)](https://img.shields.io/github/downloads/Scrounger/MetrixReloaded/0.9.5/total.svg)](https://github.com/Scrounger/MetrixReloaded/releases)
![GitHub repo size](https://img.shields.io/github/repo-size/Scrounger/MetrixReloaded.svg)
[![GitHub](https://img.shields.io/github/license/Scrounger/MetrixReloaded.svg)](https://github.com/Scrounger/MetrixReloaded/blob/master/LICENSE)

MetrixReloaded ist ein HD Skin für VU+ Receiver mit [VTI Image](https://www.vuplus-support.org/).

[![paypal](https://www.paypalobjects.com/de_DE/DE/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=YHPPW474N5CKQ&source=url)
[![download](https://dabuttonfactory.com/button.gif?t=Download&f=Calibri-Bold&ts=30&tc=fff&tshs=1&tshc=000&hp=20&vp=8&c=5&bgt=gradient&bgc=3d85c6&ebgc=073763)](https://github.com/Scrounger/MetrixReloaded/releases)

## Unterstütze Images:
* VTI v14.x

## Unterstützte Plugins
* EPGShare (im Skin optional implementiert)
* [EPGRefresh](https://wiki.vuplus-support.org/index.php?title=EPGrefresh)
* [SerienRecorder](https://github.com/einfall/serienrecorder)
* [EPGImport](https://github.com/oe-alliance/XMLTV-Import)
* Filebrowser VTI
* Chromium
* AutoTimer
* Multi QuickButton
* EPGSearch
* PiconManager
* FFC
* CoverFind
* Multi QuickButton
* MediaPlayer
* Satfinder
* [InfoBarTunerState](https://github.com/betonme/e2openplugin-InfoBarTunerState)

## Installation

1. Ladet euch die [aktuelle Version](https://github.com/Scrounger/MetrixReloaded/releases) herunter.
2. Kopiert die heruntergeladene *.ipk Datei in das /tmp/ Vereichnis auf Euren VU+ Receiver
3. Öffne das VtiPanel (Blaue Taste) -> *Manuelle Installation von Paketen* -> *IPKG-Pakete installieren*
4. Wähle die *.ipk Datei aus und starte die Installation

## Einstellungen
<img src="screenshots/MetrixReloadedSetup.jpg?sanitize=true&raw=true" title="MetrixReloadedSetup" width="600"/>

Unter *Erweiterungen* -> *MetrixReloaded* findest du zusätzliche Einstellungen für den Skin. Die Einstellungen sind dort ausführlich beschrieben, sobald du diese anwählst

#### Picons
Der Skin ist für Picons mit einer Auflösung von 330x198px ausgelegt (XHDPicons). Ich verwende diese hier -> [MetrixFHD Pro XHDPicons](https://www.vuplus-support.org/wbb4/index.php?thread/101261-metrixfhd-pro-xhdpicons/)
* Einstellung GUI muss Picons auf vorgegebene SKingröße skalieren auf 'Ja' stehen
<br/> *(Menu -> VTI -> Einstellung GUI -> 'Picons auf vorgegebene Skingröße skalieren': Ja)* 
* Einstellung für Einzeilig & zweizeilige Kanaliste: 100x60 px 
<br/> *(Menu -> VTI -> Einstellung - Kanalliste -> 'Picons in Kanalliste anzeigen': 100x60 px)*
* Einstellung für horizontale Kanalliste: Benutzerdefiniert
<br/> *(Menu -> VTI -> Einstellung - Kanalliste -> 'Picons in Kanalliste anzeigen': Benutzerdefiniert)* 

## Fehlerbehebung / Verbesserungen
Für Fehlerbehebung, Verbesserungen oder von Euch erstellten screenFiles bzw. skinParts ein [Issue](https://github.com/Scrounger/MetrixReloaded/issues) erstellen.
* Bei Fehler immer die Log-Dateien (Debug Modus in den Einstellungen aktivieren!!!) mit anhängen - das Verzeichnis kann in den Einstellungen des Skins festgelegt werden (siehe oben).


## Aufbau des Repositories
* Ich habe ein paar kleine Tools geschrieben, die für die Erstellung des Skin inkl. der Python Dateien verwendet werden.
Die Einstellungen (Verzeichnisse) für die Tools müssen in der [settings.cfg](https://github.com/Scrounger/MetrixReloaded/blob/master/settings.cfg) ggf. angepasst werden
* Für eine bessere und übersichtliche Versionsverwaltung sind alle Screens des Skins in einzelne *.xml Dateien ausgelagert worden. Die einzelnen Screens findet ihr im Verzeichnis [screenFiles](https://github.com/Scrounger/MetrixReloaded/tree/master/screenFiles).
Mit Hilfe der **Merger.exe** wird aus den screenFiles die [skin.xml](https://github.com/Scrounger/MetrixReloaded/blob/master/skin/skin.xml) Datei im Verzeichnis [skin](https://github.com/Scrounger/MetrixReloaded/tree/master/skin) erzeugt
* Genauso sind die SkinParts in das Verzeichnis [skinParts](https://github.com/Scrounger/MetrixReloaded/tree/master/skinparts) ausgelagert worden und werden auch mit dem Tool **Merger.exe** in das [skin](https://github.com/Scrounger/MetrixReloaded/tree/master/skin) Verzeichnis kopiert
* Mit Hilfe der **Builder.exe** wird der Skin inkl. Converter, Renderer, Plugin, etc. gebaut und alle relvanten Daten in das Verzeichnis kopiert, dass als Build-Verzeichnis in der [settings.cfg](https://github.com/Scrounger/MetrixReloaded/blob/master/settings.cfg) angegeben ist. Mit diesen Dateien kann die *.ipk Datei erstellt werden, z.B. mit dem Tool [IPK Creator 5.0 (Java) By Persian Prince](https://www.vuplus-support.org/wbb4/index.php?thread/111551-ipk-creator-5-0-java-by-persian-prince/)
* Skin ist zu 100% kompatibel mit dem [OpenSkin-Designer](https://github.com/Humaxx/OpenSkin-Designer) (Version >= 3.2.0). Könnt ihr [hier downloaden](https://github.com/Humaxx/OpenSkin-Designer/releases)


## Screenshots
<p align="center">
<img src="screenshots/MetrixReloadedSetup.jpg?sanitize=true&raw=true" title="MetrixReloadedSetup" width="400"/>
<img src="screenshots/contextMenu.jpg?sanitize=true&raw=true" title="ContextMenu" width="400"/>
<img src="screenshots/infobar.jpg?sanitize=true&raw=true" title="InfoBar" width="400"/>
<img src="screenshots/SecondInfoBar.jpg?sanitize=true&raw=true" title="SecondInfoBar" width="400"/>
<img src="screenshots/infoBarZapHistory.jpg?sanitize=true&raw=true" title="InfoBarZapHistory" width="400"/>
<img src="screenshots/messageBox.jpg?sanitize=true&raw=true" title="MessageBox" width="400"/>
<img src="screenshots/moviePlayer.jpg?sanitize=true&raw=true" title="MoviePlayer" width="400"/>
<img src="screenshots/movieSelection.jpg?sanitize=true&raw=true" title="MovieSelection" width="400"/>
<img src="screenshots/pluginBrowser.jpg?sanitize=true&raw=true" title="PluginBrowser" width="400"/>
<img src="screenshots/setup.jpg?sanitize=true&raw=true" title="Setup" width="400"/>
<img src="screenshots/timerEditList.jpg?sanitize=true&raw=true" title="TimerEditList" width="400"/>
<img src="screenshots/timerEntry.jpg?sanitize=true&raw=true" title="TimerEntry" width="400"/>
<img src="screenshots/vtiPanel.jpg?sanitize=true&raw=true" title="VtiPanel" width="400"/>
<img src="screenshots/AtileHD_Config.jpg?sanitize=true&raw=true" title="AtileHD_Config" width="400"/>
<img src="screenshots/ChannelSelection.jpg?sanitize=true&raw=true" title="ChannelSelection" width="400"/>
<img src="screenshots/EPGSelection.jpg?sanitize=true&raw=true" title="EPGSelection" width="400"/>
<img src="screenshots/GraphMultiEPG.jpg?sanitize=true&raw=true" title="GraphMultiEPG" width="400"/>
<img src="screenshots/GraphMultiEPG1.jpg?sanitize=true&raw=true" title="GraphMultiEPG1" width="400"/>
<img src="screenshots/GraphMultiEPG2.jpg?sanitize=true&raw=true" title="GraphMultiEPG2" width="400"/>
<img src="screenshots/GraphMultiEPG3.jpg?sanitize=true&raw=true" title="GraphMultiEPG3" width="400"/>
<img src="screenshots/VerticalEPGView_FHD.jpg?sanitize=true&raw=true" title="VerticalEPGView_FHD" width="400"/>
<img src="screenshots/TimeshiftState.jpg?sanitize=true&raw=true" title="TimeshiftState" width="400"/>
<img src="screenshots/menu_mainmenu.jpg?sanitize=true&raw=true" title="menu_mainmenu" width="400"/>
<img src="screenshots/EPGSelectionMulti.jpg?sanitize=true&raw=true" title="EPGSelectionMulti" width="400"/>
</p>

## Farbstile
<p align="center">
<img src="screenshots/colors_Blue.jpg?sanitize=true&raw=true" title="colors_Blue" width="400"/>
<img src="screenshots/colors_Grey.jpg?sanitize=true&raw=true" title="colors_Grey" width="400"/>
<img src="screenshots/colors_Brown.jpg?sanitize=true&raw=true" title="colors_Brown" width="400"/>
<img src="screenshots/colors_Green.jpg?sanitize=true&raw=true" title="colors_Green" width="400"/>
<img src="screenshots/colors_Purple.jpg?sanitize=true&raw=true" title="colors_Purple" width="400"/>
<img src="screenshots/colors_Red.jpg?sanitize=true&raw=true" title="colors_Red" width="400"/>
<img src="screenshots/colors_Metrix_Retro.jpg?sanitize=true&raw=true" title="colors_Red" width="400"/>
<img src="screenshots/colors_Black.jpg?sanitize=true&raw=true" title="colors_Black" width="400"/>
</p>

## Changelog

### 0.9.5 BETA (28.05.2019)
* CutListeEditor skinned
* TaskListScreen bug fix
* SkinPart Poster in InfoBar anzeigen
* Einstellungen für Poster hinzugefügt
* SkinPart Plugin InfoBarTunerState by vu13
* Converter und zugehörige log Ausgabe optimiert 
* viele kleine Screen bug fixes

### 0.9.0 BETA (04.05.2019)
* EPGImport bug fix
* progressBarForeground zu colors hinzugefügt
* EPGSearch skinned
* AudioSelection bug fixed
* SystemInfos mehr Platz hinzugefügt
* Converter bug fixes und Verbesserungen
* EPG Info Anzeige erweitert (RatingsStars, RemainingTime, LeadText, Conclusion, etc.)
* SecondInfoBar neues Layout
* 2 SkinParts für SecondInfoBar Layout
* Skinpart für InfoBar von SleepyHellow
* Plugin CoverFind skinned
* Plugin MediaPlayer skinned
* Plugin Satfinder skinned
* viele kleine Screen bug fixes

### 0.8.0 BETA (18.04.2019)
* EPG Info Anzeige erweitert (SxxExx, Genre, Land, etc.)
* Plugin ChromiumOS, FileBrowserVTi, YoutubeTv skinned
* Moderne Logos in den einzelnen Screens hinzugefügt
* VerticalEPGView_FHD, GraphMultiEPG bug fixes
* Converter bug fixes
* viele kleine Screen bug fixes

### 0.7.0 BETA (08.04.2019)
* constant-widgets durch panels ersetzt -> Skin ist jetzt 100% kompatibel mit dem [OpenSkin-Designer](https://github.com/Humaxx/OpenSkin-Designer) (Version >= 3.2.0). Könnt ihr [hier downloaden](https://github.com/Humaxx/OpenSkin-Designer/releases)
* [Neues Hauptmenü Design](https://raw.githubusercontent.com/Scrounger/MetrixReloaded/master/screenshots/menu_mainmenu.jpg)
* Moderne Icons hinzugefügt - Vielen Dank an die Authoren! (Quellen: [iFlatFHD Hauptmenü Icons](https://www.vuplus-support.org/wbb4/index.php?thread/93005-iflatfhd-hauptmen%C3%BC-icons-v6-6-07-04-2019/&pageNo=1), [MyMetrix Hauptmenu Icons gepimpt by rennmaus und kleiner.teufel](https://www.vuplus-support.org/wbb4/index.php?thread/71023-mymetrix-hauptmenu-icons-gepimpt-by-rennmaus-und-kleiner-teufel/), [MetrixHD - simple Icons gepimpt by kleiner.teufel & rennmaus](https://www.vuplus-support.org/wbb4/index.php?thread/82277-metrixhd-simple-icons-gepimpt-by-kleiner-teufel-rennmaus/))
* Icon unhandled-key geändert - Vielen Dank an maggy (Quelle: [Unhandled Key Icons](https://www.vuplus-support.org/wbb4/index.php?thread/33779-unhandled-key-icons/))
* Plugin PiconManager hinzugefügt
* Systeminfos hinzugefügt
* SkinPart SystemInfo Full hinzugefügt
* Farbstil colors_Black bug fixes
* viele kleine Screen bug fixes

### 0.6.40 BETA (31.03.2019)
* Fehlende Dependencies hinzugefügt
* Autotimer screen bug fixes
* [Farbe Black hinzugefügt](https://raw.githubusercontent.com/Scrounger/MetrixReloaded/master/screenshots/colors_Black.jpg)
* Translator hinzugefügt
* kleinere bug fixes

### 0.6.0 BETA (26.03.2019)
* Fehlende Dependencies hinzugefügt
* Insatller bug fixes
* font_Fett bug fixed
* Farbe Metrix Retro hinzugefügt

### 0.5.0 BETA (24.03.2019)
* MetrixReloaded Einstellungen: selektierte Menu Einträge anzeigen
* Schriftart hinzugefügt
* SkinParts hinzugefügt
* Preview Images hinzugefügt
* Bug fixes

### 0.4.0 BETA (23.03.2019)
* MetrixReloaded Einstellungen: Screen Namen anzeigen
* Farb-Stile hinzugefügt
* Bug fixes

### 0.3.1 BETA (21.03.2019)
* Skin Updater bug fixes

### 0.3.0 BETA (21.03.2019)
* Skin Updater -> lädt neue version herunter
* ScreenFiles überarbeitet
* Bug fixes 

### 0.2.0 BETA (19.03.2019)
* erste veröffentlichte Version
* ca. 80% der Screens sind final
* Converter und Plugin enthalten

