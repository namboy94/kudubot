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
from plugins.GenericPlugin import GenericPlugin
from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class TheTVDB(GenericPlugin):
    """
    the TheTVDB class
    """

    def __init__(self, layer, message_protocol_entity=None):
        """
        Constructor
        :param layer: the overlying yowsup layer
        :param message_protocol_entity: the received message information
        :return: void
        """
        super().__init__(layer, message_protocol_entity)
        self.tvshow = ""
        self.season = ""
        self.episode = ""

    def regex_check(self):
        """
        Checks if the user input matches the regex needed for the plugin to function correctly
        :return: True if input is valid, False otherwise
        """
        regex = r"^/(tvdb) ([^ ]+| )+ s[0-9]{1,2} e[0-9]{1,4}$"
        if re.search(regex, self.message):
            return True
        else:
            return False

    def parse_user_input(self):
        """
        Parses the user input
        :return: void
        """
        self.tvshow = self.message.split(" ", 1)[1].rsplit(" s", 1)[0]
        self.season = int(self.message.rsplit("s", 1)[1].rsplit(" e", 1)[0])
        self.episode = int(self.message.rsplit("e", 1)[1])

    def get_response(self):
        """
        Fetches the episode name of a specific episode
        :return: the episode name as a textMessageProtocolEntity
        """
        try:
            tvdb = tvdb_api.Tvdb()
            episode_info = tvdb[self.tvshow][self.season][self.episode]
            episode_name = episode_info['episodename']
            return WrappedTextMessageProtocolEntity(episode_name, to=self.sender)
        except Exception as e:
            if "cannot find show on TVDB" in str(e):
                return WrappedTextMessageProtocolEntity("Show not found", to=self.sender)
            if "Could not find episode" in str(e):
                return WrappedTextMessageProtocolEntity("Episode not found", to=self.sender)
            if "Could not find season" in str(e):
                return WrappedTextMessageProtocolEntity("Season not found", to=self.sender)
            print(str(e))

    @staticmethod
    def get_description(language):
        """
        Returns a description about this plugin
        :param language: the language in which to display the description
        :return the description in the specified language
        """
        if language == "en":
            return "/tvdb\tSends episode name of an episode from TVDB\n" \
                   "syntax: /tvdb <show> s<season> e<episode>"
        elif language == "de":
            return "/tvdb\tSchickt den Episodennamen einer Episode auf TVDB\n" \
                   "syntax: /tvdb <show> s<staffel> e<episode>"
        else:
            return "Help not available in this language"
