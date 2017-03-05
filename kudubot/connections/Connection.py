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

import os
import sqlite3
from typing import List
from kudubot.services.Service import Service
from kudubot.connections.Message import Message
from kudubot.users.AddressBook import AddressBook


class Connection(object):
    """
    Abstract class that provides a unified model for a chat service connection
    It keeps track of various state variables and provides APIs to send messages
    and start a listener that reacts on incoming messages using the implemented
    service modules
    """

    identifier = "connection"
    """
    A unique identifier that is attributed to the connection. Must be implemented by
    subclasses of the Connection class
    """

    connection_database_file_location = os.path.join(os.path.expanduser("~"), ".kudubot", "data_config")
    """
    The location of the connection's data location
    """

    def __init__(self, services: List[Service]):
        """
        Initializes the connection object using the specified services
        Starts the database connection

        :param services: The services to use with the connection
        """
        self.services = services
        self.connection_database_file_location = os.path.join(self.connection_database_file_location, self.identifier)
        self.db = sqlite3.connect(self.connection_database_file_location)
        self.address_book = AddressBook(self.db)

    def send_message(self, message: Message):
        """
        Sends a Message using the connection

        :param message: The message to send
        :return: None
        """
        raise NotImplementedError()

    def listen(self):
        """
        Starts listening on the connection in an infinite loop. If the execution of the
        program has to continue past starting the listener, the listen_in_separate_thread() method
        should be called instead

        :return: None
        """
        raise NotImplementedError()

    def on_message_received(self, message: Message):
        """
        Specifies how the connection reacts on incoming messages.

        :param message: The message that was received
        :return: None
        """
        raise NotImplementedError()
