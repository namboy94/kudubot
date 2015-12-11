"""
Class that retrieves information from the KIT Mensa webpage
@:author Hermann Krumrey<hermann@krumreyh.com>
"""
import requests
import re
from bs4 import BeautifulSoup
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin

"""
the Mensa class
"""
class Mensa(GenericPlugin):

    """
    Constructor
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the received message information
    @:override
    """
    def __init__(self, layer, messageProtocolEntity=None):
        if messageProtocolEntity is None: self.layer = layer; return
        self.future = False
        self.mode = "all"

        self.layer = layer
        self.entity = messageProtocolEntity
        self.message = self.entity.getBody().lower()
        self.sender = self.entity.getFrom()

        self.linie1 = ""
        self.linie2 = ""
        self.linie3 = ""
        self.linie45 = ""
        self.linie6 = ""
        self.linieschnitzel = ""
        self.linieabend = ""
        self.liniecurry = ""
        self.liniecafeteria = ""
        self.liniecafeteria1430 = ""

    """
    Checks if the user input matches the regex needed for the plugin to function correctly
    @:override
    """
    def regexCheck(self):
        regex = r"^/(mensa)( )?(linie (1|2|3|4|5|6)|schnitzelbar|curry queen|abend|cafeteria vormittag|cafeteria nachmittag)?( morgen)?$"
        if re.search(regex, self.message): return True
        else: return False

    """
    Parses the user input
    @:override
    """
    def parseUserInput(self):
        splitInput = self.message.split(" ", 1)
        if len(splitInput) == 1: self.mode = "all"
        else:
            arg = splitInput[1]
            if "morgen" in arg: self.future = True
            if arg == "all" or arg == "alle": self.mode = "all"
            elif "1" in arg: self.mode = "1"
            elif "2" in arg: self.mode = "2"
            elif "3" in arg: self.mode = "3"
            elif "4" in arg or "5" in arg: self.mode = "45"
            elif "schnitzel" in arg: self.mode = "schnitzel"
            elif "6" in arg: self.mode = "6"
            elif "abend" in arg: self.mode = "abend"
            elif "curry" in arg: self.mode = "curry"
            elif "cafeteria" in arg and not "nachmittag" in arg: self.mode = "cafeteriavm"
            elif "cafeteria" in arg and "nachmittag" in arg: self.mode = "cafeterianm"
        self.getTodaysPlan()

    """
    Decides which information to send back to the user
    @:return the message to be sent back as a TextMessageProtocolEntity
    @:override
    """
    def getResponse(self):

        message = ""
        nl = "\n"
        if self.mode == "all": message = self.linie1 + nl + self.linie2 + nl + self.linie3 + nl + self.linie45 + nl \
                                      + self.linie6 + nl + self.linieschnitzel + nl + self.liniecurry + nl + \
                                      self.linieabend + nl + self.liniecafeteria + nl + self.liniecafeteria1430
        elif self.mode == "1": message = self.linie1
        elif self.mode == "2": message = self.linie2
        elif self.mode == "3": message = self.linie3
        elif self.mode == "45": message = self.linie45
        elif self.mode == "6": message = self.linie6
        elif self.mode == "schnitzel": message = self.linieschnitzel
        elif self.mode == "curry": message = self.liniecurry
        elif self.mode == "abend": message = self.linieabend
        elif self.mode == "cafeteriavm": message = self.liniecafeteria
        elif self.mode == "cafeteriavm": message = self.liniecafeteria1430

        return TextMessageProtocolEntity(message, to=self.sender)


    """
    Returns a description about this plugin
    @:override
    """
    @staticmethod
    def getDescription(language):
        if language == "en":
            return "syntax: /mensa [<linie>] [morgen]\n\n" \
                   "/table\tSends football table information\n"
        elif language == "de":
            return "/mensa\tSchickt den Mensa Plan\n" \
                   "syntax: /mensa [<linie>] [morgen]\n\n"
        else:
            return "Help not available in this language"

    ### Private Methods ###


    """
    Retrieves the information about today's (or tomorrow's) mensa plan
    """
    def getTodaysPlan(self):

        if self.future: url = "http://mensa.akk.uni-karlsruhe.de/?DATUM=morgen&uni=1"
        else: url = "http://mensa.akk.uni-karlsruhe.de/?DATUM=heute&uni=1"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        res = soup.select('body')
        body = res[0].text

        self.linie1 = "Linie 1\n" + body.split("Linie 1:\n", 1)[1].split("Linie 2:", 1)[0]
        self.linie2 = "Linie 2\n" + body.split("Linie 2:\n", 1)[1].split("Linie 3:", 1)[0]
        self.linie3 = "Linie 3\n" + body.split("Linie 3:\n", 1)[1].split("Linie 4/5:", 1)[0]
        self.linie45 = "Linie 4/5\n" + body.split("Linie 4/5:\n", 1)[1].split("Schnitzelbar:", 1)[0]
        self.linieschnitzel = "Schnitzelbar\n" + body.split("Schnitzelbar:\n", 1)[1].split("L6 Update:", 1)[0]
        self.linie6 = "L6 Update\n" + body.split("L6 Update:\n", 1)[1].split("Abend:", 1)[0]
        self.linieabend = "Abend\n" + body.split("Abend:\n", 1)[1].split("Curry Queen:", 1)[0]
        self.liniecurry = "Curry Queen\n" + body.split("Curry Queen:\n", 1)[1].split("Cafeteria Heiße Theke:", 1)[0]
        self.liniecafeteria = "Cafeteria Heiße Theke\n" + body.split("Cafeteria Heiße Theke:\n", 1)[1].split("Cafeteria ab 14:30:", 1)[0]
        self.liniecafeteria1430 = "Cafeteria ab 14:30\n" + body.split("Cafeteria ab 14:30:\n", 1)[1].split("Stand:", 1)[0]

        return "Curry Queen\nSchnitzel-Bar"


