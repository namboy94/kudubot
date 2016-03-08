# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsbot.

    whatsbot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsbot.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import re
import time
import datetime
import random
from subprocess import Popen

try:
    from plugins.localServicePlugins.Casino import Casino
    from utils.contacts.AddressBook import AddressBook
    from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
except ImportError:
    from whatsbot.plugins.localServicePlugins.Casino import Casino
    from whatsbot.utils.contacts.AddressBook import AddressBook
    from whatsbot.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class Roulette(Casino):
    """
    The Roulette Class
    """

    outcome = -1
    mode = ""
    insufficient_funds = False

    # Constant Values
    red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    board = [[3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
             [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
             [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]]
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
            i += 1
            j += 1
        r += 1

    def regex_check(self):
        """
        Checks if the user input is valid for this plugin to continue
        :return True if input is valid, False otherwise
        """

        current_time = datetime.datetime.now()
        current_minute = int(current_time.minute)
        current_second = int(current_time.second)

        if re.search(r"^/roulette (spin|cancel|board|time|bets|([0-9]+(\.[0-9]{2})?)"
                     r" ([0-9]{1,2}|batch [0-9]{1,2}(-[0-9]{1,2}){3}|batch [0-9]{1,2}-[0-9]{1,2}|"
                     r"black|red|odd|even|half (1|2)|(row|group) (1|2|3)))$", self.message):
            if current_minute % 2 == 1 and current_second >= 55:
                self.send_message(WrappedTextMessageProtocolEntity("Currently spinning the wheel!", to=self.sender))
                return False
            try:
                bet_number = int(self.message.split(" ")[2])
                return bet_number < 37
            except Exception as e:
                str(e)
                try:
                    batch_string = self.message.split(" ")[3]
                    numbers = []
                    for number in batch_string.split("-"):
                        num = int(number)
                        if not num < 37:
                            return False
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
                    else:
                        return True
                    self.send_message(WrappedTextMessageProtocolEntity("Invalid batch!", to=self.sender))
                    return False
                except Exception as ex:
                    str(ex)
                    return True

    def parse_user_input(self):
        """
        Parses the user's input
        :return: void
        """
        self.create_user(self.entity)
        mode = self.message.split(" ")[1]
        if mode == "time": 
            self.mode = "time"
        elif mode == "bets": 
            self.mode = "bets"
        elif mode == "board": 
            self.mode = "board"
        elif mode == "cancel":
            self.mode = "cancel"
        elif mode == "spin": 
            self.mode = "spin"
        else:
            self.mode = "newBet"
            dollars, cents = self.decode_money_string(self.message.split(" ")[1])
            if self.has_sufficient_funds(self.user_id, dollars, cents):
                self.transfer_funds(self.user_id, -1 * dollars, -1 * cents)
                bet = self.message.split(" ")[2]
                if len(self.message.split(" ")) == 4: 
                    bet += ":" + self.message.split(" ")[3]
                self.store_bet("roulette", self.user_id, self.sender, dollars, cents, bet)
            else:
                self.insufficient_funds = True

    def get_response(self):
        """
        Returns the response calculated by the plugin
        :return: the response as a MessageProtocolEntity
        """
        if self.mode == "newBet":
            if self.insufficient_funds:
                return WrappedTextMessageProtocolEntity("Insufficient Funds", to=self.sender)
            else:
                return WrappedTextMessageProtocolEntity("Bet Saved", to=self.sender)
        elif self.mode == "bets":
            return WrappedTextMessageProtocolEntity(self.get_bet_strings("roulette", self.user_id), to=self.sender)
        elif self.mode == "spin":
            if AddressBook().is_authenticated(self.user_id):
                self.parallel_run(True)
                return None
            else:
                return WrappedTextMessageProtocolEntity("Sorry.", to=self.sender)
        elif self.mode == "board":
            roulette_image = "../res/images/roulette/table.jpg"
            self.send_image(self.sender, roulette_image, "")
            return None
        elif self.mode == "cancel":
            Popen(["rm", self.casino_dir + "roulette/" + self.user_id]).wait()
            return WrappedTextMessageProtocolEntity("Bets cancelled", to=self.sender)
        elif self.mode == "time":
            current_time = datetime.datetime.now()
            current_minute = int(current_time.minute)
            current_second = int(current_time.second)
            time_left = 120 - current_second - 5
            if current_minute % 2 == 1: 
                time_left -= 60
            return WrappedTextMessageProtocolEntity(str(time_left) + "s to turn.", to=self.sender)

    @staticmethod
    def get_description(language):
        """
        Returns a helpful description of the plugin's syntax and functionality
        :param language: the language to be returned
        :return: the description as string
        """
        if language == "en":
            return "/roulette\tAllows the sender to play roulette\n" \
                   "syntax: /roulette <amount> <bet>\n" \
                   "valid bets: 0-36 | red | black | odd | even | half 1-2 | group 1-3 | row 1-3 | batch 0-36{2|4}\n" \
                   "/roulette time\tDisplays the time left until the wheel is spun again\n" \
                   "/roulette board\tSends an image of a Roulette board as reference\n" \
                   "/roulette bets\tDisplays all bets of a user\n" \
                   "/roulette cancel\tCancels all bet of a user\n" \
                   "/roulette spin\tImmediately spins the wheel(admin)"
        elif language == "de":
            return "/roulette\tErmöglicht das Spielen von Roulette\n" \
                   "syntax: /roulette <einsatz> <wette>\n" \
                   "Mögliche Wetten:" \
                   " 0-36 | red | black | odd | even | half 1-2 | group 1-3 | row 1-3 | batch 0-36{2|4}\n" \
                   "/roulette time\tZeigt die verbleibende Zeit bis zum nächsten Drehen des Roulette-Rads an.\n" \
                   "/roulette board\tSchickt ein Bild eines Roulettebretts als Referenz\n" \
                   "/roulette bets\tZeigt alle Wetten eines Nutzers an\n" \
                   "/roulette cancel\tBricht alle Wetten des Nutzers ab\n" \
                   "/roulette spin\tDreht das Rouletterad(admin)"
        else:
            return "Help not available in this language"

    @staticmethod
    def get_plugin_name():
        """
        Returns the plugin name
        :return: the plugin name
        """
        return "Roulette Plugin"

    def parallel_run(self, once=False):
        """
        Starts a parallel background activity if this class has one.
        :return: void
        """
        while True:
            current_time = datetime.datetime.now()
            minutes = int(current_time.minute)
            seconds = int(current_time.second)

            if (minutes % 2 == 1 and seconds >= 55) or once:
                recipients = []
                betters = []
                self.outcome = random.randint(0, 36)
                for better in os.listdir(self.casino_dir + "roulette"):
                    win_cents = 0
                    win_dollars = 0

                    bets = self.get_bets("roulette", better)
                    Popen(["rm", self.casino_dir + "roulette/" + better]).wait()

                    user = self.get_user_nick(better)

                    for bet in bets:
                        sender = bet["sender"]
                        if sender not in recipients:
                            recipients.append(sender)

                        dollars, cents = self.evaluate_bet(bet)
                        win_cents += cents
                        while win_cents >= 100: 
                            dollars += 1
                            win_cents -= 100
                        win_dollars += dollars

                    self.transfer_funds(better, win_dollars, win_cents)

                    betters.append((user, self.encode_money_string(win_dollars, win_cents, True)))

                for sender in recipients:
                    if self.outcome in self.red: 
                        colour = " (red)\n"
                    elif self.outcome in self.black: 
                        colour = " (black)\n"
                    else: 
                        colour = "\n"
                    winning_text = "The winning number is " + str(self.outcome) + colour
                    for better in betters:
                        winning_text += "\n" + better[0] + " won " + better[1] + "€"
                    self.send_message(WrappedTextMessageProtocolEntity(winning_text, to=sender))
                if not once: 
                    time.sleep(5)
            if once:
                break
            time.sleep(1)

    def evaluate_bet(self, bet):
        """
        Evaluates a bet
        :param bet: the bet
        :return: the amount won by the player
        """
        bet_type = bet["bet"]
        bet_dollars, bet_cents = self.decode_money_string(bet["value"])
        try:
            intbet = int(bet_type)
            if self.outcome == intbet:
                return self.multiply_money(35, bet_dollars, bet_cents)
            else:
                return 0, 0
        except Exception as e:
            str(e)
            if bet_type == "red":
                if self.outcome in self.red:
                    return self.multiply_money(2, bet_dollars, bet_cents)
            elif bet_type == "black":
                if self.outcome in self.black:
                    return self.multiply_money(2, bet_dollars, bet_cents)
            elif bet_type == "even":
                if self.outcome % 2 == 0:
                    return self.multiply_money(2, bet_dollars, bet_cents)
            elif bet_type == "odd":
                if self.outcome % 2 == 1:
                    return self.multiply_money(2, bet_dollars, bet_cents)
            elif bet_type.startswith("batch"):
                bet_string = bet_type.split("batch:")[1]
                bet_numbers = bet_string.split("-")
                i = 0
                while i < len(bet_numbers):
                    bet_numbers[i] = int(bet_numbers[i])
                    i += 1
                if self.outcome in bet_numbers:
                    if len(bet_numbers) == 2:
                        return self.multiply_money(18, bet_dollars, bet_cents)
                    if len(bet_numbers) == 4:
                        return self.multiply_money(9, bet_dollars, bet_cents)
            elif bet_type.startswith("group"):
                group_number = int(bet_type.split("group:")[1])
                group = []
                i = (group_number - 1) * 4
                while i < group_number * 4:
                    group.append(self.board[0][i])
                    group.append(self.board[1][i])
                    group.append(self.board[2][i])
                    i += 1
                if self.outcome in group:
                    return self.multiply_money(3, bet_dollars, bet_cents)
            elif bet_type.startswith("row"):
                row_number = int(bet_type.split("row:")[1])
                if self.outcome in self.board[row_number - 1]:
                    return self.multiply_money(3, bet_dollars, bet_cents)
            elif bet_type.startswith("half"):
                half_number = int(bet_type.split("half:")[1])
                if half_number == 1:
                    if 0 < self.outcome < 19:
                        return self.multiply_money(2, bet_dollars, bet_cents)
                else:
                    if self.outcome >= 19:
                        return self.multiply_money(2, bet_dollars, bet_cents)
        return 0, 0
