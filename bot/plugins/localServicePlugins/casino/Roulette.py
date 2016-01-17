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
from utils.encoding.Unicoder import Unicoder
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from plugins.localServicePlugins.Casino import Casino
from utils.contacts.AddressBook import AddressBook

"""
The Roulette Class
"""
class Roulette(Casino):

    outcome = -1
    mode = ""
    insufficientFunds = False

    red = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    black = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
    board = [[3,6,9,12,15,18,21,24,27,30,33,36],
             [2,5,8,11,14,17,20,23,26,29,32,35],
             [1,4,7,10,13,16,19,22,25,28,31,34]]
    pairs = []
    quads = []
    r = 0
    while r < len(board):
        i = 0
        j = 1
        while j < len(board[r]):
            pairs.append([board[r][i], board[r][j]])
            if r < (len(board) - 1):
                pairs.append([board[r][i], board[r+1][i]])
                pairs.append([board[r][j], board[r+1][j]])
                quads.append([board[r][i], board[r+1][i], board[r][j], board[r+1][j]])
            i +=1; j += 1
        r += 1



    """
    Checks if the user input is valid for this plugin to continue
    @:return True if input is valid, False otherwise
    @:override
    """
    def regexCheck(self):

        currentTime = datetime.datetime.now()
        cMin = int(currentTime.minute)
        cSec = int(currentTime.second)

        if re.search(r"^/roulette (spin|cancel|board|time|bets|([0-9]+(\.[0-9]{2})?)"
                     r" ([0-9]{1,2}|batch [0-9]{1,2}(-[0-9]{1,2}){3}|batch [0-9]{1,2}-[0-9]{1,2}|"
                     r"black|red|odd|even|half (1|2)|(row|group) (1|2|3)))$", self.message):
            if cMin % 2 == 1 and cSec >= 55:
                self.layer.toLower(TextMessageProtocolEntity("Currently spinning the wheel!", to=self.sender))
                return False
            try:
                betNumber = int(self.message.split(" ")[2])
                return betNumber < 37
            except Exception:
                try:
                    batchString = self.message.split(" ")[3]
                    numbers = []
                    for number in batchString.split("-"):
                        num = int(number)
                        if not num < 37: return False
                        numbers.append(num)
                    if len(numbers) == 2:
                        for pair in self.pairs:
                            if numbers[0] in pair and numbers[1] in pair:
                                return True
                    elif len(numbers) == 4:
                        for quad in self.quads:
                            if numbers[0] in quad and numbers[1] in quad\
                                    and numbers[2] in quad and numbers[3] in quad:
                                return True
                    else: return True
                    self.layer.toLower(TextMessageProtocolEntity("Invalid batch!", to=self.sender))
                    return False
                except:
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
        elif mode == "board": self.mode = "board"
        elif mode == "cancel": self.mode = "cancel"
        elif mode == "spin": self.mode = "spin"
        else:
            self.mode = "newBet"
            dollars, cents = self.decodeMoneyString(self.message.split(" ")[1])
            if self.hasSufficientFunds(self.userID, dollars, cents):
                self.transferFunds(self.userID, -1 * dollars, -1 * cents)
                bet = self.message.split(" ")[2]
                if len(self.message.split(" ")) == 4: bet += ":" + self.message.split(" ")[3]
                self.storeBet("roulette", self.userID, self.sender, dollars, cents, bet)
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
        elif self.mode == "spin":
            if AddressBook().isAuthenticated(self.userID):
                self.parallelRun(True)
                return None
            else:
                return TextMessageProtocolEntity("Sorry.", to=self.sender)
        elif self.mode == "board":
            rouletteImage = os.getenv("HOME") + "/.whatsapp-bot/images/roulette/table.jpg"
            self.layer.sendImage(self.sender, rouletteImage, "")
            return None
        elif self.mode == "cancel":
            Popen(["rm", self.casinoDir + "roulette/" + self.userID]).wait()
            return TextMessageProtocolEntity("Bets cancelled", to=self.sender)
        elif self.mode == "time":
            currentTime = datetime.datetime.now()
            cMin = int(currentTime.minute)
            cSec = int(currentTime.second)
            timeLeft = 120 - cSec - 5
            if cMin % 2 == 1: timeLeft -= 60
            return TextMessageProtocolEntity(str(timeLeft) + "s to turn.", to=self.sender)

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
                   "valid bets: 0-36 | red | black | odd | even | half 1-2 | group 1-3 | row 1-3 | batch 0-36{2|4}\n" \
                   "/roulette time\n" \
                   "/roulette board\n" \
                   "/roulette bets\n" \
                   "/roulette cancel\n" \
                   "/roulette spin(admin)"
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
    def parallelRun(self, once=False):
        while True:

            currentTime = datetime.datetime.now()
            minutes = int(currentTime.minute)
            seconds = int(currentTime.second)

            if (minutes % 2 == 1 and seconds >= 55) or once:
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

                    betters.append((user, self.encodeMoneyString(winDollars, winCents, True)))

                for sender in recipients:
                    colour = ""
                    if self.outcome in self.red: colour = " (red)\n"
                    elif self.outcome in self.black: colour = " (black)\n"
                    else: colour = "\n"
                    winningText = "The winning number is " + str(self.outcome) + colour
                    for better in betters:
                        winningText += "\n" + better[0] + " won " + better[1] + "€"
                    winningMessage = TextMessageProtocolEntity(winningText, to=sender)
                    self.layer.toLower(Unicoder.fixOutgoingEntity(winningMessage))
                if not once: time.sleep(5)
            if once: break
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
            elif betType.startswith("batch"):
                betString = betType.split("batch:")[1]
                betNumbers = betString.split("-")
                i = 0
                while i < len(betNumbers): betNumbers[i] = int(betNumbers[i]); i+=1
                if self.outcome in betNumbers:
                    if len(betNumbers) == 2: return self.multiplyMoney(18, betDollars, betCents)
                    if len(betNumbers) == 4: return self.multiplyMoney(9, betDollars, betCents)
            elif betType.startswith("group"):
                groupNumber = int(betType.split("group:")[1])
                group = []
                i = (groupNumber - 1) * 4
                while i < groupNumber * 4:
                    group.append(self.board[0][i])
                    group.append(self.board[1][i])
                    group.append(self.board[2][i])
                    i += 1
                if self.outcome in group:
                    return self.multiplyMoney(3, betDollars, betCents)
            elif betType.startswith("row"):
                rowNumber = int(betType.split("row:")[1])
                if self.outcome in self.board[rowNumber - 1]:
                    return self.multiplyMoney(3, betDollars, betCents)
            elif betType.startswith("half"):
                halfNumber = int(betType.split("half:")[1])
                if halfNumber == 1:
                    if self.outcome > 0 and self.outcome < 19:
                        return self.multiplyMoney(2, betDollars, betCents)
                else:
                    if self.outcome > 18:
                        return self.multiplyMoney(2, betDollars, betCents)
        return (0, 0)