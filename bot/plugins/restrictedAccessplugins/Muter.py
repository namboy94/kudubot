"""
plugin that allows muting of the bot
@author Hermann Krumrey <hermann@krumreyh.com>
"""

from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin
from utils.encoding.Unicoder import Unicoder
from utils.contacts.AddressBook import AddressBook

"""
The Muter Class
"""
class Muter(GenericPlugin):

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

        self.authenticated = False

    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):
        if self.message in ["/unmute", "/mute"]:
            return True
        else: return False

    """
    Parses the user's input
    @:override
    """
    def parseUserInput(self):
        self.authenticated = AddressBook().isAuthenticated(self.entity.getFrom(False)) \
                             or AddressBook().isAuthenticated(self.entity.getParticipant())

        if self.authenticated:
            if self.message == "/unmute":
                self.layer.muted = False
            elif self.message == "/mute":
                self.layer.muted = True

    """
    Returns the response calculated by the plugin
    @:return the response as a MessageProtocolEntity
    @:override
    """
    def getResponse(self):
        if self.layer.muted:
            messageProtocolEntity = TextMessageProtocolEntity("🤐", to=self.sender)
            messageProtocolEntity = Unicoder.fixOutgoingEntity(messageProtocolEntity)
            self.layer.toLower(messageProtocolEntity)
            return messageProtocolEntity

        else:
            return TextMessageProtocolEntity("😄", to=self.sender)

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