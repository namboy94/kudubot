"""
Decides the course of action when receiving a whatsapp message
@author Hermann Krumrey <hermann@krumreyh.com>
"""

from yowsup.demos.echoclient.deciders.Decision import Decision
from yowsup.demos.echoclient.utils.adressbook import getContact
from yowsup.demos.echoclient.deciders.RegexDecider import RegexDecider
from yowsup.demos.echoclient.deciders.ContainsDecider import ContainsDecider
from yowsup.demos.echoclient.deciders.StartsWithDecider import StartsWithDecider
from yowsup.demos.echoclient.deciders.EqualsDecider import EqualsDecider

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
    def __init__(self, message, sender, senderNumber, participant):

        self.message = message
        self.mimMessage = message.lower()
        self.sender = sender
        self.senderNumber = senderNumber
        self.senderName = getContact(senderNumber)
        self.participant = participant

    """
    handles the decision making
    """
    def decide(self):

        decision = False

        if not decision: decision = RegexDecider(self.message, self.sender).decide()
        if not decision: decision = ContainsDecider(self.message, self.sender).decide()
        if not decision: decision = StartsWithDecider(self.message, self.sender).decide()
        if not decision: decision = EqualsDecider(self.message, self.sender).decide()

        return decision