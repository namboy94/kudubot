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
    from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
except ImportError:
    from whatsbot.plugins.GenericPlugin import GenericPlugin
    from whatsbot.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class Help(GenericPlugin):
    """
    The Help Class
    """

    def __init__(self, layer, plugins, message_protocol_entity=None):
        """
        Constructor
        Defines parameters for the plugin.
        :param layer: the overlying yowsup layer
        :param plugins: The active plugins for which help messages should be shown
        :param message_protocol_entity: the received message information
        :return: void
        """
        super().__init__(layer, message_protocol_entity)
        self.plugins = plugins
        self.response = ""
        self.mode = ""
        self.lang = "en"

    def regex_check(self):
        """
        Checks if the user input is valid for this plugin to continue
        :return: True if input is valid, False otherwise
        """
        if not self.message.startswith("/help") and not self.message.startswith("/hilfe"):
            return False
        if self.message in ["/help", "/hilfe"]:
            self.mode = "all"
        else:
            try:
                self.mode = self.cap_message.split("/help ")[1]
            except IndexError:
                self.mode = self.cap_message.split("/hilfe ")[1]
                self.lang = "de"
        return True

    def parse_user_input(self):
        """
        Parses the user's input
        :return: void
        """
        self.response = "Plugins\n\n"
        indexed_plugins = {}
        counter = 0
        for plugin in self.plugins:
            self.response += str(counter) + ": " + plugin.get_plugin_name() + "\n"
            indexed_plugins[counter] = plugin
            counter += 1

        if self.lang == "en":
            self.response += "\nFor detailed instructions, enter \n/help <plugin-name> \nor \n/help <plugin-index>"
        elif self.lang == "de":
            self.response += "\nFür detailierte Anweisungen, geb \n/hilfe <plugin-name> \noder" \
                                 " \n/hilfe <plugin-index> ein"

        if self.mode != "all":
            identifier = ""
            if self.lang == "en":
                identifier = self.cap_message.split("/help ")[1]
            elif self.lang == "de":
                identifier = self.cap_message.split("/hilfe ")[1]
            try:
                self.response = indexed_plugins[int(identifier)].get_description(self.lang)
            except ValueError or KeyError:
                for plugin in self.plugins:
                    if plugin.get_plugin_name() == identifier:
                        self.response = plugin.get_description(self.lang)
                        return
            self.response = "Sorry, plugin \"" + identifier + "\" not found"

    def get_response(self):
        """
        Returns the response calculated by the plugin
        :return: the response as a WrappedTextMessageProtocolEntity
        """
        return WrappedTextMessageProtocolEntity(self.response, to=self.sender)

    @staticmethod
    def get_description(language):
        """
        No Description Needed
        """
        return ""

    @staticmethod
    def get_plugin_name():
        """
        No Description Needed
        """
        return ""
