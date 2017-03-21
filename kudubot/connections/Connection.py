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
from threading import Thread
from typing import List, Dict
from kudubot.users.Contact import Contact
from kudubot.connections.Message import Message
from kudubot.users.AddressBook import AddressBook
from kudubot.config.GlobalConfigHandler import GlobalConfigHandler


class Connection(object):
    """
    Abstract class that provides a unified model for a chat service connection
    It keeps track of various state variables and provides APIs to send messages
    and start a listener that reacts on incoming messages using the implemented
    service modules
    """

    identifier = "connection"
    """
    A unique identifier that is attributed to the connection. Must be overridden by
    subclasses of the Connection class
    """

    database_file_location = GlobalConfigHandler.data_location
    """
    The location of the connection's data location. Has to be adjusted by the __init__ method to point to the
    correct database file for the connection's data
    """

    config_file_location = GlobalConfigHandler.specific_connection_config_location
    """
    The location of the connection's configuration file
    """

    def __init__(self, services: List[type]):
        """
        Initializes the connection object using the specified services
        Starts the database connection

        :param services: The services to use with the connection
        """
        self.services = []
        for service in services:
            self.services.append(service(self))

        self.database_file_location = os.path.join(self.database_file_location, self.identifier + ".db")
        self.config_file_location = os.path.join(self.config_file_location, self.identifier + ".conf")
        self.db = sqlite3.connect(self.database_file_location)
        self.address_book = AddressBook(self.db)

        self.config = self.load_config()
        self.user_contact = self.define_user_contact()

    def apply_services(self, message: Message, break_on_match: bool = False):
        """
        Applies the services to a Message
        First, the method checks if a service is applicable to a message.
        Then, if it is applicable, the service will process the message
        If the break_on_match parameter is set to True, the first match will
        always end the loop.

        :param message: The message to process
        :param break_on_match: Can be set to True to not allow more than one result
        :return: None
        """

        for service in self.services:
            if service.is_applicable_to(message):
                service.handle_message(message)
                if break_on_match:
                    break

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

    def send_audio_message(self, receiver: Contact, audio_file: str, caption: str = ""):
        """
        Sends an audio message using the connection

        :param receiver: The receiver of the message
        :param audio_file: The path to the audio file to send
        :param caption: The caption sent together with the message
        :return: None
        """
        raise NotImplementedError()

    def send_video_message(self, receiver: Contact, video_file: str, caption: str = ""):
        """
        Sends a video message using the connection

        :param receiver: The recipient of the video message
        :param video_file: The path to the video file to be sent
        :param caption: The caption to be displayed with the video
        :return: None
        """
        raise NotImplementedError()

    def send_image_message(self, receiver: Contact, image_file: str, caption: str = ""):
        """
        Sends an image message using the connection

        :param receiver: The recipient of the image message
        :param image_file: The path to the image file
        :param caption: The caption to be displayed with the image
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

    def listen_in_separate_thread(self) -> Thread:
        """
        Runs the listen() method in a separate daemon thread

        :return: The listening thread
        """
        thread = Thread(target=self.listen)
        thread.daemon = True
        thread.start()
        return thread
