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
import requests
from bs4 import BeautifulSoup

try:
    from plugins.GenericPlugin import GenericPlugin
    from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
except ImportError:
    from whatsbot.plugins.GenericPlugin import GenericPlugin
    from whatsbot.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class KickTipp(GenericPlugin):
    """
    The KickTipp Class
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
        self.community = ""

    def regex_check(self):
        """
        Checks if the user input is valid for this plugin to continue
        :return: True if input is valid, False otherwise
        """
        if self.message.startswith("/kicktipp "):
            return True
        else:
            return False

    def parse_user_input(self):
        """
        Parses the user's input
        :return: void
        """
        self.community = self.message.split("/kicktipp ")[1]

    def get_response(self):
        """
        Returns the response calculated by the plugin
        :return: the response as a MessageProtocolEntity
        """
        return WrappedTextMessageProtocolEntity(self.__get_table__(), to=self.sender)

    @staticmethod
    def get_description(language):
        """
        Returns a helpful description of the plugin's syntax and functionality
        :param language: the language to be returned
        :return: the description as string
        """
        if language == "en":
            return "/kicktipp\tFetches Kicktipp Community Tables\n" \
                   "syntax: /kicktipp <kicktipp-community>"
        elif language == "de":
            return "/kicktipp\tZeigt Kicktipp Community Tabellen\n" \
                   "syntax: /kicktipp <kicktipp-community>"
        else:
            return "Help not available in this language"

    # Local Methods
    def __get_table__(self):
        """
        Fetches the current table of the given kicktipp communiy
        :return: the table as formatted string.
        """
        html = requests.get("http://www.kicktipp.de/" + self.community + "/tippuebersicht").text
        soup = BeautifulSoup(html, "html.parser")
        names = soup.select(".mg_class")
        scores1 = soup.select(".pkt")
        scores2 = soup.select(".pkts")

        i = 0
        j = 0
        k = 0

        return_string = ""

        while i < len(names):
            return_string += str(i + 1) + ".    "
            if re.search(r"[0-9]+,[0-9]+", scores1[j].text):
                return_string += scores2[k].text + "    "
                return_string += scores1[j].text + "    "
                return_string += scores1[j+1].text + "    "
                k += 1
                j += 2
            else:
                return_string += scores1[j].text + "    "
                return_string += scores1[j+1].text + "    "
                return_string += scores1[j+2].text + "    "
                j += 3
            return_string += names[i].text + "\n"
            i += 1

        return return_string
