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

from yowsup.layers.interface import YowInterfaceLayer
from yowsup.layers.interface import ProtocolEntityCallback

from messengerbot.connection.generic.Connection import Connection
from messengerbot.connection.whatsapp.yowsupwrapper.WrappedYowInterfaceLayer import WrappedYowInterfaceLayer
from messengerbot.connection.whatsapp.layers.YowsupEchoLayer import YowsupEchoLayer
from messengerbot.connection.whatsapp.stacks.YowsupEchoStack import YowsupEchoStack


class WhatsappConnection(WrappedYowInterfaceLayer, YowsupEchoLayer, Connection):
    """
    Class that implements the connection to the Whatsapp Messaging service
    """

    def __init__(self, static: bool = False) -> None:
        """
        Constructor for the WhatsappConnection class, with an option to only be initialized to
        establish a new connection

        :param static: Flag that defines if the created object is only used for 'static'
                        methods (i.e. the connect() method)
        :return: None
        """
        # Don't do anything if in static mode
        if static:
            return
        else:
            super().__init__()
            YowInterfaceLayer.__init__(self)

    def send_text_message(self, receiver: str, message_body: str, message_title: str = "") -> None:
        """
        Sends a text message to the receiver. Some services allow the use of titles, but some don't,
        so the message title is optional
        :param receiver: The receiver of the message
        :param message_body: The main message to be sent
        :param message_title: The title of the message, defaults to an empty string
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

    def establish_connection(self, credentials: Tuple[str]) -> None:
        """
        Establishes the connection to the specific service

        :return: None
        """
        echo_stack = YowsupEchoStack(WhatsappConnection, credentials)
        echo_stack.start()

    @ProtocolEntityCallback("message")
    def on_message(self, message_protocol_entity):
        """
        Method run when a message is received
        :param message_protocol_entity: the message received
        :return: void
        """
        self.on_incoming_message()