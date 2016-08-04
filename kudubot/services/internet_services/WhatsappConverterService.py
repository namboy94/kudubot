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
import re
from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message
from kudubot.connection.whatsapp.WhatsappConnection import WhatsappConnection


class WhatsappConverterService(Service):
    """
    Class that converts incoming Whatsapp messages. It also allows the user to reply.
    """

    identifier = "whatsapp_convert"
    """
    The identifier for this service
    """

    help_description = {"en": "/wc\tThe Whatsapp Converter\n"
                              "syntax:\n"
                              "/wc start (starts the whatsapp converter)\n"
                              "/wc send \"recipient\" \"message\" (sends a message to the recipient)",
                        "de": "/wc\tDer Whatsapp Konvertierer\n"
                              "Syntax:\n"
                              "/wc start (startet den Whatsapp Konvertierer)\n"
                              "/wc send \"recipient\" \"message\" (sendet eine Nachricht zum Empfänger)"}
    """
    Help description for this service.
    """

    whatsapp_connection = None
    """
    The internal Whatsapp connection
    """

    owner = None
    """
    """

    def process_message(self, message: Message) -> None:
        """
        Processes the message, either starting the whatsapp connection or sending a new message

        :param message: the message to process
        :return: None
        """

        if self.connection.identifier == "whatsapp":
            # Why would we convert Whatsapp to Whatsapp? That's stupid.
            return

        if message.message_body.lower().startswith("/wc start"):

            if WhatsappConverterService.whatsapp_connection is not None:
                return

            ForwardingWhatsappConnection.establish_connection()
            WhatsappConverterService.whatsapp_connection = ForwardingWhatsappConnection.singleton_variable
            WhatsappConverterService.whatsapp_connection.set_callback(self.forward_message)
            WhatsappConverterService.owner = message.address
        else:
            receiver = message.message_body.split("\"", 1)[1].split("\"", 1)[0]
            message_text = message.message_body.rsplit("\"", 2)[1]
            whatsapp_message = Message(message_text, receiver)
            WhatsappConverterService.whatsapp_connection.send_text_message(whatsapp_message)

            # Forward to whatsapp connection
            # Problems: How do we identify the recipient number?
            # Store in Database?
            # IDK

    def forward_message(self, message: Message) -> None:
        """

        :return:
        """
        message_text = "FROM:" + message.address + "\n\n" + message.message_body
        forward_message = Message(message_text, WhatsappConverterService.owner)
        self.connection.send_text_message(forward_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^/wc (start|msg \"[^\"]+\" \"[^\"]+\")$"
        return re.search(re.compile(regex), message.message_body.lower())


class ForwardingWhatsappConnection(WhatsappConnection):
    """
    Wrapper around the Whatsapp Connection class that starts a whatsapp connection that reports the incoming
    Whatsapp messages and can also send Whatsapp messages
    """

    singleton_variable = None
    callback = None

    def initialize(self) -> None:
        """
        Used to initialize stuff instead of the constructor
        :return: None
        """
        self.singleton_variable = self

    def set_callback(self, callback: callable) -> None:
        """

        :param callback:
        :return:
        """
        self.callback = callback

    def on_incoming_message(self, message: Message) -> None:
        """
        Handles incoming messages
        :param message:
        :return:
        """
        while self.callback is None:
            pass
        self.callback(message)

    @staticmethod
    def establish_connection():
        """
        :return: None
        """
        super().establish_connection()
        while ForwardingWhatsappConnection.singleton_variable is None:
            pass
