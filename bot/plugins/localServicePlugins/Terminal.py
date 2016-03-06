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
import subprocess
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin

"""
The Terminal Class
"""


class Terminal(GenericPlugin):

    """
    Constructor
    Defines parameters for the plugin.
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the received message information
    @:override
    """
    def __init__(self, layer, messageProtocolEntity=None):
        if messageProtocolEntity is None: self.layer = layer; return
        self.layer = layer
        self.entity = messageProtocolEntity
        self.message = self.entity.getBody()
        self.sender = self.entity.getFrom()

        self.command = ""

    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):
        if re.search(r"^/term uptime$", self.message):
            return True
        else: return False

    """
    Parses the user's input
    @:override
    """
    def parseUserInput(self):
        self.command = self.message.split("/term ")[1]

    """
    Returns the response calculated by the plugin
    @:return the response as a MessageProtocolEntity
    @:override
    """
    def getResponse(self):
        if self.command == "uptime":
            return TextMessageProtocolEntity(self.__executeCommand__(self.command), to=self.sender)
        else: return None

    """
    Returns a helpful description of the plugin's syntax and functionality
    @:param language - the language to be returned
    @:return the description as string
    @:override
    """
    @staticmethod
    def getDescription(language):
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

    """
    Executes a command and returns its output.
    @:return stdout of the command
    """
    def __executeCommand__(self, command):
        return subprocess.check_output(command, shell=True).decode()