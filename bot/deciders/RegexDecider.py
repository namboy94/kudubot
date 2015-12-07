"""
Decider for strings that follow a certain regex pattern
@author Hermann Krumrey <hermann@krumreyh.com>
"""

import re

from bot.utils.weather import weather
from bot.utils.FootballScores import FootballScores
from bot.utils.Mensa import Mensa
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
        weatherRegex = re.search(r"^(weather|wetter)(:)?(text;|verbose;)*( )?(([^ ]+){0,3})?", self.message.lower())
        #timeRegex = re.search(r"(time|zeit) in [^ ]+", self.message.lower())
        mensaRegex = re.search(r"^(mensa)( )?(linie (1|2|3|4|5|6)|schnitzelbar|curry queen|abend|cafeteria vormittag|cafeteria nachmittag)?$", self.message.lower())
        footballRegex = re.search(r"(^(table|tabelle|spieltag|matchday)( )?(([^ ]+){0,2})?)", self.message.lower())

        #Do stuff
        if weatherRegex: return Decision(weather(self.message.lower()).getWeather(), self.sender)
        if mensaRegex: return Decision(Mensa(self.message.lower()).getResponse(), self.sender)
        if footballRegex: return Decision(FootballScores(self.message).getResult(), self.sender)

        return False
