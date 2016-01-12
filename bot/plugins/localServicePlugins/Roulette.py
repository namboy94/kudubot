"""
Roulette Game Plugin for the whatsapp bot
@author Hermann Krumrey <hermann@krumreyh.com>
"""
import os
import re
import time
import datetime
import random
from subprocess import Popen
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.localServicePlugins.Casino import Casino

"""
The Roulette Class
"""
class Roulette(Casino):

    outcome = -1
    mode = ""
    insufficientFunds = False

    red = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    black = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]


    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):

        currentTime = datetime.datetime.now()
        cMin = int(currentTime.minute)
        cSec = int(currentTime.second)

        if re.search(r"^/roulette (time|bets|([0-9]+(\.[0-9]{2})?) ([0-9]+|black|red|odd|even))$", self.message):
            if cMin % 2 == 1 and cSec >= 55:
                self.layer.toLower(TextMessageProtocolEntity("Currently spinning the wheel!", to=self.sender))
                return False
            try:
                betNumber = int(self.message.split(" ")[2])
                return betNumber < 37
            except Exception:
                return True

    """
    Parses the user's input
    @:override
    """
    def parseUserInput(self):
        self.createUser(self.entity)
        mode = self.message.split(" ")[1]
        if mode == "time": self.mode = "time"
        elif mode == "bets": self.mode = "bets"
        else:
            self.mode = "newBet"
            dollars, cents = self.decodeMoneyString(self.message.split(" ")[1])
            if self.hasSufficientFunds(self.userID, dollars, cents):
                self.transferFunds(self.userID, -1 * dollars, -1 * cents)
                self.storeBet("roulette", self.userID, self.sender, dollars, cents, self.message.split(" ")[2])
            else:
                self.insufficientFunds = True


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
            return "/roulette\n" \
                   "syntax: /roulette <amount> <bet>\n" \
                   "valid bets: 0-36 | red | black | odd | even\n" \
                   "/roulette time\n" \
                   "/roulette bets"
        elif language == "de":
            return ""
        else:
            return "Help not available in this language"

    """
    Starts a parallel background activity if this class has one.
    Defaults to False if not implemented
    @:return False, if no parallel activity defined, should be implemented to return True if one is implmented.
    @:override
    """
    def parallelRun(self):
        while True:

            currentTime = datetime.datetime.now()
            minutes = int(currentTime.minute)
            seconds = int(currentTime.second)

            if minutes % 2 == 1 and seconds >= 55:
                recipients = []
                betters = []
                self.outcome = random.randint(0, 36)
                for better in os.listdir(self.casinoDir + "roulette"):
                    winCents = 0
                    winDollars = 0

                    bets = self.getBets("roulette", better)
                    Popen(["rm", self.casinoDir + "roulette/" + better]).wait()

                    user = self.getUserNick(better)

                    for bet in bets:
                        sender = bet["sender"]
                        if sender not in recipients:
                            recipients.append(sender)

                        dollars, cents = self.evaluateBet(bet)
                        winCents += cents
                        while winCents >= 100: dollars += 1; winCents -= 100
                        winDollars += dollars

                    self.transferFunds(better, winDollars, winCents)

                    betters.append((user, self.encodeMoneyString(winDollars, winCents)))

                for sender in recipients:
                    colour = ""
                    if self.outcome in self.red: colour = " (red)"
                    elif self.outcome in self.black: colour = " (black)"
                    winningText = "The winning number is " + str(self.outcome) + colour
                    for better in betters:
                        winningText += "\n" + better[0] + " won " + better[1] + "€"
                    winningMessage = TextMessageProtocolEntity(winningText, to=sender)
                    self.layer.toLower(winningMessage)
            time.sleep(1)

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