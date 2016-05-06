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
    along with messengerbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
import re
from typing import Tuple

import irc.bot
import irc.strings
import irc.client
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

from messengerbot.logger.PrintLogger import PrintLogger
from messengerbot.connection.generic.Message import Message
from messengerbot.connection.generic.Connection import Connection
from messengerbot.connection.irc.parsers.IrcConfigParser import IrcConfigParser


class IrcConnection(irc.bot.SingleServerIRCBot, Connection):
    """
    Class that implements the connection to an IRC network
    """

    identifier = "irc"
    """
    A string identifier with which other parts of the program can identify the type of connection
    """

    channel = ""
    """
    The channel this bot listens in on.
    """

    def __init__(self, credentials: Tuple[str, str, str, str]) -> None:
        """
        Constructor for the IRC Connection class that initializes the SingleServerIRC Bot

        :param credentials: The credentials used to log in.
        :return: None
        """
        print(credentials)
        super().__init__([(credentials[1], int(credentials[3]))], credentials[0], credentials[0])
        self.channel = credentials[2]

    # noinspection PyMethodMayBeStatic
    def on_nicknameinuse(self, connection: irc.client.Connection, event: irc.client.Event) -> None:
        """
        Method called when the nickname is already in use. It tries logging in again with the same
        name appended with an underscore

        :param connection: the connection to the IRC server
        :param event: The event that trigered the method call
        :return: None
        """
        str(event)
        connection.nick(connection.get_nickname() + "_")

    def on_welcome(self, connection: irc.client.Connection, event: irc.client.Event) -> None:
        """
        Method called when the bot connects to the IRC server. It then automatically joins the
        specified channel

        :param connection: the connection to the IRC server
        :param event: The event that triggered the method call
        :return: None
        """
        str(event)
        connection.join(self.channel)

    def on_pubmsg(self, connection: irc.client.Connection, event: irc.client.Event) -> None:
        """
        Method called whenever a message from a channel is received. Converts the event into
        a message and calls on_incoming_message with it.

        :param connection:
        :param event:
        :return:
        """
        received_text = event.arguments[0]
        sender_name = event.source.nick
        channel = self.channel

        message = Message(message_body=received_text, message_title="", address=sender_name)
        self.connection.notice(sender_name, "Test")
        #self.on_incoming_message()

    def send_text_message(self, message: Message) -> None:
        """
        Sends a text message to the receiver. Some services allow the use of titles, but some don't,
        so the message title is optional

        :param message: The message to be sent
        :return: None
        """
        pass

    def send_image_message(self, receiver: str, message_image: str, caption: str = "") -> None:
        """
        Sends an image to the receiver, with an optional caption/title

        :param receiver: The receiver of the message
        :param message_image: The image to be sent
        :param caption: The caption/title to be displayed along with the image, defaults to an empty string
        :return: None
        """
        pass

    def send_audio_message(self, receiver: str, message_audio: str, caption: str = "") -> None:
        """
        Sends an audio file to the receiver, with an optional caption/title

        :param receiver: The receiver of the message
        :param message_audio: The audio file to be sent
        :param caption: The caption/title to be displayed along with the audio, defaults to an empty string
        :return: None
        """
        pass

    @staticmethod
    def establish_connection() -> None:
        """
        Establishes the connection to the specific service

        :return: None
        """
        credentials = IrcConfigParser.parse_irc_config(IrcConnection.identifier)

        bot = IrcConnection(credentials)
        bot.start()
