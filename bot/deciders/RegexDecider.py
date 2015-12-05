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
        weatherRegex = re.search(r"(weather|wetter)(:(text;|verbose;)*)?([ ][^:;])?", self.message.lower())
        #timeRegex = re.search(r"(time|zeit) in [^ ]+", self.message.lower())
        bundesligaDayRegex = re.search(r"bundesliga spieltag", self.message.lower())
        bundesligaTableRegex = re.search(r"bundesliga tabelle", self.message.lower())
        mensaRegex = re.search(r"mensa", self.message.lower())
        genericMatchDayRegex = re.search(r"(spieltag|matchday|table|tabelle) [^ ]+", self.message.lower())

        #Do stuff
        if weatherRegex: return Decision(weather(self.message.lower()).getWeather(), self.sender)
        if bundesligaDayRegex: return Decision(FootballScores(self.message).getBundesligaScores(), self.sender)
        if bundesligaTableRegex: return Decision(FootballScores(self.message).getBundesligaTable(), self.sender)
        if mensaRegex: return Decision(Mensa().getTodaysPlan(), self.sender)
        if genericMatchDayRegex: return Decision(FootballScores(self.message).getResult(), self.sender)

        return False
