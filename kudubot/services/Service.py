"""
LICENSE:
Copyright 2015-2017 Hermann Krumrey

This file is part of kudubot.

    kudubot is a chat bot framework. It allows developers to write
    services for arbitrary chat services.

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

import logging
from typing import List
from kudubot.entities.Message import Message
from threading import Thread


class Service(object):
    """
    A class that defines how a chat bot service integrates with a Connection
    """

    def __init__(self, connection  # Connection  (Can't import due to circular imports)
                 ):
        """
        Initializes the Service using a specified Connection

        :param connection: The connection used by this service
        """
        self.connection = connection
        self.identifier = self.define_identifier()
        self.requires = self.define_requirements()
        self.logger = logging.getLogger(self.__class__.__module__)
        self.init()
        self.logger.debug(self.identifier + " Service initialized")

    # noinspection PyMethodMayBeStatic
    def init(self):
        """
        Helper method that runs after the initialization of the Service object. Can be used for
        anything, but normal use cases would include initializing a database table or
        starting a background thread

        :return: None
        """
        pass

    def is_applicable_to_with_log(self, message: Message) -> bool:
        """
        Wrapper around the is_applicable_to method, which enables logging the message easily
        for all subclasses

        :param message: The message to analyze
        :return: True if the message is applicable, False otherwise
        """
        self.logger.debug("Checking if " + message.message_body + "is applicable")
        result = self.is_applicable_to(message)
        self.logger.debug("Message is " + ("" if result else "not") + " applicable")
        return result

    def handle_message_with_log(self, message: Message):
        """
        Wrapper around the handle_message method, which enables logging the message easily
        for all subclasses

        :param message: The message to handle
        :return: None
        """
        self.logger.debug("Handling message " + message.message_body)
        self.handle_message(message)

    # noinspection PyMethodMayBeStatic
    def start_daemon_thread(self, target: callable) -> Thread:
        """
        Starts a daemon/background thread
        :param target: The target function to execute as a separate thread
        :return: The thread
        """
        self.logger.debug("Starting background thread for " + self.identifier)

        thread = Thread(target=target)
        thread.daemon = True
        thread.start()
        return thread

    # noinspection PyDefaultArgument
    def initialize_database_table(self, sql: List[str] = [], initializer: callable=None):
        """
        Executes the provided SQL queries to create the database table(s).

        :param sql: The SQL queries used to create the database tables
        :param initializer: A method that initializes the database connection itself.
        :return: None
        """
        self.logger.debug("Initializing Database table" + ("" if len(sql) < 2 else "s") + " for " + self.identifier)
        for statement in sql:
            self.connection.db.execute(statement)
        if initializer is not None:
            initializer(self.connection.db)

    def is_applicable_to(self, message: Message) -> bool:
        """
        Checks if the Service is applicable to a given message

        :param message: The message to check
        :return: True if applicable, else False
        """
        raise NotImplementedError()

    def handle_message(self, message: Message):
        """
        Handles the message, provided this service is applicable to it

        :param message: The message to process
        :return: None
        """
        raise NotImplementedError()

    @staticmethod
    def define_identifier() -> str:
        """
        Defines the unique identifier for the service

        :return: The Service's identifier.
        """
        raise NotImplementedError()

    @staticmethod
    def define_requirements() -> List[str]:
        """
        Defines the requirements for the service

        :return: The required services for this Service.
        """
        raise NotImplementedError()

    def reply(self, title: str, body: str, message: Message):
        """
        Provides a helper method that streamlines the process of replying to a message. Very useful
        for Services that send a reply immediately to cut down on clutter in the code

        :param title: The title of the message to send
        :param body: The body of the message to send
        :param message: The message to reply to
        :return: None
        """
        reply_message = Message(title, body, message.get_direct_response_contact(), self.connection.user_contact)
        self.connection.send_message(reply_message)
