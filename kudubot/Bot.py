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
import time
import json
import logging
import traceback
from functools import wraps
from threading import Thread
from sentry_sdk import capture_exception
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker, scoped_session
from bokkichat.exceptions import InvalidSettings
from bokkichat.connection.Connection import Connection
from bokkichat.entities.message.Message import Message
from bokkichat.entities.message.TextMessage import TextMessage
from bokkichat.entities.message.MediaMessage import MediaMessage
from kudubot import version as kudubot_version
from kudubot.db import Base
from kudubot.db.Address import Address as Address
from kudubot.db.config.impl.SqlteConfig import SqliteConfig
from kudubot.exceptions import ConfigurationError, ParseError
from kudubot.parsing.CommandParser import CommandParser
from typing import Type, Optional, List, Tuple, Dict, Any, cast, Callable


class Bot:
    """
    The Bot class offers an abstraction layer above bokkichat
    """

    # noinspection PyMethodParameters
    def auth_required(func: Callable) -> Callable:
        """
        This is a decorator that makes it possible to restrict a user's access
        to certain commands.
        To use this, simply decorate an 'on_'-method with this decorator.
        The method will then only be called if the is_authorized() method
        returns True
        :return: None
        """
        @wraps(func)
        def wrapper(
                self: Bot,
                sender: Address,
                args: Dict[str, Any],
                db_session: Session
        ):
            if not self.is_authorized(sender, args, db_session):
                self.send_txt(
                    sender,
                    self.unauthorized_message(),
                    "Unauthorized"
                )
            else:
                func(self, sender, args, db_session)
        return wrapper

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
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        log_file_handler.setFormatter(formatter)
        self.logger.addHandler(log_file_handler)
        self.connection.logger.addHandler(log_file_handler)
        self.logger.setLevel(logging.DEBUG)
        self.connection.logger.setLevel(logging.DEBUG)

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

        self.sessionmaker = scoped_session(sessionmaker(bind=self.db_engine))

        self.bg_thread = Thread(target=self.run_in_bg, daemon=True)
        self.init()

    def init(self):
        """
        Additional init method that gets called at the end of __init__
        :return: None
        """
        pass

    def send_txt(
            self,
            receiver: Address,
            body: str,
            title: Optional[str] = ""
    ):
        """
        Convenience function that allows easier sending of text messages
        :param receiver: The receiver of the text message
        :param body: The body of the text message
        :param title: The (optional) title of the message
        :return: None
        """
        self.connection.send(
            TextMessage(
                self.connection.address,
                receiver,
                body,
                title
            )
        )

    def on_msg(self, message: Message):
        """
        The callback method is called for every received message.
        This method automatically delegates message handling to the
        on_text and on_media methods.
        This also creates a database session for those methods to use
        that will avoid threading issues.
        :param message: The received message
        :return: None
        """
        if not self.pre_callback(message):
            return

        try:
            db_session = self.sessionmaker()
            sender = db_session.query(Address)\
                .filter_by(address=message.sender.address).first()

            if message.is_text():
                message = cast(TextMessage, message)  # type: TextMessage

                parsed = self.parse(message)
                if parsed is None:
                    self.on_text(message, sender, db_session)
                else:
                    parser, command, args = parsed
                    self.on_command(
                        parser,
                        command,
                        args,
                        sender,
                        db_session
                    )

            elif message.is_media():
                message = cast(MediaMessage, message)  # type: MediaMessage

                self.on_media(message, sender, db_session)
            else:
                pass
        except Exception as e:
            self.logger.error(
                "Exception during Message: {}\n{}".format(
                    e,
                    "\n".join(traceback.format_tb(e.__traceback__))
                )
            )
            capture_exception(e)
        finally:
            self.sessionmaker.remove()

    def on_text(
            self,
            message: TextMessage,
            sender: Address,
            db_session: Session
    ):
        """
        Handles text messages that aren't commands. Those are by default simply
        ignored.
        :param message: The received message
        :param sender: The database Address object of the sender
        :param db_session: A valid database session
        :return: None
        """
        pass

    def on_media(
            self,
            message: MediaMessage,
            sender: Address,
            db_session: Session
    ):
        """
        Handles media messages. Those are by default simply ignored.
        :param message: The received message
        :param sender: The database Address object of the sender
        :param db_session: A valid database session
        :return: None
        """
        pass

    # noinspection PyUnusedLocal
    def on_command(
            self,
            parser: CommandParser,
            command: str,
            args: Dict[str, Any],
            sender: Address,
            db_session: Session
    ):
        """
        Handles text messages that have been parsed as commands.
        Automatically searches for 'on_X' methods in the bot and
        forwards the parameters to those methods if they exist.
        This mechanism can be used for simple bots that don't need more logic
        than a simple if "command" elif "other_command"... .
        :param parser: The parser containing the command
        :param command: The command name
        :param args: The arguments of the command
        :param sender: The database address of the sender
        :param db_session: A valid database session
        :return: None
        """
        for prefix in ["on_", "_on_", "handle_", "_handle_"]:
            try:
                method = getattr(self, prefix + command)
                method(sender, args, db_session)
                return
            except AttributeError:
                pass
        self.logger.warning("No method for command " + command)

    @classmethod
    def name(cls) -> str:
        """
        :return: The name of the bot
        """
        raise NotImplementedError()

    @classmethod
    def version(cls) -> str:
        """
        :return: The current version of the bot
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

    @property
    def bg_pause(self) -> int:
        """
        The pause between background iterations
        :return: The pause in seconds
        """
        return 60

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def is_authorized(
            self,
            address: Address,
            args: Dict[str, Any],
            db_session: Session
    ) -> bool:
        """
        Checks if a user is authorized
        :param address: The user to check
        :param args: possible command arguments
        :param db_session: The database session to use
        :return: True if authorized, False otherwise
        """
        return True

    @classmethod
    def unauthorized_message(cls) -> str:
        """
        :return: A custom message sent to a user if they tried to access
                 a feature that requires authorization without being
                 authorized
        """
        return "Unauthorized"

    def run_in_bg(self):
        """
        Method that is started when the bot is started.
        This executes the bg_iteration method every bg_pause seconds
        :return: None
        """
        self.logger.info("Starting background thread")
        counter = 0
        while True:
            self.logger.debug("Starting background iteration " + str(counter))
            try:
                db_session = self.sessionmaker()
                self.bg_iteration(counter, db_session)
            except BaseException as e:
                self.logger.error(
                    "Exception in background thread: {}\n{}".format(
                        e,
                        "\n".join(traceback.format_tb(e.__traceback__))
                    )
                )
                capture_exception(e)
            finally:
                self.sessionmaker.remove()
                counter += 1
                time.sleep(self.bg_pause)

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def bg_iteration(self, iteration: int, db_session: Session):
        """
        Executes a background iteration. By default this does nothing.
        This is supposed to be overriden by child classes to implement
        background functionality
        :param iteration: The iteration count. Useful for differentiating
                          between actions that have different repetition rates
        :param db_session: The database session to use
        :return:
        """
        pass

    def pre_callback(self, message: Message) -> bool:
        """
        Prepares the callback and decides whether or not the callback
        is even executed
        :param message: The message to check
        :return: True if the execution continues, False otherwise
        """
        _continue = True
        _continue = _continue and self._store_in_address_book(message)

        if message.is_text():
            message = cast(TextMessage, message)  # type: TextMessage
            _continue = _continue and self._handle_help_command(message)
            _continue = _continue and self._handle_ping(message)

        return _continue

    def start(self):
        """
        Starts the bot using the implemented callback function
        :return: None
        """
        self.logger.info("Starting Bot")

        def loop_callback(_: Connection, message: Message):
            self.logger.info("Received message {}".format(message))
            self.on_msg(message)

        self.bg_thread.start()

        try:
            self.connection.loop(callback=loop_callback)
        except ConfigurationError as e:
            print("Invalid Coniguration Detected")
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
        db_session = self.sessionmaker()
        exists = db_session.query(Address) \
            .filter_by(address=message.sender.address).first()

        if exists is None:
            entry = Address(address=message.sender.address)
            db_session.add(entry)
            db_session.commit()
        return True

    def _handle_help_command(self, message: TextMessage) -> bool:
        """
        Handles the /help command.
        :param message: The message to check for a /help command
        :return: Whether or not handling the message should continue
        """
        if message.body.lower().strip() in ["/help", "/start"]:

            help_message = "Help message for:\n{} V{}\n(kudubot V{})\n\n"\
                .format(self.name(), self.version(), kudubot_version)

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

    def _handle_ping(self, message: TextMessage) -> bool:
        """
        Handles PING messages
        :param message: The message to analyze
        :return: Whether or not handling the message should continue
        """
        if message.body.lower().strip() == "ping":
            self.send_txt(message.sender, "Pong", "Pong")
            if not self.bg_thread.is_alive():
                self.send_txt(message.sender, "BG Thread is dead", "BG Thread")
            return False
        elif message.body.lower().strip() == "bg_ping":
            reply = "👍" if self.bg_thread.is_alive() else "👎"
            self.send_txt(message.sender, reply, "Pong")
            return False
        else:
            return True
