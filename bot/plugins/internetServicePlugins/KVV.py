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
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin

"""
The KVV Class
"""
class KVV(GenericPlugin):

    """
    Constructor
    Defines parameters for the plugin.
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the received message information
    """
    def __init__(self, layer, messageProtocolEntity=None):
        #add this to the top:
        if messageProtocolEntity is None: self.layer = layer; return
        self.layer = layer
        self.entity = messageProtocolEntity
        self.message = self.entity.getBody()
        self.sender = self.entity.getFrom()

    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):
        return re.search(r"^/kvv [^ ]+", self.message)

    """
    Parses the user's input
    @:override
    """
    def parseUserInput(self):
        self.station = self.message.split("/kvv ", 1)[1]


    """
    Returns the station input by the user, and adds "!kvv " to it
    @:return the response as a MessageProtocolEntity
    @:override
    """
    def getResponse(self):
        return TextMessageProtocolEntity("!kvv " + self.station, to=self.sender)

    """
    Returns a helpful description of the plugin's syntax and functionality
    @:param language - the language to be returned
    @:return the description as string
    @:override
    """
    @staticmethod
    def getDescription(language):
        if language == "en":
            return "/kvv\tUses Johannes bucher's bot to display kvv times\n" \
                   "syntax: /kvv <station>"
        elif language == "de":
            return "/kvv\tBenutzt Johannes Buchers bot um KVV Zeiten anzuzeigen\n" \
                   "syntax: /kvv <station>"
        else:
            return "Help not available in this language"