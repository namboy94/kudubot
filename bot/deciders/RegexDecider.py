"""
Decider for strings that follow a certain regex pattern
@author Hermann Krumrey <hermann@krumreyh.com>
"""

import re

from bot.utils.weather import weather

from bot.deciders.Decision import Decision

"""
RegexDecider Class
"""
class RegexDecider(object):

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

        #Regex Checks
        weatherRegex = re.compile("(weather|wetter)((:){1}(;text|;verbose)*)?( [^ :;]*)?").match(self.message.lower())

        #Do stuff
        if weatherRegex: return Decision(weather(self.message.lower()).getWeather(), self.sender)

        return False
