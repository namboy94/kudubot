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
import traceback
from threading import Thread
from kudubot.logger.ExceptionLogger import ExceptionLogger
from kudubot.connection.whatsapp.stacks.YowsupEchoStack import YowsupEchoStack
from kudubot.logger.PrintLogger import PrintLogger
from kudubot.connection.whatsapp.parsers.WhatsappConfigParser import WhatsappConfigParser
from kudubot.connection.generic.Message import Message
from kudubot.connection.whatsapp.WhatsappConnection import WhatsappConnection


class ForwardedWhatsappConnection(WhatsappConnection):
    """
    Wrapper around the Whatsapp Connection class that starts a whatsapp connection that reports the incoming
    Whatsapp messages and can also send Whatsapp messages
    """

    singleton_variable = None
    """
    Used to store the forwarded Whatsapp Connection class
    """

    callback = None
    """
    Callback method called whenever an incoming message is received
    """

    def initialize(self) -> None:
        """
        Initializes the singleton veriable with itself

        :return: None
        """
        super().initialize()
        ForwardedWhatsappConnection.singleton_variable = self

    def set_callback(self, callback: callable) -> None:
        """
        Sets the callback method

        :param callback: the callback method
        :return: None
        """
        self.callback = callback

    def process_message(self, message: Message) -> None:
        """
        Handles incoming messages, calls the callback method
        Also waits until callback method is initialized by outer source

        :param message: the message to process
        :return: None
        """
        while self.callback is None:
            pass

        self.callback(message)

    @staticmethod
    def establish_connection():
        """
        Establishes the connection in a different daemon thread

        :return: None
        """

        def start_connection():
            """
            Starts the actual whatsapp connection

            :return: None
            """
            credentials = WhatsappConfigParser.parse_whatsapp_config(WhatsappConnection.identifier)

            while True:
                try:
                    PrintLogger.print("Starting Whatsapp Forwarding Connection", 1)
                    echo_stack = YowsupEchoStack(ForwardedWhatsappConnection, credentials)
                    echo_stack.start()
                except Exception as e:
                    stack_trace = traceback.format_exc()
                    ExceptionLogger.log_exception(e, stack_trace, "whatsapp Forwarder")

        thread = Thread(target=start_connection)
        thread.daemon = True
        thread.start()

        while ForwardedWhatsappConnection.singleton_variable is None:
            pass
