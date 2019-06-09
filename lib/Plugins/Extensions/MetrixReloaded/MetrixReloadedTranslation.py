from Components.Language import language
import gettext
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from os import environ

# language
lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("MetrixReloaded", "%s%s" % (
    resolveFilename(SCOPE_PLUGINS), "Extensions/MetrixReloaded/locale/"))

def _(txt):
    t = gettext.dgettext("MetrixReloaded", txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t