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

from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin
from utils.math.Randomizer import Randomizer

"""
The SimpleEqualsResponse Class
"""
class SimpleEqualsResponse(GenericPlugin):

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
        self.message = self.entity.getBody()
        self.minMessage = self.message.lower()
        self.sender = self.entity.getFrom()

        self.caseInsensitiveOptions = [[["uptime"], ["Much too long, I'm tired"]]]
        self.caseSensitiveOptions = [[["ping"], ["pong"]],
                                     [["Ping"], ["Pong"]]]

    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):
        for option in self.caseSensitiveOptions:
            for opt in option[0]:
                if self.message == opt:
                    return True
        for option in self.caseInsensitiveOptions:
            for opt in option[0]:
                if self.minMessage == opt:
                    return True
        return False

    """
    Parses the user's input
    @:override
    """
    def parseUserInput(self):
        for option in self.caseSensitiveOptions:
            for opt in option[0]:
                if self.message == opt:
                    self.response = Randomizer.getRandomElement(option[1])
                    return
        for option in self.caseInsensitiveOptions:
            for opt in option[0]:
                if self.minMessage == opt:
                    self.response = Randomizer.getRandomElement(option[1])
                    return

    """
    Returns the response calculated by the plugin
    @:return the response as a MessageProtocolEntity
    @:override
    """
    def getResponse(self):
        return TextMessageProtocolEntity(self.response, to=self.sender)

    """
    Empty description
    @:param language - the language to be returned
    @:return the description as string
    @:override
    """
    @staticmethod
    def getDescription(language):
        return ""
