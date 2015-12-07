"""
Class that provides Football (mostly Bundesliga) Information

@author Hermann Krumrey <hermann@krumreyh.com>
"""

from bs4 import BeautifulSoup
import requests

"""
FootballScores class
"""
class FootballScores(object):

    """
    Constructor (Does nothing)
    """
    def __init__(self, userInput):
        self.bundesliga = False
        if not len(userInput.split(" ")) == 1 and not "bundesliga" in userInput:
            countryLeague = userInput.split(" ", 1)[1]
            self.country = countryLeague.split(", ")[0]
            self.league = countryLeague.split(", ")[1]
        else:
            self.bundesliga = True

        self.mode = userInput.split(" ")[0].lower()
        if self.mode in ["tabelle", "spieltag"]: self.lang = "de"
        else: self.lang = "en"

    """
    Returns the result of the user defined search
    """
    def getResult(self):
        if self.bundesliga:
            if self.mode in ["tabelle", "table"]:
                return self.getBundesligaTable()
            if self.mode in ["spieltag", "matchday"]:
                return self.getBundesligaScores()
        else:
            if self.mode in ["table", "tabelle"]:
                return self.getGenericTable()
            if self.mode in ["matchday", "spieltag"]:
                return self.getGenericMatchDay()

    """
    Fetches data for the current Bundesliga match day and returns it
    """
    def getBundesligaScores(self):

        returnString = ""

        url = "http://www.livescore.com/soccer/germany/bundesliga/"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        res = soup.select('.row-gray')

        i = 0
        for r in res:
            if i < 9:
                returnString += r.text + "\n"
                i += 1

        return self.makeBundesligaReadable(returnString)

    def getBundesligaTable(self):

        returnString = ""

        url = "http://www.livescore.com/soccer/germany/bundesliga/"

        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        teamres = soup.select('.team')
        ptsres = soup.select('.pts')

        i = 1 #teamnames
        j = 15 #points
        k = 12 #goals for
        l = 13 #goals against
        while i < 19:
            place = str(i) + ".\t"
            team = self.makeBundesligaReadable(teamres[i].text)
            points = ptsres[j].text
            goalsFor = ptsres[k].text
            goalsAgainst = ptsres[l].text
            spacer = "\t"
            if len(goalsAgainst + goalsFor) < 4: spacer += "\t"
            returnString += place + goalsFor + ":" + goalsAgainst + spacer + points + "\t" + team + "\n"
            i += 1; j += 8; k += 8; l += 8

        return self.makeBundesligaReadable(returnString)

    """
    Replaces Names of clubs that are simply too long, or English
    """
    def makeBundesligaReadable(self, string):

        returnString = string
        returnString = returnString.replace("Borussia Moenchengladbach", "Gladbach")
        returnString = returnString.replace("Bayern Munich", "FC Bayern München")
        returnString = returnString.replace("FC Cologne", "1.FC Köln")
        return returnString

    def getGenericMatchDay(self):

        returnString = ""

        url = "http://www.livescore.com/soccer/" + self.country + "/" + self.league + "/"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        res = soup.select('.row-gray')

        for r in res:
            returnString += r.text + "\n"

        return self.makeBundesligaReadable(returnString)

    def getGenericTable(self):

        returnString = ""

        url = "http://www.livescore.com/soccer/germany/" + self.country + "/" + self.league + "/"

        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        teamres = soup.select('.team')

        i = 1
        for team in teamres:
            returnString += str(i) + ".\t" + team
            i += 1

        return returnString
