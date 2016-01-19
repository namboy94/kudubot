# coding=utf-8

"""
KVV Plugin that highjacks Johannes Bucher's KVV plugin.
@author Hermann Krumrey <hermann@krumreyh.com>
"""

import re
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin

"""
The KVV Class
"""
class KVV(GenericPlugin):

    """
    Constructor
    Defines parameters for the plugin.
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the received message information
    """
    def __init__(self, layer, messageProtocolEntity=None):
        #add this to the top:
        if messageProtocolEntity is None: self.layer = layer; return
        self.layer = layer
        self.entity = messageProtocolEntity
        self.message = self.entity.getBody()
        self.sender = self.entity.getFrom()

    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):
        return re.search(r"^/kvv [^ ]+", self.message)

    """
    Parses the user's input
    @:override
    """
    def parseUserInput(self):
        self.station = self.message.split("/kvv ", 1)[1]


    """
    Returns the station input by the user, and adds "!kvv " to it
    @:return the response as a MessageProtocolEntity
    @:override
    """
    def getResponse(self):
        return TextMessageProtocolEntity("!kvv " + self.station, to=self.sender)

    """
    Returns a helpful description of the plugin's syntax and functionality
    @:param language - the language to be returned
    @:return the description as string
    @:override
    """
    @staticmethod
    def getDescription(language):
        if language == "en":
            return "/kvv\tUses Johannes bucher's bot to display kvv times\n" \
                   "syntax: /kvv <station>"
        elif language == "de":
            return "/kvv\tBenutzt Johannes Buchers bot um KVV Zeiten anzuzeigen\n" \
                   "syntax: /kvv <station>"
        else:
            return "Help not available in this language"