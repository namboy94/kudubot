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

try:
    from plugins.GenericPlugin import GenericPlugin
    from utils.contacts.AddressBook import AddressBook
    from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
except ImportError:
    from whatsbot.plugins.GenericPlugin import GenericPlugin
    from whatsbot.utils.contacts.AddressBook import AddressBook
    from whatsbot.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class PluginSelector(GenericPlugin):
    """
    The PluginSelector Class
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
        self.response = ""

    def regex_check(self):
        """
        Checks if the user input is valid for this plugin to continue
        :return: True if input is valid, False otherwise
        """
        return re.search(r"^/plugin (activate|deactivate) ([0-9]+|[a-zA-Z]+(( [a-zA-Z]+)+)?)$", self.message)

    def parse_user_input(self):
        """
        Parses the user's input
        :return: void
        """
        self.authenticated = AddressBook().is_authenticated(
            self.sender_plain) or AddressBook().is_authenticated(self.participant_plain)

        if self.authenticated:
            if self.message.startswith("/plugin activate"):
                success = self.layer.plugin_manager.set_plugin_state(self.sender_plain,
                                                                     self.cap_message.split("/plugin activate ")[1],
                                                                     True)
                if success:
                    self.response = "Plugin " + self.cap_message.split("/plugin activate ")[1] + " activated"
                else:
                    self.response = "Plugin " + self.cap_message.split("/plugin activate ")[1] + " does not exist"

            elif self.message.startswith("/plugin deactivate"):
                success = self.layer.plugin_manager.set_plugin_state(self.sender_plain,
                                                                     self.cap_message.split("/plugin deactivate ")[1],
                                                                     False)
                if success:
                    self.response = "Plugin " + self.cap_message.split("/plugin deactivate ")[1] + " deactivated"
                else:
                    self.response = "Plugin " + self.cap_message.split("/plugin deactivate ")[1] + " does not exist"

    def get_response(self):
        """
        Returns the response calculated by the plugin
        :return: the response as a WrappedTextMessageProtocolEntity
        """
        return WrappedTextMessageProtocolEntity(body=self.response, to=self.sender)

    @staticmethod
    def get_description(language):
        """
        Returns a helpful description of the plugin's syntax and functionality
        :param language: the language to be returned
        :return: the description as string
        """
        if language == "en":
            return "/plugin\tallows activation/deactivation of plugins (admin)\n" \
                   "/plugin activate <plugin|plugin-index>\tactivates a plugin\n" \
                   "/plugin deactivate <plugin|plugin-index>\tdeactivates a plugin\n"
        elif language == "de":
            return "/plugin\tErmöglicht das Aktivieren/Deaktivieren von plugins (admin)\n" \
                   "/plugin activate <plugin|plugin-index>\tAktiviert ein plugin\n" \
                   "/plugin deactivate <plugin|plugin-index>\tDeaktiviert ein plugin\n"
        else:
            return "Help not available in this language"
