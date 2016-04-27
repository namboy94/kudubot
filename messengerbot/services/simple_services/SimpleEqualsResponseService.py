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

from messengerbot.servicehandlers.Service import Service
from messengerbot.connection.generic.Connection import Connection
from messengerbot.connection.generic.Message import Message


class SimpleEqualsResponseService(Service):
    """
    The SimpleEqualsResponseService Class that extends the generic Service class.
    The service responds to strings that exactly match pre-defined options
    """

    case_insensitive_options = {"uptime": "Much too long, I'm tired"}
    """
    Case-insensitive defined response conditions and responses
    """

    case_sensitive_options = {"ping": "pong",
                              "Ping": "Pong"}
    """
    Case-sensitive defined response conditions and responses
    """

    def __init__(self, connection: Connection) -> None:
        """
        Constructor of the SimpleEqualsResponseService class.
        It defines parameters for the plugin.

        :param connection: The connection defined
        :return: None
        """
        super().__init__(connection)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this plugin to continue

        :return: True if input is valid, False otherwise
        """
        for option in SimpleEqualsResponseService.case_sensitive_options:
            if option == message.message_body:
                return True
        for option in SimpleEqualsResponseService.case_insensitive_options:
            if option == message.message_body.lower():
                return True
        return False

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        try:
            reply = self.case_sensitive_options[message.message_body]
        except KeyError:
            reply = self.case_insensitive_options[message.message_body.lower()]

        reply_message = Message(reply, "Simple Equals Response", message.address, False)
        self.send_text_message(reply_message)

    @staticmethod
    def get_description(language):
        """
        Empty description, since this plugin doesn't really provide any functionality

        :param language: the language to be returned
        :return: an empty string
        """
        return ""

    @staticmethod
    def get_plugin_name():
        """
        Returns the plugin name
        :return: the plugin name
        """
        return "Simple Equals Plugin"
