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
from typing import List, Dict
from kudubot.users.Contact import Contact
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

    connection_database_file_location = os.path.join(os.path.expanduser("~"), ".kudubot", "data")
    """
    The location of the connection's data location. Has to be adjusted by the __init__ method to point to the
    correct database file for the connection's data
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

        self.config = self.load_config()
        self.user_contact = self.define_user_contact()

    def load_config(self) -> Dict[str, object]:
        """
        Loads the configuration for the connection. If this fails for some reason, an InvalidConfigException
        is raised

        :return: A dictionary containing the configuration
        """
        raise NotImplementedError()

    def generate_configuration(self):
        """
        Generates a new configuration file for this connection.

        :return: None
        """
        raise NotImplementedError()

    def define_user_contact(self) -> Contact:
        """
        Creates a Contact object for the connection by which the connection itself is identified

        :return: The connection's user object
        """
        raise NotImplementedError()

    def send_message(self, message: Message):
        """
        Sends a Message using the connection

        :param message: The message to send
        :return: None
        """
        raise NotImplementedError()

    def send_audio_message(self, receiver: Contact, caption: str, audio_file: str):
        """
        Sends an audio message using the connection

        :param receiver: The receiver of the message
        :param caption: The caption sent together with the message
        :param audio_file: The path to the audio file to send
        :return: None
        """
        raise NotImplementedError()

    def send_video_message(self, receiver: Contact, caption: str, video_file: str):
        """
        Sends a video message using the connection

        :param receiver: The recipient of the video message
        :param caption: The caption to be displayed with the video
        :param video_file: The path to the video file to be sent
        :return: None
        """
        raise NotImplementedError()

    def send_image_message(self, receiver: Contact, caption: str, image_file: str):
        """
        Sends an image message using the connection

        :param receiver: The recipient of the image message
        :param caption: The caption to be displayed with the image
        :param image_file: The path to the image file
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
