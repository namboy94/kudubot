"""
Decider for strings that follow a certain regex pattern
@author Hermann Krumrey <hermann@krumreyh.com>
"""

import re

from bot.utils.weather import weather
from bot.utils.FootballScores import FootballScores
from bot.utils.Mensa import Mensa
from bot.deciders.Decision import Decision
from bot.utils.calculations import anyBaseToN

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
        weatherRegex = re.search(r"^(weather|wetter)(:)?(text;|verbose;)*( )?(([^ ]+| ){0,5})?$", self.message.lower())
        mensaRegex = re.search(r"^(mensa)( )?(linie (1|2|3|4|5|6)|schnitzelbar|curry queen|abend|cafeteria vormittag|cafeteria nachmittag)?( morgen)?$", self.message.lower())
        footballRegex = re.search(r"^(table|tabelle|spieltag|matchday)( )?(([^ ]+| ){0,3})?$", self.message.lower())
        binaryRegex = re.search(r"^(0|1)+$", self.message)
        hexRegex = re.search(r"^(0x)(0|1|2|3|4|5|6|7|8|9|a|b|c|d|e|f)+$", self.message.lower())

        #Do stuff
        if weatherRegex: return Decision(weather(self.message.lower()).getWeather(), self.sender)
        if mensaRegex: return Decision(Mensa(self.message.lower()).getResponse(), self.sender)
        if footballRegex: return Decision(FootballScores(self.message.lower()).getResult(), self.sender)
        if binaryRegex: return Decision(anyBaseToN(2, self.message), self.sender)
        if hexRegex: return Decision(anyBaseToN(16, self.message.lower().split("0x")[1]), self.sender)

        return False
