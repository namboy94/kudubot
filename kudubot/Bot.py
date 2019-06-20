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
import json
import logging
from threading import Thread
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker
from bokkichat.exceptions import InvalidSettings
from bokkichat.connection.Connection import Connection
from bokkichat.entities.message.Message import Message
from bokkichat.entities.message.TextMessage import TextMessage
from kudubot.db import Base
from kudubot.db.Address import Address as Address
from kudubot.db.config.impl.SqlteConfig import SqliteConfig
from kudubot.exceptions import ConfigurationError, ParseError
from kudubot.parsing.CommandParser import CommandParser
from typing import Type, Optional, List, Tuple, Dict, Any, cast


class Bot:
    """
    The Bot class offers an abstraction layer above bokkichat
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

        self.logfile = os.path.join(location, "kudubot.log")
        log_file_handler = logging.FileHandler(self.logfile)
        log_file_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(log_file_handler)
        self.connection.logger.addHandler(log_file_handler)

        self.connection_file_path = os.path.join(location, "connection.json")
        if not os.path.isfile(self.connection_file_path):
            raise ConfigurationError("Missing connection settings")

        self.extras = {}
        self.extras_file_path = os.path.join(location, "extras.json")
        if len(self.extra_config_args()) > 0:
            if not os.path.isfile(self.extras_file_path):
                raise ConfigurationError("Missing extra settings")
            else:
                with open(self.extras_file_path, "r") as f:
                    self.extras = json.load(f)
                    for arg in self.extra_config_args():
                        if arg not in self.extras:
                            raise ConfigurationError(
                                "Missing extra settings parameter " + arg
                            )

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

    @classmethod
    def name(cls) -> str:
        """
        :return: The name of the bot
        """
        raise NotImplementedError()

    @classmethod
    def parsers(cls) -> List[CommandParser]:
        """
        :return: A list of parser the bot supports for commands
        """
        raise NotImplementedError()

    @classmethod
    def extra_config_args(cls) -> List[str]:
        """
        :return: A list of additional settings parameters required for
                 this bot. Will be stored in a separate extras.json file
        """
        return []

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

        try:
            self.connection.loop(callback=loop_callback)
        except ConfigurationError as e:
            raise e
        except BaseException as e:
            self.logger.error("Fatal Exception: {} {}: {}".format(
                e, type(e), e.args
            ))
            raise e

    def parse(self, message: Message) \
            -> Optional[Tuple[CommandParser, str, Dict[str, Any]]]:
        """
        Parses the received message to check which parser and command
        are applicable to the message.
        :param message: The message to parse
        :return: The resulting parser/command combination
        """
        if not message.is_text():
            return None
        message = cast(TextMessage, message)
        body = message.body.strip()
        lower_body = body.lower()

        selected_parser = None
        if len(self.parsers()) > 1:
            if not lower_body.startswith("!"):
                return None
            else:
                parser_name = lower_body.split("!", 1)[1].split(" ", 1)[0]
                for parser in self.parsers():
                    if parser_name == parser.name():
                        selected_parser = parser
                        body = body.split(" ", 1)[1]
        elif len(self.parsers()) == 1:
            selected_parser = self.parsers()[0]

        if selected_parser is None:
            return None

        try:
            command, args = selected_parser.parse(body)
            return selected_parser, command, args
        except ParseError:
            pass

        return None

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
        with open(self.connection_file_path, "w") as f:
            f.write(self.connection.settings.serialize())
        with open(self.extras_file_path, "w") as f:
            json.dump(self.extras, f)

    @classmethod
    def load(cls, connection_cls: Type[Connection], location: str):
        """
        Generates a Bot from the location.
        :param connection_cls: The class of the connection
        :param location: The location of the bot configuration directory
        :return: The generated bot
        """
        connection_file = os.path.join(location, "connection.json")
        if not os.path.isfile(connection_file):
            raise ConfigurationError("Missing connection settings file")

        with open(connection_file, "r") as f:
            serialized = f.read()

        try:
            connection = connection_cls.from_serialized_settings(serialized)
        except InvalidSettings:
            raise ConfigurationError("Invalid settings for connection")

        return cls(connection, location)

    @classmethod
    def create_config(cls, connection_cls: Type[Connection], path: str):
        """
        Creates a configuration directory for a bot
        :param connection_cls: The connection class for
                               which to generate a config
        :param path: The path of the configuration directory
        :return: None
        """
        if not os.path.isdir(path):
            os.makedirs(path)

        connection_path = os.path.join(path, "connection.json")
        settings = connection_cls.settings_cls().prompt()

        extras_path = os.path.join(path, "extras.json")
        extras = {}

        for arg in cls.extra_config_args():
            while True:
                resp = input("(Extras){}: ".format(arg)).strip()
                if resp != "":
                    extras[arg] = resp
                    break

        with open(connection_path, "w") as f:
            f.write(settings.serialize())
        with open(extras_path, "w") as f:
            json.dump(extras, f)

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

            help_message = "Help message for {}\n\n".format(self.name())

            include_titles = len(self.parsers()) > 1
            for parser in self.parsers():
                help_message += parser.help_text(include_titles) + "\n\n"

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
