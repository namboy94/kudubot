"""
Decider for strings that equals an exact string
@author Hermann Krumrey <hermann@krumreyh.com>
"""

from yowsup.demos.echoclient.utils.randomizer import getRandom
from yowsup.demos.echoclient.deciders.Decision import Decision

"""
EqualsDecider Class
"""
class EqualsDecider(object):

    """
    Constructor
    @:param message - the received whatsapp message
    @:param sender - the sender of the received message
    """
    def __init__(self, message, sender):
        self.message = message
        self.sender = sender

        self.options = [[["uptime"], ["Much too long, I'm tired"]]
                   ]

    """
    Decides the user input
    """
    def decide(self):

        i = 0
        while i < len(self.options):
            for key in self.options[i][0]:
                if self.message.lower() == key:
                    return Decision(getRandom(self.options[i][1]), self.sender)
            i += 1

        return False