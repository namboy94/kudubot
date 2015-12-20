"""
Whatsapp Bot plugin that simulates games of blackjack
@author Hermann Krumrey <hermann@krumreyh.com>
"""

import re
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin

"""
The BlackJack Class
"""
class BlackJack(GenericPlugin):

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
        self.message = self.entity.getBody().lower()
        self.sender = self.entity.getFrom()

    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):
        #TODO USERCHECK
        return re.search(r"^/blackjack (start|hit|stay)$", self.message)

    """
    Parses the user's input
    @:override
    """
    def parseUserInput(self):
        splitString = self.message.split("/blackjack ")[1]
        if "start" in splitString:
            print()
        elif "hit" in splitString:
            print()
        elif "stay" in splitString:
            print()

    """
    Returns the response calculated by the plugin
    @:return the response as a MessageProtocolEntity
    @:override
    """
    def getResponse(self):
        return TextMessageProtocolEntity(, to=)
        raise NotImplementedError()

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