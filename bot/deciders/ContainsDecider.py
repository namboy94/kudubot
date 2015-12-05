"""
Decider for strings that only contain a certain substring
@author Hermann Krumrey <hermann@krumreyh.com>
"""

import random

from bot.deciders.Decision import Decision

from bot.utils.randomizer import getRandom

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

        self.options = [[["keks", "cookie"], ["Ich will auch Kekse!",
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
                   [["beste bot", "bester bot"], ["😘"]],
                   [["chicken", "nuggets", "huhn", "hühnchen"], ["🐤", "Die armen Kücken!\n🐤🐤🐤"]],
                   [["scheiße", "kacke"], ["💩"]]
                   ]

    """
    Decides the user input
    """
    def decide(self):

        i = 0
        while i < len(self.options):
            for key in self.options[i][0]:
                if key in self.message.lower():
                    return Decision(getRandom(self.options[i][1]), self.sender)
            i += 1

        return False
