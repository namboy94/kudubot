"""
Class that handles the /help command
@author Hermann Krumrey<hermann@krumreyh.com>
"""

"""
The CommandHelper Class
"""
class CommandHelper(object):

    """
    Constructor
    @:param userInput - the user input, used to establish the language to use
    """
    def __init__(self, userInput):
        self.language = "en"
        if userInput == "hilfe": self.language = "de"

    """
    Generates the help string
    @:param the help string
    """
    def generateHelp(self):

        if self.language == "en":
            return "Commands:\n\n\n" \
                   "/help\tSends this help message\n\n" \
                   "/(wetter|weather)\tSends weather information\n" \
                   "syntax:\t/weather[:][options;] <cityname>[, <region>][, <country>]\n" \
                   "options: text,verbose\n\n" \
                   "/mensa\tSends Mensa Information\n" \
                   "syntax: /mensa [<linie>] [morgen]\n\n" \
                   "/tvdb\tSends episode name of an episode from TVDB\n" \
                   "syntax: /tvdb <show> s<season> e<episode>\n\n" \
                   "/table\tSends football table information\n" \
                   "syntax: /table [<country>][, <league>]\n\n" \
                   "/matchday|\tSends football matchday information\n" \
                   "syntax: /matchday [<country>][, <league>]\n\n" \
                   "/remind\tSaves a reminder and sends it back at the specified time\n" \
                   "syntax: /remind \"<message>\" <time>\n" \
                   "time syntax: <YYYY-MM-DD-hh-mm-ss>\n" \
                   "or: <amount> [years|months|days|hours|minutes|seconds]"

        elif self.language == "de":
            return "Befehle:\n\n\n" \
                   "/help\tSchickt diese Hilfsnachricht\n\n" \
                   "/wetter\tSchickt Wetterinformationen\n" \
                   "syntax:\t/wetter[optionen;] <stadtname>[, <region>][, <land>]\n" \
                   "options: text,verbose\n\n" \
                   "/mensa\tSchickt den Mensa Plan\n" \
                   "syntax: /mensa [<linie>] [morgen]\n\n" \
                   "/tvdb\tSchickt den Episodennamen einer Episode auf TVDB\n" \
                   "syntax: /tvdb <show> s<staffel> e<episode>\n\n" \
                   "/tabelle\tSchickt Fußball Tabelleninformationen\n" \
                   "syntax: /tabelle [<land>][, <league>]\n\n" \
                   "/spieltag\tSchickt Fußball Spieltaginformationen\n" \
                   "syntax: /spieltag [<country>][, <league>]\n\n" \
                   "/remind\tSpeichert eine Erinnerung und verschickt diese zum angegebenen Zeitpunkt\n" \
                   "syntax: /remind \"<nachricht>\" <zeit>\n" \
                   "zeit syntax: YYYY-MM-DD-hh-mm-ss\n" \
                   "oder: <anzahl> [jahre|monate|tage|stunden|minuten|sekunden]"

        else: return "This language is currently not supported"