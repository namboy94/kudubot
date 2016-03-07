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
import subprocess

try:
    from plugins.GenericPlugin import GenericPlugin
    from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
except ImportError:
    from whatsbot.plugins.GenericPlugin import GenericPlugin
    from whatsbot.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class Terminal(GenericPlugin):
    """
    The Terminal Class
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
        self.command = ""

    def regex_check(self):
        """
        Checks if the user input is valid for this plugin to continue
        :return: True if input is valid, False otherwise
        """
        if re.search(r"^/term uptime$", self.message):
            return True
        else:
            return False

    def parse_user_input(self):
        """
        Parses the user's input
        :return: void
        """
        self.command = self.message.split("/term ")[1]

    def get_response(self):
        """
        Returns the response calculated by the plugin
        :return: the response as a WrappedTextMessageProtocolEntity
        """
        if self.command == "uptime":
            return WrappedTextMessageProtocolEntity(self.__execute_command__(self.command), to=self.sender)
        else:
            return None

    @staticmethod
    def get_description(language):
        """
        Returns a helpful description of the plugin's syntax and functionality
        :param language: the language to be returned
        :return: the description as string
        """
        if language == "en":
            return "/term\tAllows limited access to the server's terminal\n" \
                   "syntax:\n" \
                   "/term uptime\tShow's the server's uptime"
        elif language == "de":
            return "/term\tErmöglicht beschränkten Zugriff auf das Terminal des Servers\n" \
                   "syntax:\n" \
                   "/term uptime\tZeigt die uptime des Servers"
        else:
            return "Help not available in this language"

    @staticmethod
    def __execute_command__(command):
        """
        Executes a command and returns its output.
        :return: stdout of the command
        """
        return subprocess.check_output(command, shell=True).decode()
