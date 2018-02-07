# -*- coding: utf-8 -*-
"""
Copyright 2015-2017 Hermann Krumrey

This file is part of kudubot.

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
"""

import logging
from typing import List
from threading import Thread
from kudubot.entities.Message import Message


class BaseService(object):
    """
    A class that defines how a chat bot service integrates with a Connection.
    Includes various helper methods.
    """

    @staticmethod
    def define_identifier() -> str:
        """
        Defines the unique identifier for the service

        :return: The Service's identifier.
        """
        raise NotImplementedError()

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

    def __init__(self, connection):
        """
        Initializes the Service using a specified Connection

        :param connection: The connection used by this service
        """
        self.connection = connection
        self.identifier = self.define_identifier()
        self.logger = logging.getLogger(self.__class__.__module__)
        self.init()
        self.logger.debug(self.identifier + " Service initialized")

    # noinspection PyMethodMayBeStatic
    def init(self):
        """
        Helper method that runs after the initialization of the Service object.
        Can be used for anything, but normal use cases would include
        initializing a database table or starting a background thread

        :return: None
        """
        pass

    # -------------------------------------------------------------------------
    #                  _,-'/-'/                                Here be dragons!
    #  .      __,-; ,'( '/
    #   \.    `-.__`-._`:_,-._       _ , . ``
    #    `:-._,------' ` _,`--` -: `_ , ` ,' :
    #       `---..__,,--'            ` -'. -'
    # Everything below this should not be overridden by subclasses
    # -------------------------------------------------------------------------

    def reply(self, title: str, body: str, message: Message):
        """
        Provides a helper method that streamlines the process
        of replying to a message.
        Very useful for Services that send a reply immediately
        to cut down on clutter in the code

        :param title: The title of the message to send
        :param body: The body of the message to send
        :param message: The message to reply to
        :return: None
        """
        reply_message = Message(
            title, body, message.get_direct_response_contact(),
            self.connection.user_contact
        )
        self.connection.send_message(reply_message)

    def is_applicable_to_with_log(self, message: Message) -> bool:
        """
        Wrapper around the is_applicable_to method,
        which enables logging the message easily
        for all subclasses

        :param message: The message to analyze
        :return: True if the message is applicable, False otherwise
        """
        self.logger.debug("Checking if " + message.message_body +
                          " is applicable")

        # Check if a subclass is_applicable fits here
        # This construct is required to avoid having to call super()
        # in implemented service classes, which can not be enforced or
        # hinted at via an IDE
        for subclass in [
            "multi_language", "authenticated", "helper", "external"
        ]:
            is_applicable_method = \
                getattr(self, "is_applicable_to_" + subclass, None)
            if callable(is_applicable_method):
                if is_applicable_method(message):
                    self.logger.debug("Message is applicable")
                    return True
                elif subclass == "authenticated":
                    self.reply("Access Denied", "Access Denied ❌", message)
                    return False

        result = self.is_applicable_to(message)
        not_word = "" if result else "not"
        self.logger.debug("Message is " + not_word + " applicable")
        return result

    def handle_message_with_log(self, message: Message):
        """
        Wrapper around the handle_message method,
        which enables logging the message easily
        for all subclasses

        :param message: The message to handle
        :return: None
        """
        self.logger.debug("Handling message " + message.message_body)

        # Checks if a parent class of the service is applicable, if yes,
        # Runs their handle_message method
        for subclass in [
            "multi_language", "authenticated", "helper", "external"
        ]:
            is_applicable_method = \
                getattr(self, "is_applicable_to_" + subclass, None)
            handle_method = getattr(self, "handle_message_" + subclass, None)

            if callable(is_applicable_method) and callable(handle_method):

                if is_applicable_method(message):
                    handle_method(message)
                    return

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
    def initialize_database_table(self, sql: List[str] = [],
                                  initializer: callable=None):
        """
        Executes the provided SQL queries to create the database table(s).

        :param sql: The SQL queries used to create the database tables
        :param initializer: A method that initializes
                            the database connection itself.
        :return: None
        """
        self.logger.debug("Initializing Database table" +
                          ("" if len(sql) < 2 else "s") +
                          " for " + self.identifier)
        for statement in sql:
            self.connection.db.execute(statement)
        if initializer is not None:
            initializer(self.connection.db)
