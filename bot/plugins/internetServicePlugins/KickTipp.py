# coding=utf-8

"""
Plugin that fetches information from kicktipp.de
@author Hermann Krumrey <hermann@krumreyh.com>
"""

import re
import requests
from bs4 import BeautifulSoup
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin

"""
The KickTipp Class
"""
class KickTipp(GenericPlugin):

    """
    Constructor
    Defines parameters for the plugin.
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the received message information
    @:override
    """
    def __init__(self, layer, messageProtocolEntity=None):
        if messageProtocolEntity is None: self.layer = layer; return
        self.layer = layer
        self.entity = messageProtocolEntity
        self.message = self.entity.getBody().lower()
        self.sender = self.entity.getFrom()

        self.community = ""

    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):
        if self.message.startswith("/kicktipp "):
            return True
        else:
            return False

    """
    Parses the user's input
    @:override
    """
    def parseUserInput(self):
        self.community = self.message.split("/kicktipp ")[1]

    """
    Returns the response calculated by the plugin
    @:return the response as a MessageProtocolEntity
    @:override
    """
    def getResponse(self):
        return TextMessageProtocolEntity(self.__getTable__(), to=self.sender)

    """
    Returns a helpful description of the plugin's syntax and functionality
    @:param language - the language to be returned
    @:return the description as string
    @:override
    """
    @staticmethod
    def getDescription(language):
        if language == "en":
            return "/kicktipp\tFetches Kicktipp Community Tables\n" \
                   "syntax: /kicktipp <kicktipp-community>"
        elif language == "de":
            return "/kicktipp\tZeigt Kicktipp Community Tabellen\n" \
                   "syntax: /kicktipp <kicktipp-community>"
        else:
            return "Help not available in this language"

    ### Local Methods ###

    """
    Fetches the current table of the given kicktipp communiy
    @:return the table as formatted string.
    """
    def __getTable__(self):
        html = requests.get("http://www.kicktipp.de/" + self.community + "/tippuebersicht").text
        soup = BeautifulSoup(html, "html.parser")
        names = soup.select(".mg_class")
        scores1 = soup.select(".pkt")
        scores2 = soup.select(".pkts")

        i = 0
        j = 0
        k = 0

        returnString = ""

        while i<len(names):
            returnString += str(i + 1) + ".    "
            if re.search(r"[0-9]+,[0-9]+", scores1[j].text):
                returnString += scores2[k].text + "    "
                returnString += scores1[j].text + "    "
                returnString += scores1[j+1].text + "    "
                k+=1
                j+=2
            else:
                returnString += scores1[j].text + "    "
                returnString += scores1[j+1].text + "    "
                returnString += scores1[j+2].text + "    "
                j+=3
            returnString += names[i].text + "\n"
            i+=1

        return returnString