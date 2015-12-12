"""
Plugin that can perform various terminal commands
@author Hermann Krumrey <hermann@krumreyh.com>
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
            return ""
        elif language == "de":
            return ""
        else:
            return "Help not available in this language"

    """
    """
    def __executeCommand__(self, command):
        return subprocess.check_output(command, shell=True).decode()