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
import re
import random
import string

from messengerbot.servicehandlers.Service import Service
from messengerbot.connection.generic.Message import Message


class RandomKeyGeneratorService(Service):
    """
    The RandomKeyGeneratorService Class that extends the generic Service class.
    The service sends a random key of specified length
    """

    identifier = "random_key_generator"
    """
    The identifier for this service
    """

    help_description = {"en": "/randomkey\tgenerates a random key\n"
                              "syntax:\n"
                              "/randomkey <length>",
                        "de": "/zufallschlüssel\tgeneriert einen zufälligen Schlüssel\n"
                              "syntax:\n"
                              "/zufallschlüssel <Länge>"}
    """
    Help description for this service.
    """

    alphabet = string.ascii_letters + string.digits + string.punctuation
    """
    The alphabet to be used to generate a random key
    """

    random_key_keywords = {"/randomkey": "en",
                           "/zufallschlüssel": "de"}
    """
    Keywords for the /randomkey command
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        language, length = message.message_body.lower().split(" ", 1)
        self.connection.last_used_language = self.random_key_keywords[language]

        reply = self.generate_key(int(length))
        reply_message = self.generate_reply_message(message, "Random Key", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^" + Service.regex_string_from_dictionary_keys([RandomKeyGeneratorService.random_key_keywords]) \
                + " [0-9]+$"
        return re.search(re.compile(regex), message.message_body.lower())

    def generate_key(self, length: int) -> str:
        """
        Generates a random key of specified length using the alphabet specified as class variable

        :param length: the length of the keyphrase
        :return: the random key
        """
        random_key = ""
        for x in range(0, length):
            random_key += random.choice(self.alphabet)
        return random_key
