"""
Decider for strings that starts with a certain substring
@author Hermann Krumrey <hermann@krumreyh.com>
"""

from yowsup.demos.echoclient.utils.randomizer import getRandom
from yowsup.demos.echoclient.deciders.Decision import Decision

"""
StartsWithDecider Class
"""
class StartsWithDecider(object):

    """
    Constructor
    @:param message - the received whatsapp message
    @:param sender - the sender of the received message
    """
    def __init__(self, message, sender):
        self.message = message
        self.sender = sender

    """
    Decides the user input
    """
    def decide(self):

        options = [[["ls"], ["something\nsomething else\n...\nsome more stuff"]],
                   [["cat"], ["You're a kitty!",
                              "https://xkcd.com/231/",
                              "https://xkcd.com/729/",
                              "https://xkcd.com/26/"]],
                   [["man"], ["Oh, I'm sure you can figure it out."]],
                   [["echo"], [self.message, "Echo what now?"]]
                   ]

        i = 0
        while i < len(options):
            if self.message.lower().startswith(options[i]):
                return Decision(getRandom(options[i][1]), self.sender)
            i += 1

        return False