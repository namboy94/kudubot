"""
Decides the course of action when receiving a whatsapp message
@author Hermann Krumrey <hermann@krumreyh.com>
"""

from bot.deciders.ContainsDecider import ContainsDecider
from bot.deciders.EqualsDecider import EqualsDecider
from bot.deciders.RegexDecider import RegexDecider
from bot.deciders.StartsWithDecider import StartsWithDecider
from bot.utils.adressbook import getContact

from bot.deciders.CommandDecider import CommandDecider

"""
GeneralDecider Class
"""
class GeneralDecider(object):

    """
    Constructor
    @:param message - the message received by the yowsup layer
    @:param sender - the sender from whom the message wa received from
    @:param senderNumber - the number of the sender
    @:param participant - the participant number of a whatsapp group
    """
    def __init__(self, message, sender, participant):

        self.message = message
        self.mimMessage = message.lower()
        self.sender = sender
        self.senderName = getContact(sender)
        self.participant = participant

    """
    handles the decision making
    """
    def decide(self):

        if self.participant == "4915733871694": return False

        decision = False

        if not decision: decision = RegexDecider(self.message, self.sender).decide()
        if not decision: decision = ContainsDecider(self.message, self.sender).decide()
        if not decision: decision = StartsWithDecider(self.message, self.sender).decide()
        if not decision: decision = CommandDecider(self.message, self.sender).decide()
        if not decision: decision = EqualsDecider(self.message, self.sender).decide()

        return decision