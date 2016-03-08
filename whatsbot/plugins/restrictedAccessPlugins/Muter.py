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
    from utils.contacts.AddressBook import AddressBook
    from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
except ImportError:
    from whatsbot.plugins.GenericPlugin import GenericPlugin
    from whatsbot.utils.contacts.AddressBook import AddressBook
    from whatsbot.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class Muter(GenericPlugin):
    """
    The Muter Class
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
        self.authenticated = False

    def regex_check(self):
        """
        Checks if the user input is valid for this plugin to continue
        :return: True if input is valid, False otherwise
        """
        if self.message in ["/unmute", "/mute"]:
            return True
        else:
            return False

    def parse_user_input(self):
        """
        Parses the user's input
        :return: void
        """
        self.authenticated = AddressBook().is_authenticated(
            self.sender_plain) or AddressBook().is_authenticated(self.participant_plain)

        if self.authenticated:
            if self.message == "/unmute":
                self.layer.muted = False
            elif self.message == "/mute":
                self.layer.muted = True

    def get_response(self):
        """
        Returns the response calculated by the plugin
        :return: the response as a WrappedTextMessageProtocolEntity
        """
        if self.layer.muted:
            message_protocol_entity = WrappedTextMessageProtocolEntity("🤐", to=self.sender)
            self.send_message(message_protocol_entity)
            return message_protocol_entity

        else:
            return WrappedTextMessageProtocolEntity("😄", to=self.sender)

    @staticmethod
    def get_description(language):
        """
        Returns a helpful description of the plugin's syntax and functionality
        :param language: the language to be returned
        :return: the description as string
        """
        if language == "en":
            return "/mute\tmutes the whatsbot (admin)\n" \
                   "/unmute\tunmutes the whatsbot (admin)\n"
        elif language == "de":
            return "/mute\tStellt den Bot auf lautlos (admin)\n" \
                   "/unmute\tHolt den Bot wieder aus dem Lautlosmodus aus (admin)\n"
        else:
            return "Help not available in this language"

    @staticmethod
    def get_plugin_name():
        """
        Returns the plugin name
        :return: the plugin name
        """
        return "Muter Plugin"
