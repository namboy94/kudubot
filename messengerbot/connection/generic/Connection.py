# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via online chat services.

    messengerbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    messengerbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
from typing import Tuple

from messengerbot.servicehandlers.ServiceManager import ServiceManager
from messengerbot.connection.generic.Message import Message


class Connection(object):
    """
    Class that defines common interface elements to handle the connection to the various
    messenger services
    """

    identifier = "generic"
    """
    A string identifier with which other parts of the program can identify the type of connection
    """

    service_manager = None
    """
    An object that handles all active message services of the messenger bot
    """

    def send_text_message(self, message: Message) -> None:
        """
        Sends a text message to the receiver.
        :param message: The message entity to be sent
        :return: None
        """
        raise NotImplementedError()

    def send_image_message(self, receiver: str, message_image: str, caption: str = "") -> None:
        """
        Sends an image to the receiver, with an optional caption/title
        :param receiver: The receiver of the message
        :param message_image: The image to be sent
        :param caption: The caption/title to be displayed along with the image, defaults to an empty string
        :return: None
        """
        raise NotImplementedError()

    def send_audio_message(self, receiver: str, message_audio: str, caption: str = "") -> None:
        """
        Sends an audio file to the receiver, with an optional caption/title
        :param receiver: The receiver of the message
        :param message_audio: The audio file to be sent
        :param caption: The caption/title to be displayed along with the audio, defaults to an empty string
        :return: None
        """
        raise NotImplementedError()

    def on_incoming_message(self, message: Message) -> None:
        """
        Message called whenever a message is received

        :param message: The received message object
        :return: None
        """
        # Create a ServiceManager object if there is None before this
        if self.service_manager is None:
            self.service_manager = ServiceManager(self)
        # Process the message
        self.service_manager.process_message(message)

    def establish_connection(self, credentials: Tuple) -> None:
        """
        Establishes the connection to the specific service

        :param credentials: Credentials used to establish the connection
        :return: None
        """
        raise NotImplementedError()
