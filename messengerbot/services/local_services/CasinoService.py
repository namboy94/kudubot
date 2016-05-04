# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via the online chat services.

    messengerbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    messengerbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with messengerbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
import os
import re
import time
import random
import datetime
from typing import Dict, List

from messengerbot.servicehandlers.Service import Service
from messengerbot.connection.generic.Message import Message
from messengerbot.config.LocalConfigChecker import LocalConfigChecker


class CasinoService(Service):
    """
    The CasinoService Class that extends the generic Service class.
    The service provides the backbone for all casino-related services, like the Roulette Service
    Note: All monetary values are in cents
    """

    identifier = "casino"
    """
    The identifier for this service
    """

    has_background_process = True
    """
    Has a backround process
    """

    help_description = {"en": "/casino\tprovides basic casino functions\n"
                              "syntax:\n"
                              "/casino balance\tsends you your current balance\n"
                              "/casino beg\tlets you beg for money",
                        "de": "/casino\tBietet simple Casino Funktionen\n"
                              "syntax:\n"
                              "/casino kontostand\tSchickt den momentanen Kontostand des Nutzers\n"
                              "/casino betteln\tLässt den Nutzer für Geld betteln"}
    """
    Help description for this service.
    """

    casino_directory = os.path.join(LocalConfigChecker.services_directory, "casino")
    """
    The directory containing the casino files
    """

    user_directory = os.path.join(casino_directory, "users")
    """
    The directory storing user account files
    """

    bet_directory = os.path.join(casino_directory, "bets")
    """
    The directory storing user bets
    """

    currency = "€"
    """
    The currency used
    """

    account_balance_keywords = {"balance": "en",
                                "kontostand": "de"}
    """
    Keywords for the account balance parameter
    """

    beg_keyword = {"beg": "en",
                   "betteln": "de"}
    """
    Keywords for the beg command
    """

    beg_values = [50, 100, 200, 300, 400, 500, 30000]
    """
    Monetary Values that can be gained with begging
    """

    beg_message = {"en": ("You beg for money. You earn ", " while begging"),
                   "de": ("Du bettelst für Geld. Du verdienst ", " während dem Betteln")}
    """
    Message sent to the user if he/she begs
    """

    balance_message = {"en": "Your account balance is: ",
                       "de": "Dein Kontostand beträgt: "}
    """
    Message shown when the user requests his/her account balance
    """

    no_bets_stored = {"en": "No bets stored",
                      "de": "Keine Wetten gespeichert"}

    delete_bet_out_of_bound = {"en": "No bet with that index available",
                               "de": "Keine Wette mit dem Index verfügbar"}

    successful_bet_delete_message = {"en": "Bet successfully deleted",
                                     "de": "Wette erfolgreich gelöscht"}

    def initialize(self) -> None:
        """
        Initializes the casino directories

        :return: None
        """
        LocalConfigChecker.validate_directory(self.casino_directory)
        LocalConfigChecker.validate_directory(self.user_directory)
        LocalConfigChecker.validate_directory(self.bet_directory)

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        identifier = message.get_unique_identifier()
        option = message.message_body.lower().split("/casino ")[1]
        reply = ""

        if option in self.beg_keyword:
            self.connection.last_used_language = self.beg_keyword[option]
            reply = self.beg(identifier)
        elif option in self.account_balance_keywords:
            self.connection.last_used_language = self.account_balance_keywords[option]
            reply = self.get_balance_as_message(identifier)

        reply_message = self.generate_reply_message(message, "Casino", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^/casino " + Service.regex_string_from_dictionary_keys([CasinoService.beg_keyword,
                                                                         CasinoService.account_balance_keywords]) + "$"
        return re.search(re.compile(regex), message.message_body.lower())

    def beg(self, identifier: str) -> str:
        """
        Executes the 'beg' command, giving the user a random amount(mostly small) of money to gamble with

        :param identifier: the identifier for the user
        :return: A reply message for the user
        """
        beg_amount = random.choice(self.beg_values)
        response = self.beg_message[self.connection.last_used_language]

        self.transfer_funds(identifier, beg_amount)
        return response[0] + self.format_money_string(beg_amount) + response[1]

    def get_balance_as_message(self, identifier: str) -> str:
        """
        Gets the current balance of the user

        :param identifier: the unique identifier
        :return: the message to be sent to the user
        """
        try:
            balance = self.get_balance(identifier)
        except FileNotFoundError:
            self.create_account(identifier)
            balance = self.get_balance(identifier)

        response = self.balance_message[self.connection.last_used_language]

        return response + self.format_money_string(int(balance))

    def create_account(self, identifier: str, starting_value: int = 200000) -> None:
        """
        Creates a new user account

        :param identifier: the user identifier for whom the account is created
        :param starting_value: can be used to set a custom starting value
        :return: None
        """
        account_file = os.path.join(self.user_directory, identifier)
        with open(account_file, 'w') as account:
            account.write(str(starting_value))

    def transfer_funds(self, identifier: str, amount: int) -> None:
        """
        Transfers funds to/from an account
        It can be called with negative values to remove money from the account

        :param identifier: the user's identifier
        :param amount: the amount to transfer
        :return: None
        """
        user_exists = False
        for user_file in os.listdir(self.user_directory):
            if user_file.startswith(identifier):
                account_file = os.path.join(self.user_directory, user_file)

                user_exists = True
                current_balance = self.get_balance(identifier)

                if current_balance + amount < 0:
                    raise InsufficientFundsError()
                else:
                    with open(account_file, 'w') as account:
                        account.write(str(current_balance + amount))

        if not user_exists:
            self.create_account(identifier)
            if amount >= -200000:
                self.transfer_funds(identifier, amount)
            else:
                raise InsufficientFundsError()

    def get_balance(self, identifier: str) -> int:
        """
        Reads the current balance from the account file

        :param identifier: the user identifier
        :return: the account balance.
        """
        account_file = os.path.join(self.user_directory, identifier)
        with open(account_file, 'r') as account:
            account_balance = int(account.read())
        return account_balance

    def format_money_string(self, value: int) -> str:
        """
        Formats a cent-based monetary value into a human-readable string

        :param value: the value to be formatted
        :return: the formatted money string
        """
        cents = value % 100
        dollars = int((value - cents) / 100)
        return str(dollars) + "," + str(cents) + self.currency

    def parse_money_string(self, money_string: str) -> int:
        """
        Reads a money string and returns its value as a cent-based int value

        :param money_string: the string to be parsed
        :return: the value of that string
        """
        money = money_string.replace(self.currency, "")
        dollars, cents = money.split(",")
        value = int(cents) + (int(dollars) * 2)

        return value

    def store_bet(self, game: str, identifier: str, value: int, bet_type: str) -> None:
        """
        Stores a bet as a bet file

        :param game: the game this bet was created by
        :param identifier: te user identifier of the better
        :param value: the value set
        :param bet_type: the bet type - game-specific
        :return: None
        """
        directory = os.path.join(self.bet_directory, game)
        file_name = identifier + "###BETVAL=" + str(value)
        bet_file = os.path.join(directory, file_name)

        if os.path.isfile(bet_file):
            os.remove(bet_file)
            bet_file = bet_file.rsplit("###BETVAL=", 1)[0]
            bet_file += str(2 * value)

        with open(bet_file, 'w') as bet:
            bet.write(bet_type)

    def get_bets(self, game: str, identifier: str) -> List[Dict[str, (int or str)]]:
        """
        Returns a list of dictionaries representing bets of a specific user

        :param game: the game for which the bets should be fetched
        :param identifier: the user's identifier
        :return: the List of reminder dictionaries
        """
        directory = os.path.join(self.bet_directory, game)
        bets = []

        for bet in os.listdir(directory):
            if bet.startswith(identifier):
                bet_file = os.path.join(directory, bet)

                bet_dictionary = {"value": int(bet.rsplit("###BETVAL=", 1)[1]),
                                  "file": bet_file}
                with open(bet_file, 'r') as opened_bet_file:
                    bet_dictionary["bet_type"] = opened_bet_file.read()

                bets.append(bet_dictionary)

        bets = sorted(bets, key=lambda dictionary: dictionary["value"])
        return bets

    def get_bets_as_formatted_string(self, game: str, identifier: str) -> str:
        """
        Return all bets of a user for a specific game as a formatted string

        :param game: the game to which the bets belong
        :param identifier: the user's identifier
        :return: the formatted string
        """
        bets = self.get_bets(game, identifier)
        bet_list_string = ""

        for bet in range(1, len(bets) + 1):
            bet_list_string += str(bet) + ": " + str(bets[bet]["value"]) + "\n"
            bet_list_string += bets[bet]["bet_type"] + "\n\n"

        if bet_list_string == "":
            bet_list_string = self.no_bets_stored[self.connection.last_used_language] + game
        else:
            bet_list_string = bet_list_string.rsplit("\n\n", 1)[0]

        return bet_list_string

    def delete_bet(self, game: str, identifier: str, index: int) -> str:
        """
        Deletes a bet at the given iundex for the given game by the given user

        :param game: the game the bet to delete belongs to
        :param identifier: the user's unique identifier
        :param index: the index of the bet to delete
        :return: A message to the user
        """
        if index < 1:
            return self.delete_bet_out_of_bound[self.connection.last_used_language]

        bets = self.get_bets(game, identifier)
        os.remove(bets[index - 1]['file'])

        return self.successful_bet_delete_message[self.connection.last_used_language]

    def background_process(self) -> None:
        """
        Adds 100 € each day to each account

        :return: None
        """
        while True:
            current_time = datetime.datetime.utcnow()
            hour = int(current_time.hour)

            if hour == 23:
                for account_file in os.listdir(self.user_directory):
                    user_identifier = str(account_file.rsplit("###BETVAL=", 1)[0])
                    self.transfer_funds(user_identifier, 10000)
            time.sleep(3600)


class InsufficientFundsError(Exception):
    """
    Error to be raised when insufficient funds
    """
    pass
