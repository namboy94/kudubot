"""
Decision object, stores message and sender of a Decider.

@author Hermann Krumrey <hermann@krumreyh.com>
"""

"""
The decision class
"""
class Decision(object):

    """
    Constructor
    @:param message = the message to be sent
    @:param sender = the recipient of the message
    """
    def __init__(self, message="", sender=""):
        self.message = message
        self.sender = sender