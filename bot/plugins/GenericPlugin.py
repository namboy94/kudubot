"""
Generic Plugin that defines the required  by the Plugin Manager
@author Hermann Krumrey <hermann@krumreyh.com>
"""

from utils.logging.LogWriter import LogWriter
from utils.encoding.Unicoder import Unicoder
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity

"""
The GenericPlugin Class
"""
class GenericPlugin(object):

    """
    Constructor
    Defines parameters for the plugin.
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the received message information
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
    """
    def regexCheck(self):
        raise NotImplementedError()

    """
    Parses the user's input
    """
    def parseUserInput(self):
        raise NotImplementedError()

    """
    Returns the response calculated by the plugin
    @:return the response as a MessageProtocolEntity
    """
    def getResponse(self):
        raise NotImplementedError()

    """
    Returns a helpful description of the plugin's syntax and functionality
    @:param language - the language to be returned
    @:return the description as string
    """
    @staticmethod
    def getDescription(language):
        raise NotImplementedError()

    """
    Starts a parallel background activity if this class has one.
    Defaults to False if not implemented
    @:return False, if no parallel activity defined, should be implemented to return True if one is implmented.
    """
    def parallelRun(self):
        return False

    """
    Sends a message outside of the normal yowsup loop
    @:param entity - the entity to be sent
    """
    def sendMessage(self, entity):
        if self.layer.muted:
            LogWriter.writeEventLog("s(m)", entity)
        else:
            LogWriter.writeEventLog("sent", entity)
            fixedEntity = Unicoder.fixOutgoingEntity(entity)
            self.layer.toLower(fixedEntity)

    """
    Sends an image outside of the normal yowsup loop
    @:param recipient - the receiver of the image
    @:param imagePath - the file path to the image
    @:param caption - the caption to be sent
    """
    def sendImage(self, recipient, imagePath, caption):
        if self.layer.muted:
            LogWriter.writeEventLog("i(m)", TextMessageProtocolEntity(imagePath + " --- " + caption, to=recipient))
        else:
            LogWriter.writeEventLog("imgs", TextMessageProtocolEntity(imagePath + " --- " + caption, to=recipient))
            self.layer.sendImage(recipient.split("@")[0], imagePath, caption)