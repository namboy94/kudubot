"""
Decider for strings that are defined as commands
@author Hermann Krumrey <hermann@krumreyh.com>
"""

from bot.deciders.Decision import Decision

from bot.utils.randomizer import getRandom

"""
CommandDecider Class
"""
class CommandDecider(object):

    """
    Constructor
    @:param message - the received whatsapp message
    @:param sender - the sender of the received message
    """
    def __init__(self, message, sender):
        self.message = message
        self.sender = sender

        self.options = [[["insult"], ["Nein, wieso?"]]
                        ]

    """
    Decides the user input
    """
    def decide(self):

        if not self.message.startswith("/") or len(self.message) < 2: return False

        self.message = self.message.split("/")[1].lower()

        i = 0
        while i < len(self.options):
            for key in self.options[i][0]:
                if self.message.lower().startswith(key):
                    return Decision(getRandom(self.options[i][1]), self.sender)
            i += 1

        return False