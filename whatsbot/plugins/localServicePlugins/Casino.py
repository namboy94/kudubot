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
import time
import datetime
import configparser

try:
    from plugins.GenericPlugin import GenericPlugin
    from yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity
except ImportError:
    from whatsbot.plugins.GenericPlugin import GenericPlugin
    from whatsbot.yowsupwrapper.entities.WrappedTextMessageProtocolEntity import WrappedTextMessageProtocolEntity


class Casino(GenericPlugin):
    """
    The Casino Class
    """

    casino_dir = os.getenv("HOME") + "/.whatsbot/casino/"
    user_dir = casino_dir + "users/"

    def __init__(self, layer, message_protocol_entity=None):
        """
        Constructor
        Defines parameters for the plugin.
        :param layer: the overlying yowsup layer
        :param message_protocol_entity: the received message information
        :return: void
        """
        super().__init__(layer, message_protocol_entity)

        if self.entity is not None:
            self.user = self.participant
            self.user_id = self.user.split("@")[0]
            self.user_nick = self.notify
            self.reply = None

    def regex_check(self):
        """
        Checks if the user input is valid for this plugin to continue
        :return: True if input is valid, False otherwise
        """
        return re.search(r"^/casino (balance|beg)$", self.message)

    def parse_user_input(self):
        """
        Parses the user's input
        :return: void
        """
        self.create_user(self.entity)
        mode = self.message.split("/casino ")[1]

        reply_text = ""
        if mode == "balance":
            balance = self.get_balance(self.user_id)
            reply_text = "Your balance is: " + self.encode_money_string(balance[0], balance[1], True) + "€"
        elif mode == "beg":
            self.transfer_funds(self.user_id, 1, 0)
            reply_text = "You earn 1€ while begging for money"
        self.reply = WrappedTextMessageProtocolEntity(reply_text, to=self.sender)

    def get_response(self):
        """
        Returns the response calculated by the plugin
        :return: the response as a WrappedTextMessageProtocolEntity
        """
        return self.reply

    @staticmethod
    def get_description(language):
        """
        Returns a helpful description of the plugin's syntax and functionality
        :param language: the language to be returned
        :return: the description as string
        """
        if language == "en":
            return "/casino\tprovides basic casino functions\n" \
                   "syntax:\n" \
                   "/casino balance\tsends you your current balance"
        elif language == "de":
            return "/casino\tBietet simple Casino Funktionen\n" \
                   "syntax:\n" \
                   "/casino balance\tSchickt den momentanen Kontostand des Nutzers"
        else:
            return "Help not available in this language"

    @staticmethod
    def get_plugin_name():
        """
        Returns the plugin name
        :return: the plugin name
        """
        return "Casino Plugin"

    def parallel_run(self):
        """
        Starts a parallel background activity if this class has one.
        :return: void
        """
        while True:
            current_time = datetime.datetime.now()
            hours = int(current_time.hour)
            if not hours < 23:
                for user in os.listdir(self.user_dir):
                    self.transfer_funds(user, 2000, 0)
            time.sleep(3600)
            
    # Private methods
    def create_user(self, message_entity):
        """
        Creates a new user file
        :param message_entity: a messageEntity sent from the user
        :return: void
        """
        user_id = message_entity.get_participant()
        if not user_id:
            user_id = message_entity.get_from(False)
        user_id = user_id.split("@")[0]
        user_nick = message_entity.get_notify()
        user_file = self.user_dir + user_id

        if not os.path.isfile(user_file):
            self.generate_user(user_id, user_nick, "1000.00")

    def generate_user(self, user_id, user_nick, balance):
        """
        Generates a user account
        :param user_id: the user's ID
        :param user_nick: the user's (nick)name
        :param balance: the user's balance
        :return: void
        """
        user_file = self.user_dir + user_id
        file = open(user_file, "w")
        file.write("[account]\n")
        file.write("nick=" + user_nick + "\n")
        file.write("balance=" + balance)

    def get_user_nick(self, user_id):
        """
        Gets the user's (nick)name from his/her account
        :param user_id: the user's ID
        :return: the user's (nick)name
        """
        user_file = self.user_dir + user_id
        user_details = configparser.ConfigParser()
        user_details.read(user_file)
        nick = dict(user_details.items("account"))["nick"]
        return nick

    def get_balance(self, user_id):
        """
        Gets the balance of a user
        :param user_id: the user's ID
        :return: the user's balance
        """
        user_file = self.user_dir + user_id
        user_details = configparser.ConfigParser()
        user_details.read(user_file)
        balance = dict(user_details.items("account"))["balance"]
        return self.decode_money_string(balance)

    def set_balance(self, user_id, dollars, cents):
        """
        Sets a user's balance to a specified value
        :param user_id: the user's ID
        :param dollars: the amount of dollars
        :param cents: the amount of cents
        :return: void
        """
        balance_string = self.encode_money_string(dollars, cents)
        user_nick = self.get_user_nick(user_id)
        self.generate_user(user_id, user_nick, balance_string)

    @staticmethod
    def decode_money_string(money_string):
        """
        Decodes a money string
        :param money_string: the String to be decoded
        :return: the monetary value as a tuple of dollars and cents
        """
        dollars = int(money_string.split(".")[0])
        try:
            cents = money_string.split(".")[1]
            if len(cents) < 2:
                cents += "0"
            cents = int(cents)
        except ValueError:
            cents = 0
        return dollars, cents

    @staticmethod
    def encode_money_string(dollars, cents, delimiters=False):
        """
        Encodes a tuple of dollars and cents to a moneyString
        :param dollars: the amount of dollars
        :param cents: the amount of cents
        :param delimiters: switch for enabling delimiters
        :return: the encoded dollar string
        """
        cent_string = str(cents)
        if len(cent_string) < 2:
            cent_string = "0" + cent_string
        if len(cent_string) < 2:
            cent_string = "0" + cent_string
        if not delimiters:
            return str(dollars) + "." + cent_string
        else:
            dollar_string = str(dollars)
            dollar_list = []
            for char in dollar_string:
                dollar_list.insert(0, char)
            formated_dollar_string = ""
            i = 0
            while i < len(dollar_list):
                if i > 0 and i % 3 == 0:
                    formated_dollar_string = " " + formated_dollar_string
                formated_dollar_string = dollar_list[i] + formated_dollar_string
                i += 1
            return formated_dollar_string + "." + cent_string

    @staticmethod
    def multiply_money(factor, dollars, cents):
        """
        Multiplies a monetary value by a given factor
        :param factor: the actor with which to multiply
        :param dollars: the initial amount of dollars
        :param cents: the initial amount of cents
        :return: the multiplied monetary value as a tuple of dollars and cents
        """
        multiplied_dollars = factor * dollars
        multiplied_cents = factor * cents
        while multiplied_cents >= 100:
            multiplied_cents -= 100
            multiplied_dollars += 1
        return multiplied_dollars, multiplied_cents

    def transfer_funds(self, user_id, dollars, cents):
        """
        Adds or subtracts an amount from the balance of a player
        :param user_id: the user's ID
        :param dollars: the amount of dollars to be transferred
        :param cents: the amount of cents to be transferred
        :return: void
        """
        current_dollars, current_cents = self.get_balance(user_id)
        new_cents = current_cents + cents
        while new_cents >= 100:
            current_dollars += 1
            new_cents -= 100
        while new_cents < 0:
            current_dollars -= 1
            new_cents += 100
        new_dollars = current_dollars + dollars
        self.set_balance(user_id, new_dollars, new_cents)

    def has_sufficient_funds(self, user_id, dollars, cents):
        """
        Checks if a user has enough funds for a specified bet
        :param user_id: the user's ID
        :param dollars: the amount of dollars to be bet
        :param cents: the amount of cents to be bet
        :return: True if the user has enough funds, False otherwise
        """
        current_dollars, current_cents = self.get_balance(user_id)
        current_money = (current_dollars * 100) + current_cents
        query_value = (dollars * 100) + cents
        return query_value <= current_money

    def store_bet(self, game, user_id, sender, dollars, cents, bet_type):
        """
        Stores a bet to a user's bet file
        :param game: the game played
        :param user_id: the user's ID
        :param sender: the sender of the bet
        :param dollars: the bet mount (dollars)
        :param cents: the bet amount (cents)
        :param bet_type: the bet type identifier
        """
        bet_string = sender + ";" + self.encode_money_string(dollars, cents) + ";" + bet_type + "\n"
        user_bets = open(self.casino_dir + game + "/" + user_id, "a")
        user_bets.write(bet_string)
        user_bets.close()

    def get_bets(self, game, user_id):
        """
        Gets the bets from a user's bet file
        :param game: the game played
        :param user_id: the user's ID
        :return: the bets as a list of strings
        """
        bet_file = open(self.casino_dir + game + "/" + user_id, "r")
        raw_bets = bet_file.read().split("\n")
        raw_bets.pop()
        bet_file.close()
        bets = []

        for bet in raw_bets:
            bet_parts = bet.split(";")
            bet_dict = {"sender": bet_parts[0], "value": bet_parts[1], "bet": bet_parts[2]}
            bets.append(bet_dict)

        return bets

    def get_bet_strings(self, game, user_id):
        """
        Gets the bets of a user as strings
        :param game: the game played
        :param user_id: the user's ID
        :return: the bets as a string
        """
        bet_string = "You have bet on the following:"
        try:
            bets = self.get_bets(game, user_id)
            for bet in bets:
                dollars, cents = self.decode_money_string(bet["value"])
                bet_val = self.encode_money_string(dollars, cents, True)
                bet_string += "\nBet: " + bet["bet"] + "     Amount: " + bet_val + "€"
        except Exception as e:
            str(e)
        return bet_string
