# coding=utf-8
"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of kudubot.

    kudubot makes use of various third-party python modules to serve
    information via online chat services.

    kudubot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    kudubot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with kudubot.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
import os
import re
from datetime import timedelta

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message
from kudubot.resources.images.__init__ import get_location as get_resource


class SimpleCommandsService(Service):
    """
    The SimpleCommandsService Class that extends the generic Service class.
    The service offers several trivial commands to the user
    """

    identifier = "simple_commands"
    """
    The identifier for this service
    """

    help_description = {"en": "Simple Commands: Collection of Commands that do simple things\n"
                              "/uptime\tDisplays the uptime of the server running the bot\n"
                              "/sl\tlike ls, but different.",
                        "de": "Simple Befehle: Sammlung von Befehlen die simple Sachen machen\n"
                              "/upzeit\tZeigt die 'uptime' des Servers auf dem der Bot läuft\n"
                              "/sl\twie ls, aber anders"}
    """
    Help description for this service.
    """

    commands = {"/uptime": "en",
                "/upzeit": "de",
                "/sl": "en"}
    """
    List of commands together with the language they are in and the method they call (initialized in initialize())
    """

    uptime_no_uptime_file = {"en": "Uptime command unavailable on this platform",
                             "de": "Upzeit Befehl auf dieser Platform nicht unterstützt"}

    def initialize(self) -> None:
        """
        Initializes the commands dictionary

        :return: None
        """
        self.commands = {"/uptime": ("en", self.get_uptime),
                         "/upzeit": ("de", self.get_uptime),
                         "/sl": ("en", self.steam_locomotive)}

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        self.connection.last_used_language = self.commands[message.message_body.lower()][0]
        command = self.commands[message.message_body.lower()][1]
        command(message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^" + Service.regex_string_from_dictionary_keys([SimpleCommandsService.commands]) + "$"
        return re.search(re.compile(regex), message.message_body.lower())

    def get_uptime(self, message: Message) -> None:
        """
        Calculates the host PC's uptime and sends it to the sender

        :param message: The received message
        :return: None
        """
        if not os.path.isfile('/proc/uptime'):
            reply = self.uptime_no_uptime_file[self.connection.last_used_language]

        else:
            with open('/proc/uptime', 'r') as uptime_file:
                uptime_seconds = float(uptime_file.readline().split()[0])
                uptime_string = str(timedelta(seconds=uptime_seconds))
            reply = "Uptime: " + uptime_string

        reply_message = self.generate_reply_message(message, "Uptime", reply)
        self.send_text_message(reply_message)

    def steam_locomotive(self, message: Message) -> None:
        """
        Sends an image of a Steam locomotive to the sender

        :param message: the received message
        :return: None
        """
        image_file = get_resource("sl.jpg")
        self.send_image_message(message.address, image_file)
