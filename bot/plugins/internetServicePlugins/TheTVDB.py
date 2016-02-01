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
import tvdb_api
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin

"""
the TheTVDB class
"""
class TheTVDB(GenericPlugin):

    """
    Constructor
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

        self.tvshow = ""
        self.season = ""
        self.episode = ""

    """
    Checks if the user input matches the regex needed for the plugin to function correctly
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):
        regex = r"^/(tvdb) ([^ ]+| )+ s[0-9]{1,2} e[0-9]{1,4}$"
        if re.search(regex, self.message): return True
        else: return False

    """
    Parses the user input
    @:override
    """
    def parseUserInput(self):
        self.tvshow = self.message.split(" ", 1)[1].rsplit(" s", 1)[0]
        self.season = int(self.message.rsplit("s", 1)[1].rsplit(" e", 1)[0])
        self.episode = int(self.message.rsplit("e", 1)[1])

    """
    Fetches the episode name of a specific episode
    @:return the episode name as a textMessageProtocolEntity
    @:override
    """
    def getResponse(self):

        try:
            tvdb = tvdb_api.Tvdb()
            episodeInfo = tvdb[self.tvshow][self.season][self.episode]
            episodeName = episodeInfo['episodename']
            return TextMessageProtocolEntity(episodeName, to=self.sender)
        except Exception as e:
            if "cannot find show on TVDB" in str(e):
                return TextMessageProtocolEntity("Show not found", to=self.sender)
            if "Could not find episode" in str(e):
                return TextMessageProtocolEntity("Episode not found", to=self.sender)
            if "Could not find season" in str(e):
                return TextMessageProtocolEntity("Season not found", to=self.sender)
            print(str(e))

    """
    Returns a description about this plugin
    @:param language - the language in which to display the description
    @:return the description in the specified language
    @:override
    """
    @staticmethod
    def getDescription(language):
        if language == "en":
            return "/tvdb\tSends episode name of an episode from TVDB\n" \
                   "syntax: /tvdb <show> s<season> e<episode>"
        elif language == "de":
            return "/tvdb\tSchickt den Episodennamen einer Episode auf TVDB\n" \
                   "syntax: /tvdb <show> s<staffel> e<episode>"
        else:
            return "Help not available in this language"
