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
from utils.encoding.Unicoder import Unicoder
from utils.contacts.AddressBook import AddressBook

"""
The Muter Class
"""
class Muter(GenericPlugin):

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

        self.authenticated = False

    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):
        if self.message in ["/unmute", "/mute"]:
            return True
        else: return False

    """
    Parses the user's input
    @:override
    """
    def parseUserInput(self):
        self.authenticated = AddressBook().isAuthenticated(self.entity.getFrom(False)) \
                             or AddressBook().isAuthenticated(self.entity.getParticipant())

        if self.authenticated:
            if self.message == "/unmute":
                self.layer.muted = False
            elif self.message == "/mute":
                self.layer.muted = True

    """
    Returns the response calculated by the plugin
    @:return the response as a MessageProtocolEntity
    @:override
    """
    def getResponse(self):
        if self.layer.muted:
            messageProtocolEntity = TextMessageProtocolEntity("🤐", to=self.sender)
            messageProtocolEntity = Unicoder.fixOutgoingEntity(messageProtocolEntity)
            self.sendMessage(messageProtocolEntity)
            return messageProtocolEntity

        else:
            return TextMessageProtocolEntity("😄", to=self.sender)

    """
    Returns a helpful description of the plugin's syntax and functionality
    @:param language - the language to be returned
    @:return the description as string
    @:override
    """
    @staticmethod
    def getDescription(language):
        if language == "en":
            return "/mute\tmutes the bot (admin)\n" \
                   "/unmute\tunmutes the bot (admin)\n"
        elif language == "de":
            return "/mute\tStellt den Bot auf lautlos (admin)\n" \
                   "/unmute\tHolt den Bot wieder aus dem Lautlosmodus aus (admin)\n"
        else:
            return "Help not available in this language"