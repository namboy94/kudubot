"""
Decider for strings that only contain a certain substring
@author Hermann Krumrey <hermann@krumreyh.com>
"""

from yowsup.demos.echoclient.utils.randomizer import getRandom
from yowsup.demos.echoclient.deciders.Decision import Decision
import random


"""
ContainsDecider Class
"""
class ContainsDecider(object):

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

        options = [[["keks", "cookie"], ["Ich will auch Kekse!",
                                         "Wo gibt's Kekse?",
                                         "Kekse sind klasse!",
                                         "Ich hab einen Gutschein für McDonald's Kekse!"]],
                   [["kuchen", "cake"], ["Ich mag Kuchen",
                                         "Marmorkuchen!",
                                         "Kuchen gibt's bei Starbucks"]],
                   [["ups", "oops", "uups"], ["Was hast du jetzt schon wieder kaputt gemacht?"]],
                   [["wuerfel", "würfel"], ["Würfel sind toll",
                                            "Du hast eine " + str(random.randint(1,6)) + " gewürfelt!",
                                            "https://play.google.com/store/apps/details?id=com.namibsun.android.dice"]],
                   [["😂"], ["😂😂😂"]],
                   [["🖕🏻"], ["😡🖕🏻"]],
                   [["beste bot", "bester bot"], ["😘"]]
                   ]

        i = 0
        while i < len(options):
            if self.message.lower() in options[i]:
                return Decision(getRandom(options[i][1]), self.sender)
            i += 1

        return False
