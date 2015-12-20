"""
Roulette Game Plugin for the whatsapp bot
@author Hermann Krumrey <hermann@krumreyh.com>
"""
import os
import re
import random
import configparser
from subprocess import Popen
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.GenericPlugin import GenericPlugin

"""
The Roulette Class
"""
class Roulette(GenericPlugin):

    """
    Constructor
    Defines parameters for the plugin.
    @:param layer - the overlying yowsup layer
    @:param messageProtocolEntity - the received message information
    @:override
    """
    def __init__(self, layer, messageProtocolEntity=None):
        self.outcome = -1
        self.userDir = os.getenv("HOME") + "/.whatsapp-bot/casino/users"
        self.rouletteDir = os.getenv("HOME") + "/.whatsapp-bot/casino/roulette"
        if messageProtocolEntity is None: self.layer = layer; return
        self.layer = layer
        self.entity = messageProtocolEntity
        self.message = self.entity.getBody()
        self.sender = self.entity.getFrom()
        self.user = self.entity.getFrom(False)
        if not self.user: self.user = self.entity.getFrom(False)
        if not os.path.isfile(self.userDir + "/" + self.user): self.__addUser__()
        userDetails = configparser.ConfigParser().read(self.userDir + "/" + self.user)
        self.balance = float(dict(userDetails.items("account"))["balance"])

        self.insufficientFunds = False

        self.betAmount = 0.0
        self.bet = ""

    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):
        return re.search(r"^/roulette ([0-9]+\.[0-9]{2}) ([0-9]+|black|red)$", self.message)
        #TODO Check how to force a number between 0 and 36
        #TODO Make a time check to avoid conflicts with writing/reading/deleting files

    """
    Parses the user's input
    @:override
    """
    def parseUserInput(self):
        splitString = self.message.split("/roulette ")[1]
        self.betAmount = float(splitString.split(" ")[0])
        self.bet = splitString.split(" ")[1]
        if self.betAmount > self.balance:
            self.insufficientFunds = True
            return
        betFile = open(self.rouletteDir + "/" + self.user, 'a')
        betFile.write("sender=" + self.sender + "\n")
        betFile.write("bet=" + self.bet + "\n")
        betFile.write("betamount=" + str(self.betAmount) + "\n")
        betFile.write("br\n")
        betFile.close()
        self.__transferFunds(self.user, self.betAmount)

    """
    Returns the response calculated by the plugin
    @:return the response as a MessageProtocolEntity
    @:override
    """
    def getResponse(self):
        return TextMessageProtocolEntity("Bet Saved", to=self.sender)

    """
    Returns a helpful description of the plugin's syntax and functionality
    @:param language - the language to be returned
    @:return the description as string
    @:override
    """
    @staticmethod
    def getDescription(language):
        if language == "en":
            return ""
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
            #TODO get time in minutes and seconds
            minutes = 2
            seconds = 1
            if minutes % 2 == 0 and seconds == 0:
                recipients = []
                self.outcome = random.randint(0, 36)
                for better in os.listdir(self.rouletteDir):
                    winnings = 0.0

                    file = open(self.rouletteDir + "/" + better, 'r')
                    fileContent = file.read()
                    file.close()
                    Popen(["rm", self.rouletteDir + "/" + better])
                    rawBets = fileContent.split("br\n")
                    for betString in rawBets:
                        sender = betString.split("sender=")[1].split("\n")[0]
                        if not sender in recipients:
                            recipients.append(sender)
                        bet = betString.split("bet=")[1].split("\n")[0]
                        betAmount = float(betString.split("betamount=")[1].split("\n")[0])
                        winnings += self.__evaluateBet__(bet, betAmount)
                    self.__transferFunds(better, winnings)
                for sender in recipients:
                    winningMessage = TextMessageProtocolEntity("The winning number is " + str(self.outcome), to=sender)
                    self.layer.toLower(winningMessage)



    ###LOCAL METHODS###

    """
    Adds a new user, or updates the user's balance
    """
    def __addUser__(self, value):
        file = open(self.userDir + "/" + self.user, 'w')
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
                #TODO Find out which numbers are red and which are black
                if self.outcome in [0,1,2,3]:
                    return betAmount * 2
            elif bet == "black":
                #TODO Find out which numbers are red and which are black
                if self.outcome in [0,1,2,3]:
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
    def __transferFunds(self, user, amount):
        file = open(self.userDir + "/" + user, 'r')
        content = file.read()
        file.close()
        balance = float(content.split("balance = ")[1])
        balance += amount
        file = open(self.userDir + "/" + user, 'w')
        file.write("[account]\nbalance = " + str(balance))
        file.close()

