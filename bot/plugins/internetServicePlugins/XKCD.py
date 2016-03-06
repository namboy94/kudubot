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
from plugins.GenericPlugin import GenericPlugin
from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class XKCD(GenericPlugin):
    """
    The XKCD Class
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
        self.comic = 0

    def regex_check(self):
        """
        Checks if the user input is valid for this plugin to continue
        :return: True if input is valid, False otherwise
        """
        return re.search(r"^/xkcd [0-9]+$", self.message)

    def parse_user_input(self):
        """
        Parses the user's input
        :return: void
        """
        self.comic = int(self.message.split("/xkcd ")[1])

    def get_response(self):
        """
        Returns the response calculated by the plugin
        :return: the response as a MessageProtocolEntity
        """
        return WrappedTextMessageProtocolEntity("!xkcd " + str(self.comic), to=self.sender)

    @staticmethod
    def get_description(language):
        """
        Returns a helpful description of the plugin's syntax and functionality
        :param language: the language to be returned
        :return: the description as string
        """
        if language == "en":
            return "/kvv\tUses Johannes bucher's bot to display XKCD comics\n" \
                   "syntax: /xkcd <comic_number>"
        elif language == "de":
            return "/kvv\tBenutzt Johannes Buchers bot um XKCD Comics anzuzeigen\n" \
                   "syntax: /xkcd <comic_number>"
        else:
            return "Help not available in this language"
