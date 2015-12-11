"""
Generic Plugin that defines the required  by the Plugin Manager
@author Hermann Krumrey <hermann@krumreyh.com>
"""

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