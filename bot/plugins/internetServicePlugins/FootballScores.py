# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsapp-bot.

    whatsapp-bot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsapp-bot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsapp-bot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsapp-bot.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
import requests
from bs4 import BeautifulSoup
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin

"""
FootballScores class
"""
class FootballScores(GenericPlugin):

    """
    Constructor
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the received message information
    @:override
    """
    def __init__(self, layer, messageProtocolEntity=None):
        if not messageProtocolEntity: self.layer = layer; return
        self.bundesliga = False
        self.lang = "en"

        self.layer = layer
        self.entity = messageProtocolEntity
        self.message = self.entity.getBody()
        self.sender = self.entity.getFrom()

        self.country = ""
        self.league = ""

    """
    Checks if the user input matches the regex needed for the plugin to function correctly
    @:return True if the regex matches, False otherwise
    @:override
    """
    def regexCheck(self):
        regex = r"^/(table|tabelle|spieltag|matchday)( [^ ]+, [^ ]+)?$"
        if re.search(regex, self.message): return True
        else: return False

    """
    Parses the user input
    @:override
    """
    def parseUserInput(self):
        if not len(self.message.split(" ")) == 1 and not "bundesliga" in self.message:
            countryLeague = self.message.split(" ", 1)[1]
            self.country = countryLeague.split(", ")[0]
            self.league = countryLeague.split(", ")[1]
        else:
            self.bundesliga = True

        self.mode = self.message.split(" ")[0].split("/")[1].lower()
        if self.mode in ["tabelle", "spieltag"]: self.lang = "de"

    """
    Returns the result of the user defined search
    @:return the result of the user defined search
    A:override
    """
    def getResponse(self):
        response = ""
        if self.bundesliga:
            if self.mode in ["tabelle", "table"]:
                response = self.__getBundesLigaTable__()
            if self.mode in ["spieltag", "matchday"]:
                response = self.__getBundesligaMatchDay__()
        else:
            if self.mode in ["table", "tabelle"]:
                response = self.__getGenericTable__()
            if self.mode in ["matchday", "spieltag"]:
                response = self.__getGenericMatchDay__()
        return TextMessageProtocolEntity(response, to=self.sender)

    """
    Returns a description about this plugin
    @:param language - the language in which to display the description
    @:return the description in the specified language
    @:override
    """
    @staticmethod
    def getDescription(language):
        if language == "en":
            return "/table\tSends football table information\n" \
                   "syntax: /table [<country>][, <league>]\n\n" \
                   "/matchday\tSends football matchday information\n" \
                   "syntax: /matchday [<country>][, <league>]"
        elif language == "de":
            return "/tabelle\tSchickt Fußball Tabelleninformationen\n" \
                   "syntax: /tabelle [<land>][, <league>]\n\n" \
                   "/spieltag\tSchickt Fußball Spieltaginformationen\n" \
                   "syntax: /spieltag [<country>][, <league>]"
        else:
            return "Help not available in this language"

    ### Private Methods ###

    """
    Fetches the current bundesliga table
    @return: a formatted string containing the bundesliga table
    """
    def __getBundesLigaTable__(self):

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
            team = self.__makeBundesligaReadable__(teamres[i].text)
            points = ptsres[j].text
            goalsFor = ptsres[k].text
            goalsAgainst = ptsres[l].text
            spacer = "\t"
            if len(goalsAgainst + goalsFor) < 4: spacer += "\t"
            returnString += place + goalsFor + ":" + goalsAgainst + spacer + points + "\t" + team + "\n"
            i += 1; j += 8; k += 8; l += 8

        return self.__makeBundesligaReadable__(returnString)

    """
    Fetches data for the current Bundesliga match day and returns it
    @:return the bundesliga matchday scores
    """
    def __getBundesligaMatchDay__(self):

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

        return self.__makeBundesligaReadable__(returnString)

    """
    Replaces Names of clubs that are simply too long, or English
    @:return the replaced name
    """
    def __makeBundesligaReadable__(self, string):

        returnString = string
        returnString = returnString.replace("Borussia Moenchengladbach", "Gladbach")
        returnString = returnString.replace("Bayern Munich", "F\0C\0 B\0a\0y\0e\0r\0n M\0ü\0n\0c\0hen") #Overliste Johannes' Bot.
        returnString = returnString.replace("FC Cologne", "1.FC Köln")
        return returnString

    """
    Fetches information about a generic country/league matchday
    @:return the matchday as string
    """
    def __getGenericMatchDay__(self):

        returnString = ""

        url = "http://www.livescore.com/soccer/" + self.country + "/" + self.league + "/"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        res = soup.select('.row-gray')

        for r in res:
            returnString += r.text + "\n"

        return returnString

    """
    Fetches the information about a generic country/league table
    @:return the league table as string
    """
    def __getGenericTable__(self):

        returnString = ""

        url = "http://www.livescore.com/soccer/" + self.country + "/" + self.league + "/"

        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        teamres = soup.select('.team')

        i = 1
        while i < len(teamres):
            returnString += str(i) + ".\t" + teamres[i].text + "\n"
            i += 1

        return returnString
