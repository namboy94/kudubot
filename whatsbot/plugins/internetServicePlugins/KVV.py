# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsbot.

    whatsbot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsbot.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
from plugins.GenericPlugin import GenericPlugin
from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class KVV(GenericPlugin):
    """
    The KVV Class
    """

    def __init__(self, layer, message_protocol_entity=None):
        """
        Constructor
        Defines parameters for the plugin.
        :param layer: the overlying yowsup layer
        :param message_protocol_entity: the received message information
        :return: void
        """
        super().__init__(layer, message_protocol_entity)
        self.station = ""

    def regex_check(self):
        """
        Checks if the user input is valid for this plugin to continue
        :return: True if input is valid, False otherwise
        """
        return re.search(r"^/kvv [^ ]+", self.message)

    def parse_user_input(self):
        """
        Parses the user's input
        :return: void
        """
        self.station = self.message.split("/kvv ", 1)[1]

    def get_response(self):
        """
        Returns the station input by the user, and adds "!kvv " to it
        :return: the response as a MessageProtocolEntity
        """
        return WrappedTextMessageProtocolEntity("!kvv " + self.station, to=self.sender)

    @staticmethod
    def get_description(language):
        """
        Returns a helpful description of the plugin's syntax and functionality
        :param language: the language to be returned
        :return: the description as string
        """
        if language == "en":
            return "/kvv\tUses Johannes bucher's whatsbot to display kvv times\n" \
                   "syntax: /kvv <station>"
        elif language == "de":
            return "/kvv\tBenutzt Johannes Buchers whatsbot um KVV Zeiten anzuzeigen\n" \
                   "syntax: /kvv <station>"
        else:
            return "Help not available in this language"
