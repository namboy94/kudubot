"""
Roulette Game Plugin for the whatsapp bot
@author Hermann Krumrey <hermann@krumreyh.com>
"""
import os
import re
import time
import datetime
import random
import configparser
from subprocess import Popen
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin

"""
The Roulette Class
"""
class Roulette(GenericPlugin):

    red = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    black = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]

    """
    Constructor
    Defines parameters for the plugin.
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the received message information
    @:override
    """
    def __init__(self, layer, messageProtocolEntity=None):
        self.outcome = -1
        self.mode = "bet"
        self.userDir = os.getenv("HOME") + "/.whatsapp-bot/casino/users"
        self.rouletteDir = os.getenv("HOME") + "/.whatsapp-bot/casino/roulette"
        if messageProtocolEntity is None: self.layer = layer; return
        self.layer = layer
        self.entity = messageProtocolEntity
        self.message = self.entity.getBody().lower()
        self.sender = self.entity.getFrom()
        self.userNick = self.entity.getNotify()

        user = self.entity.getParticipant()
        if not user:
            self.userName = self.entity.getFrom(False)
        else:
            self.userName = user.split("@")[0]


    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):

        currentTime = datetime.datetime.now()
        cMin = int(currentTime.minute)
        cSec = int(currentTime.second)

        if re.search(r"^/roulette ([0-9]+\.[0-9]{2}) ([0-9]+|black|red|odd|even)$", self.message):
            if cMin % 2 == 1 and cSec >= 55:
                self.layer.toLower(TextMessageProtocolEntity("No more bets!", to=self.sender))
                return False
            try:
                betNumber = int(self.message.split(" ")[2])
                return betNumber < 37
            except Exception:
                return True
        elif re.search(r"^/roulette time$", self.message):
            if cMin % 2 == 1 and cSec >= 55:
                self.layer.toLower(TextMessageProtocolEntity("Turning Now!", to=self.sender))
                return False
            timeLeft = 120 - cSec - 5
            if cMin % 2 == 1: timeLeft -= 60
            self.layer.toLower(TextMessageProtocolEntity(str(timeLeft) + "s to turn.", to=self.sender))
            return False
        elif re.search(r"^/roulette balance$", self.message):
            if not os.path.isfile(self.userDir + "/" + self.userName): self.__addUser__(1000.00)
            userDetails = configparser.ConfigParser()
            userDetails.read(self.userDir + "/" + self.userName)
            balance = float(dict(userDetails.items("account"))["balance"])
            self.layer.toLower(TextMessageProtocolEntity("Your balance is " + str(balance), to=self.sender))
            return False
        elif re.search(r"^/roulette bets$", self.message):
            self.__sendBets__()
            return False

    """
    Parses the user's input
    @:override
    """
    def parseUserInput(self):
        if not os.path.isfile(self.userDir + "/" + self.userName): self.__addUser__(1000.00)
        userDetails = configparser.ConfigParser()
        userDetails.read(self.userDir + "/" + self.userName)
        self.balance = float(dict(userDetails.items("account"))["balance"])

        self.insufficientFunds = False

        self.betAmount = 0.0
        self.bet = ""

        splitString = self.message.split("/roulette ")[1]
        if splitString == "balance":
            self.mode = "balance"
            return
        self.betAmount = float(splitString.split(" ")[0])
        self.bet = splitString.split(" ")[1]
        if self.betAmount > self.balance:
            self.insufficientFunds = True
            return
        betFile = open(self.rouletteDir + "/" + self.userName, 'a')
        betFile.write("sender=" + self.sender + ";")
        betFile.write("user=" + self.userNick + ";")
        betFile.write("bet=" + self.bet + ";")
        betFile.write("betamount=" + str(self.betAmount) + ";\n")
        betFile.close()
        self.__transferFunds(self.userName, (-1) * self.betAmount)

    """
    Returns the response calculated by the plugin
    @:return the response as a MessageProtocolEntity
    @:override
    """
    def getResponse(self):
        if self.mode == "bet":
            if self.insufficientFunds:
                return TextMessageProtocolEntity("Insufficient Funds", to=self.sender)
            else:
                return TextMessageProtocolEntity("Bet Saved", to=self.sender)
        elif self.mode == "balance":
            return TextMessageProtocolEntity("balance: " + str(self.balance), to=self.sender)

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
                   "/roulette bets\n" \
                   "/roulette balance"
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
                for better in os.listdir(self.rouletteDir):
                    winnings = 0.0

                    file = open(self.rouletteDir + "/" + better, 'r')
                    fileContent = file.read()
                    file.close()
                    Popen(["rm", self.rouletteDir + "/" + better])
                    rawBets = fileContent.split("\n")
                    rawBets.pop()
                    user = ""

                    for rawBet in rawBets:
                        sender = rawBet.split(";")[0].split("sender=")[1]
                        if not sender in recipients:
                            recipients.append(sender)
                        user = rawBet.split(";")[1].split("user=")[1]
                        bet = rawBet.split(";")[2].split("bet=")[1]
                        betAmount = float(rawBet.split(";")[3].split("betamount=")[1])
                        winnings += self.__evaluateBet__(bet, betAmount)
                        self.__transferFunds(better, winnings)
                    betters.append((user, str(winnings)))

                for sender in recipients:
                    colour = ""
                    if self.outcome in self.red: colour = "(red)"
                    elif self.outcome in self.black: colour = "(black)"
                    winningText = "The winning number is " + str(self.outcome) + colour
                    for better in betters:
                        winningText += "\n" + better[0] + " won " + better[1]
                    winningMessage = TextMessageProtocolEntity(winningText, to=sender)
                    self.layer.toLower(winningMessage)
            time.sleep(1)



    ###LOCAL METHODS###

    """
    Adds a new user, or updates the user's balance
    """
    def __addUser__(self, value):
        file = open(self.userDir + "/" + self.userName, 'w')
        file.write("[account]\nbalance = " + str(value))
        file.close()

    """
    Evaluates a bet
    @:return the amount won by the player
    """
    def __evaluateBet__(self, bet, betAmount):
        try:
            intbet = int(bet)
            if self.outcome == intbet:
                return betAmount * 35
            else:
                return 0.0
        except:
            if bet == "red":
                if self.outcome in self.red:
                    return betAmount * 2
            elif bet == "black":
                if self.outcome in self.black:
                    return betAmount * 2
            elif bet == "even":
                if self.outcome % 2 == 0:
                    return betAmount * 2
            elif bet == "odd":
                if self.outcome % 2 == 1:
                    return betAmount * 2
        return 0.0

    """
    Adds or subtracts an amount from the balance of a player
    """
    def __transferFunds(self, userName, amount):
        file = open(self.userDir + "/" + userName, 'r')
        content = file.read()
        file.close()
        balance = float(content.split("balance = ")[1])
        balance += amount
        file = open(self.userDir + "/" + userName, 'w')
        file.write("[account]\nbalance = " + str(balance))
        file.close()

    """
    Sends a user all bets he/she has placed
    """
    def __sendBets__(self):
        message = "You have bet on the following:"
        try:
            file = open(self.rouletteDir + "/" + self.userName, 'r')
            fileContent = file.read()
            file.close()
            rawBets = fileContent.split("\n")
            rawBets.pop()


            for rawBet in rawBets:
                bet = rawBet.split(";")[2].split("bet=")[1]
                betAmount = float(rawBet.split(";")[3].split("betamount=")[1])
                message += "\nBet: " + bet + "     Amount: " + str(betAmount)
        except:
            print()
        self.layer.toLower(TextMessageProtocolEntity(message, to=self.sender))
