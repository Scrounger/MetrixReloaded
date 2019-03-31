# MetrixReloaded
[![GitHub release](https://img.shields.io/github/release/Scrounger/MetrixReloaded.svg)](https://github.com/Scrounger/MetrixReloaded/releases)
[![GitHub All Releases](https://img.shields.io/github/downloads/Scrounger/MetrixReloaded/total.svg)](https://github.com/Scrounger/MetrixReloaded/releases)
[![GitHub Releases (by Release)](https://img.shields.io/github/downloads/Scrounger/MetrixReloaded/0.6.40/total.svg)](https://github.com/Scrounger/MetrixReloaded/releases)
![GitHub repo size](https://img.shields.io/github/repo-size/Scrounger/MetrixReloaded.svg)
![GitHub](https://img.shields.io/github/license/Scrounger/MetrixReloaded.svg)

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

## Installation

##### benötigte Plugins:
Achtung! Folgende Plugins müssen auf Eurem System installiert sein, damit der Skin funktioniert:
* ExtendedEventInfoHandler >= Version 2.3<br>(Installieren über *Erweiterungen -> rote Taste -> Systemerweiterungen -> exteventinfohandler*)

1. Ladet euch die [aktuelle Version](https://github.com/Scrounger/MetrixReloaded/releases) herunter.
2. Kopiert die heruntergeladene *.ipk Datei in das /tmp/ Vereichnis auf Euren VU+ Receiver
3. Öffne das VtiPanel (Blaue Taste) -> *Manuelle Installation von Paketen* -> *IPKG-Pakete installieren*
4. Wähle die *.ipk Datei aus und starte die Installation

## Einstellungen
<img src="screenshots/MetrixReloadedSetup.jpg?sanitize=true&raw=true" title="MetrixReloadedSetup" width="600"/>

Unter *Erweiterungen* -> *MetrixReloaded* findest du zusätzliche Einstellungen für den Skin. Die Einstellungen sind dort ausführlich beschrieben, sobald du diese anwählst

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

