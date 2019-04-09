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
import sqlite3
from typing import Callable, Type
from bokkichat.connection.Connection import Connection
from bokkichat.message.Message import Message


class Bot:
    """
    The Bot class automatically
    """

    def __init__(self, connection: Connection, location: str):
        """
        Initializes the bot
        :param connection: The connection the bot should use
        :param location: The location of config and DB files
        """
        self.connection = connection
        self.location = location
        if not os.path.isdir(location):
            os.makedirs(location)

        self.settings_file_path = os.path.join(location, "settings.json")
        self.db_path = os.path.join(location, "data.db")
        self.db = self.db_connect()

    def start(self, callback: Callable[[object, Connection, Message], None]):
        """
        Starts the bot using a callback function
        :param callback: The callback function to use.
                         Gets the following arguments:
                            - Bot
                            - Connection
                            - Message
        :return: None
        """
        def loop_callback(connection: Connection, message: Message):
            if self.pre_callback(connection, message):
                callback(self, connection, message)

        self.connection.loop(callback=loop_callback)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def pre_callback(self, connection: Connection, message: Message) -> bool:
        """
        Prepares the callback and decides whether or not the callback
        is even executed
        :param connection: The connection to use
        :param message: The message to check
        :return: True if the execution continues, False otherwise
        """
        # TODO do stuff
        return True

    def db_connect(self) -> sqlite3.Connection:
        """
        Creates a new database connection
        :return: The database connection
        """
        return sqlite3.connect(self.db_path)

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
        with open(os.path.join(location, "settings.json"), "r") as f:
            serialized = f.read()
        connection = connection_cls.from_serialized_settings(serialized)
        return cls(connection, location)
