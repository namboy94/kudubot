"""
Plugin that sends simple text responses to exact strings
@author Hermann Krumrey <hermann@krumreyh.com>
"""

from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin
from utils.math.Randomizer import Randomizer

"""
The SimpleEqualsResponse Class
"""
class SimpleEqualsResponse(GenericPlugin):

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
        self.minMessage = self.message.lower()
        self.sender = self.entity.getFrom()

        self.caseInsensitiveOptions = [[["uptime"], ["Much too long, I'm tired"]]]
        self.caseSensitiveOptions = [[[], []]]

    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):
        for option in self.caseSensitiveOptions:
            match = False
            for opt in option[0]:
                if self.message == opt:
                    match = True
        for option in self.caseInsensitiveOptions:
            match = False
            for opt in option[0]:
                if self.minMessage == opt:
                    match = True

    """
    Parses the user's input
    @:override
    """
    def parseUserInput(self):
        for option in self.caseSensitiveOptions:
            for opt in option[0]:
                if self.message == opt:
                    self.response = Randomizer.getRandomElement(option[1])
                    return
        for option in self.caseInsensitiveOptions:
            for opt in option[0]:
                if self.minMessage == opt:
                    self.response = Randomizer.getRandomElement(option[1])
                    return

    """
    Returns the response calculated by the plugin
    @:return the response as a MessageProtocolEntity
    @:override
    """
    def getResponse(self):
        return TextMessageProtocolEntity(self.response, to=self.sender)

    """
    Empty description
    @:param language - the language to be returned
    @:return the description as string
    @:override
    """
    @staticmethod
    def getDescription(language):
        return ""
