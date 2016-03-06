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

import re
import os
import random
import datetime

from plugins.localServicePlugins.Casino import Casino
from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class BlackJack(Casino):
    """
    The BlackJack Class
    """

    in_game = False
    mode = ""
    outcome = ""
    insufficient_funds = False

    def regex_check(self):
        """
        Checks if the user input is valid for this plugin to continue
        :return: True if input is valid, False otherwise
        """
        if re.search(r"^/blackjack (start ([0-9]+(\.[0-9]{2})?)|hit|stay)$", self.message):
            return True

    def parse_user_input(self):
        """
        Parses the user's input
        :return: void
        """
        self.create_user(self.entity)
        self.mode = self.message.split(" ")[1]
        if self.mode == "start":
            if os.path.isdir(self.casino_dir + "blackjack/" + self.user_id):
                self.in_game = True
            else:
                dollars, cents = self.decode_money_string(self.message.split(" ")[2])
                self.store_bet("blackjack", self.user_id, self.sender, dollars, cents, "start")

    def get_response(self):
        """
        Returns the response calculated by the plugin
        :return: the response as a WrappedTextMessageProtocolEntity
        """
        if self.mode == "newBet":
            if self.insufficient_funds:
                return WrappedTextMessageProtocolEntity("Insufficient Funds", to=self.sender)
            else:
                return WrappedTextMessageProtocolEntity("Bet Saved", to=self.sender)
        elif self.mode == "bets":
            return WrappedTextMessageProtocolEntity(self.get_bet_strings("roulette", self.user_id), to=self.sender)
        elif self.mode == "time":
            current_time = datetime.datetime.now()
            current_minute = int(current_time.minute)
            current_second = int(current_time.second)
            time_left = 120 - current_second - 5
            if current_minute % 2 == 1:
                time_left -= 60
            self.layer.toLower(WrappedTextMessageProtocolEntity(str(time_left) + "s to turn.", to=self.sender))

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

    def evaluate_bet(self, bet):
        """
        Evaluates a bet
        :return: the amount won by the player
        """
        str(bet)
        str(self)
        return 0, 0

    @staticmethod
    def draw_card():
        """
        Draws a random card
        :return: the random card number
        """
        return random.randint(2, 11)
