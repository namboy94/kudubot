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

try:
    from plugins.GenericPlugin import GenericPlugin
    from utils.math.Randomizer import Randomizer
    from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
except ImportError:
    from whatsbot.plugins.GenericPlugin import GenericPlugin
    from whatsbot.utils.math.Randomizer import Randomizer
    from whatsbot.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class SimpleEqualsResponse(GenericPlugin):
    """
    The SimpleEqualsResponse Class
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

        self.response = ""
        self.case_insensitive_options = [[["uptime"], ["Much too long, I'm tired"]]]
        self.case_sensitive_options = [[["ping"], ["pong"]],
                                       [["Ping"], ["Pong"]]]

    def regex_check(self):
        """
        Checks if the user input is valid for this plugin to continue
        :return: True if input is valid, False otherwise
        """
        for option in self.case_sensitive_options:
            for opt in option[0]:
                if self.cap_message == opt:
                    return True
        for option in self.case_insensitive_options:
            for opt in option[0]:
                if self.message == opt:
                    return True
        return False

    def parse_user_input(self):
        """
        Parses the user's input
        :return: void
        """
        for option in self.case_sensitive_options:
            for opt in option[0]:
                if self.message == opt:
                    self.response = Randomizer.get_random_element(option[1])
                    return
        for option in self.case_insensitive_options:
            for opt in option[0]:
                if self.message == opt:
                    self.response = Randomizer.get_random_element(option[1])
                    return

    def get_response(self):
        """
        Returns the response calculated by the plugin
        :return: the response as a MessageProtocolEntity
        """
        return WrappedTextMessageProtocolEntity(self.response, to=self.sender)

    @staticmethod
    def get_description(language):
        """
        Empty description, since this plugin doesn't really provide any functionality
        :param language: the language to be returned
        :return: an empty string
        """
        return ""
