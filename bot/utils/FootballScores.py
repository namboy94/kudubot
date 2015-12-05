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
    def __init__(self):
        print()

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

        teamurl = "http://www.livescore.com/soccer/germany/bundesliga/"
        teamhtml = requests.get(teamurl).text
        teamsoup = BeautifulSoup(teamhtml, "html.parser")
        teamres = teamsoup.select('.team')

        ptsurl = "http://www.livescore.com/soccer/germany/bundesliga/"
        ptshtml = requests.get(ptsurl).text
        ptssoup = BeautifulSoup(ptshtml, "html.parser")
        ptsres = ptssoup.select('.pts')

        i = 1 #teamnames
        j = 15 #points
        k = 12 #goals for
        l = 13 #goals against
        while i < 19:
            place = str(i) + ". "
            team = self.makeBundesligaReadable(teamres[i].text)
            team = self.formatNameForTable(team)
            points = ptsres[j].text
            goalsFor = ptsres[k].text
            goalsAgainst = ptsres[l].text
            spacer = "\t"
            if len(goalsAgainst + goalsFor) < 4: spacer += "\t"
            returnString += place + team + goalsFor + ":" + goalsAgainst + spacer + points + "\n"
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

    def formatNameForTable(self, string):

        bundesLigaDict = {"FC Bayern München": "\t",
                          "Borussia Dortmund": "\t",
                          "Gladbach": "\t\t\t",
                          "Hertha Berlin": "\t\t",
                          "Wolfsburg": "\t\t\t",
                          "Schalke 04": "\t\t\t",
                          "Mainz 05": "\t\t\t",
                          "Bayer Leverkusen": "\t",
                          "Hamburger SV": "\t\t",
                          "1.FC Köln": "\t\t\t",
                          "Ingolstadt": "\t\t\t",
                          "Darmstadt": "\t\t\t",
                          "Eintracht Frankfurt": "\t",
                          "Hannover 96": "\t\t",
                          "Augsburg": "\t\t\t",
                          "Werder Bremen": "\t",
                          "Hoffenheim": "\t\t",
                          "VfB Stuttgart": "\t\t"
                          }

        return string + bundesLigaDict[string]
