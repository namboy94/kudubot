# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsapp-bot.

    whatsapp-bot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsapp-bot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsapp-bot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsapp-bot.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
import os
import random
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.localServicePlugins.Casino import Casino

"""
The BlackJack Class
"""
class BlackJack(Casino):

    inGame = False
    mode = ""
    insufficientFunds = False

    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):

        if re.search(r"^/blackjack (start ([0-9]+(\.[0-9]{2})?)|hit|stay)$", self.message):
            return True

    """
    Parses the user's input
    @:override
    """
    def parseUserInput(self):
        self.createUser(self.entity)
        self.mode = self.message.split(" ")[1]
        if self.mode == "start":
            if os.path.isdir(self.casinoDir + "blackjack/" + self.userID):
                self.inGame = True
            else:
                dollars, cents = self.decodeMoneyString(self.message.split(" ")[2])
                self.storeBet("blackjack", self.userID, self.sender, dollars, cents, "start")


    """
    Returns the response calculated by the plugin
    @:return the response as a MessageProtocolEntity
    @:override
    """
    def getResponse(self):
        if self.mode == "newBet":
            if self.insufficientFunds:
                return TextMessageProtocolEntity("Insufficient Funds", to=self.sender)
            else:
                return TextMessageProtocolEntity("Bet Saved", to=self.sender)
        elif self.mode == "bets":
            return TextMessageProtocolEntity(self.getBetStrings("roulette", self.userID), to=self.sender)
        elif self.mode == "time":
            currentTime = datetime.datetime.now()
            cMin = int(currentTime.minute)
            cSec = int(currentTime.second)
            timeLeft = 120 - cSec - 5
            if cMin % 2 == 1: timeLeft -= 60
            self.layer.toLower(TextMessageProtocolEntity(str(timeLeft) + "s to turn.", to=self.sender))

    """
    Returns a helpful description of the plugin's syntax and functionality
    @:param language - the language to be returned
    @:return the description as string
    @:override
    """
    @staticmethod
    def getDescription(language):
        if language == "en":
            return "/roulette\tAllows the sender to play roulette\n" \
                   "syntax: /roulette <amount> <bet>\n" \
                   "valid bets: 0-36 | red | black | odd | even | batch <1-2-3-4> |" \
                   " batch <1-2> | group <1-3> | row <1-3> | half <1-2>\n" \
                   "/roulette time\tDisplays the time until the roulette wheel is spun next.\n" \
                   "/roulette bets\tDisplays all bets of the user"
        elif language == "de":
            return "/roulette\tErmöglicht es, Roulette zu spielen\n" \
                   "syntax: /roulette <einsatz> <wette>\n" \
                   "Mögliche Wetten: 0-36 | red | black | odd | even | batch <1-2-3-4> |" \
                   " batch <1-2> | group <1-3> | row <1-3> | half <1-2>\n" \
                   "/roulette time\tZeigt die verbleibende Zeit bis zum nächsten Drehen des Roulette-Rads an\n" \
                   "/roulette bets\tZeigt alle Wetten des Nutzers an."
        else:
            return "Help not available in this language"

    """
    Evaluates a bet
    @:return the amount won by the player
    """
    def evaluateBet(self, bet):
        betType = bet["bet"]
        betDollars, betCents = self.decodeMoneyString(bet["value"])
        try:
            intbet = int(betType)
            if self.outcome == intbet:
                return self.multiplyMoney(35, betDollars, betCents)
            else:
                return (0, 0)
        except:
            if betType == "red":
                if self.outcome in self.red:
                    return self.multiplyMoney(2, betDollars, betCents)
            elif betType == "black":
                if self.outcome in self.black:
                    return self.multiplyMoney(2, betDollars, betCents)
            elif betType == "even":
                if self.outcome % 2 == 0:
                    return self.multiplyMoney(2, betDollars, betCents)
            elif betType == "odd":
                if self.outcome % 2 == 1:
                    return self.multiplyMoney(2, betDollars, betCents)
        return (0, 0)

    """
    """
    def drawCard(self):
        return random.randint(2, 11)