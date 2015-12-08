"""
Class that retrieves information from the KIT Mensa webpage
"""

from bs4 import BeautifulSoup
import requests

class Mensa(object):

    def __init__(self, userInput):
        self.userInput = userInput
        self.future = False
        self.mode = "all"
        self.parseUserInput()
        self.getTodaysPlan()

    def parseUserInput(self):
        splitInput = self.userInput.split(" ", 1)
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

    def getResponse(self):

        nl = "\n"
        if self.mode == "all": return self.linie1 + nl + self.linie2 + nl + self.linie3 + nl + self.linie45 + nl \
                                      + self.linie6 + nl + self.linieschnitzel + nl + self.liniecurry + nl + \
                                      self.linieabend + nl + self.liniecafeteria + nl + self.liniecafeteria1430
        elif self.mode == "1": return self.linie1
        elif self.mode == "2": return self.linie2
        elif self.mode == "3": return self.linie3
        elif self.mode == "45": return self.linie45
        elif self.mode == "6": return self.linie6
        elif self.mode == "schnitzel": return self.linieschnitzel
        elif self.mode == "curry": return self.liniecurry
        elif self.mode == "abend": return self.linieabend
        elif self.mode == "cafeteriavm": return self.liniecafeteria
        elif self.mode == "cafeteriavm": return self.liniecafeteria1430
        else: return False

