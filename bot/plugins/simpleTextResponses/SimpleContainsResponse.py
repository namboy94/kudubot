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

import random
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from utils.math.Randomizer import Randomizer
from plugins.GenericPlugin import GenericPlugin

"""
The SimpleContainsResponse Class
"""
class SimpleContainsResponse(GenericPlugin):

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

        self.response = ""
        self.caseInsensitiveOptions = \
                [[["keks", "cookie"], ["Ich will auch Kekse!",
                                        "Wo gibt's Kekse?",
                                        "Kekse sind klasse!",
                                        "Ich hab einen Gutschein für McDonald's Kekse!",
                                        "🍪"]],
                [["kuchen", "cake"], ["Ich mag Kuchen",
                                        "Marmorkuchen!",
                                        "Kuchen gibt's bei Starbucks"]],
                [["ups", "oops", "uups"], ["Was hast du jetzt schon wieder kaputt gemacht?"]],
                [["wuerfel", "würfel"], ["Würfel sind toll",
                                        "Du hast eine " + str(random.randint(1,6)) + " gewürfelt!",
                                        "https://play.google.com/store/apps/details?id=com.namibsun.android.dice"]],
                [["😂"], ["😂😂😂"]],
                [["🖕🏻"], ["😡🖕🏻"]],
                [["beste bot", "bester bot"], ["😘"]],
                [["chicken", "nuggets", "huhn", "hühnchen"], ["🐤", "Die armen Kücken!\n🐤🐤🐤"]],
                [["scheiße", "kacke"], ["💩"]]]
        self.caseSensitiveOptions = [[[], []]]

    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):
        matches = 0
        for option in self.caseSensitiveOptions:
            match = False
            for opt in option[0]:
                if opt in self.message:
                    match = True
            if match: matches += 1
        for option in self.caseInsensitiveOptions:
            match = False
            for opt in option[0]:
                if opt in self.minMessage:
                    match = True
            if match: matches += 1
        if matches == 1: return True
        else: return False

    """
    Parses the user's input
    @:override
    """
    def parseUserInput(self):
        for option in self.caseSensitiveOptions:
            for opt in option[0]:
                if opt in self.message:
                    self.response = Randomizer.getRandomElement(option[1])
                    return
        for option in self.caseInsensitiveOptions:
            for opt in option[0]:
                if opt in self.minMessage:
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
    Empty Description
    @:param language - the language to be returned
    @:return the description as string
    @:override
    """
    @staticmethod
    def getDescription(language):
        return ""