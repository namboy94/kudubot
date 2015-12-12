"""
plugin that allows muting of the bot
@author Hermann Krumrey <hermann@krumreyh.com>
"""

from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin

"""
The  Class
"""


class(GenericPlugin):
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
        raise NotImplementedError()

    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """

    def regexCheck(self):
        raise NotImplementedError()

    """
    Parses the user's input
    @:override
    """

    def parseUserInput(self):
        raise NotImplementedError()

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

    """
    Starts a parallel background activity if this class has one.
    Defaults to False if not implemented
    @:return False, if no parallel activity defined, should be implemented to return True if one is implmented.
    @:override
    """

    def parallelRun(self):
        return False