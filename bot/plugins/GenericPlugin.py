"""
Generic Plugin that defines the required  by the Plugin Manager
@author Hermann Krumrey <hermann@krumreyh.com>
"""

"""
The GenericPlugin Class
"""
class GenericPlugin(object):

    """
    Returns the regex(or an array of multiple regex's) used to identify this plugin
    @:return the regex or array of regex's
    """
    @staticmethod
    def getRegex():
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
    Starts a parallel background activity if this class has one.
    Defaults to False if not implemented
    @:return False, if no parallel activity defined, should be implemented to return True if one is implmented.
    """
    def parallelRun(self):
        return False