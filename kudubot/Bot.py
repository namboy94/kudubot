"""LICENSE
Copyright 2015 Hermann Krumrey <hermann@krumreyh.com>

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
LICENSE"""

import os
import logging
from typing import Type, Optional, List
from threading import Thread
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker
from bokkichat.connection.Connection import Connection
from bokkichat.entities.message.Message import Message
from bokkichat.entities.message.TextMessage import TextMessage
from kudubot.db import Base
from kudubot.db.Address import Address as Address
from kudubot.db.config.impl.SqlteConfig import SqliteConfig
from kudubot.exceptions import ConfigurationError
from kudubot.parsing.CommandParser import CommandParser


class Bot:
    """
    The Bot class offers an abstraction layer above
    """

    def __init__(
            self,
            connection: Connection,
            location: str,
            db_uri: Optional[str] = None
    ):
        """
        Initializes the bot
        :param connection: The connection the bot should use
        :param location: The location of config and DB files
        :param db_uri: Specifies a custom database URI
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Initializing Bot")

        self.connection = connection
        self.location = location
        if not os.path.isdir(location):
            raise ConfigurationError("Invalid configuration directory")

        self.settings_file_path = os.path.join(location, "settings.json")
        if not os.path.isfile(self.settings_file_path):
            raise ConfigurationError("Missing settings")

        self.sqlite_path = os.path.join(location, "data.db")
        if db_uri is None:
            db_uri = SqliteConfig(self.sqlite_path).to_uri()
        self.db_uri = db_uri

        self.db_engine = create_engine(self.db_uri)
        Base.metadata.create_all(self.db_engine, checkfirst=True)

        self._sessionmaker = sessionmaker(bind=self.db_engine)
        self.db_session = self.create_db_session()

        self.bg_thread = Thread(target=self.run_in_bg, daemon=True)

    def on_msg(self, message: Message, address: Address):
        """
        The callback method is called for every received message.
        This method defines the main functionality of a bot
        :param message: The received message
        :param address: The address of the sender in the database
        :return: None
        """
        raise NotImplementedError()

    @property
    def name(self) -> str:
        """
        :return: The name of the bot
        """
        raise NotImplementedError()

    @property
    def parsers(self) -> List[CommandParser]:
        """
        :return: A list of parser the bot supports for commands
        """
        raise NotImplementedError()

    def run_in_bg(self):
        """
        Method that is started when the bot is started.
        By default this does nothing, for functionality must be extended
        by subclasses.
        :return: None
        """
        pass

    def pre_callback(self, _: Connection, message: Message) -> bool:
        """
        Prepares the callback and decides whether or not the callback
        is even executed
        :param _: The connection to use
        :param message: The message to check
        :return: True if the execution continues, False otherwise
        """
        _continue = True
        _continue = _continue and self._store_in_address_book(message)
        _continue = _continue and self._handle_help_command(message)
        _continue = _continue and self._handle_ping(message)
        return _continue

    def start(self):
        """
        Starts the bot using the implemented callback function
        :return: None
        """
        self.logger.info("Starting Bot")

        def loop_callback(connection: Connection, message: Message):

            self.logger.info("Received message {}".format(message))

            if self.pre_callback(connection, message):
                address = self.db_session.query(Address)\
                    .filter_by(address=message.sender.address).first()
                self.on_msg(message, address)

        self.bg_thread.start()
        self.connection.loop(callback=loop_callback)

    def create_db_session(self) -> Session:
        """
        Creates a new database session
        :return: The database session
        """
        return self._sessionmaker()

    def save_config(self):
        """
        Saves the configuration for this bot
        :return: None
        """
        with open(self.settings_file_path, "w") as f:
            f.write(self.connection.settings.serialize())

    @classmethod
    def load(cls, connection_cls: Type[Connection], location: str):
        """
        Generates a Bot from the location.
        :param connection_cls: The class of the connection
        :param location: The location of the bot configuration directory
        :return: The generated bot
        """
        settings_file = os.path.join(location, "settings.json")
        if not os.path.isfile(settings_file):
            raise ConfigurationError("Missing settings file")

        with open(settings_file, "r") as f:
            serialized = f.read()
        connection = connection_cls.from_serialized_settings(serialized)
        return cls(connection, location)

    @staticmethod
    def create_config(connection_cls: Type[Connection], path: str):
        """
        Creates a configuration directory for a bot
        :param connection_cls: The connection class for
                               which to generate a config
        :param path: The path of the configuration directory
        :return: None
        """
        if not os.path.isdir(path):
            os.makedirs(path)

        settings_path = os.path.join(path, "settings.json")
        settings = connection_cls.settings_cls().prompt()

        with open(settings_path, "w") as f:
            f.write(settings.serialize())

    def _store_in_address_book(self, message: Message) -> bool:
        """
        Stores an address in the bot's address book
        :param message: The received message
        :return: Whether or not handling the message should continue
        """
        exists = self.db_session.query(Address) \
            .filter_by(address=message.sender.address).first()

        if exists is None:
            entry = Address(address=message.sender.address)
            self.db_session.add(entry)
            self.db_session.commit()
        return True

    def _handle_help_command(self, message: Message) -> bool:
        """
        Handles the /help command.
        :param message: The message to check for a /help command
        :return: Whether or not handling the message should continue
        """
        if message.is_text():
            message = message  # type: TextMessage
        else:
            return True

        if message.body.lower().strip() == "/help":

            help_message = "Help message for {}\n\n".format(self.name)
            for parser in self.parsers:
                help_message += parser.help_text + "\n\n"

            reply = message.make_reply(
                title="Help Message", body=help_message
            )
            self.connection.send(reply)
            return False
        else:
            return True

    def _handle_ping(self, message: Message) -> bool:
        """
        Handles PING messages
        :param message: The message to analyze
        :return: Whether or not handling the message should continue
        """
        if message.is_text():
            message = message  # type: TextMessage
        else:
            return True

        if message.body.lower().strip() == "ping":
            reply = message.make_reply(title="Pong", body="Pong")
            self.connection.send(reply)
            return False
        else:
            return True
