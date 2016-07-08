# coding=utf-8
"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of kudubot.

    kudubot makes use of various third-party python modules to serve
    information via online chat services.

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

# imports
import re
import traceback

from yowsup.layers.interface import YowInterfaceLayer
from yowsup.layers.interface import ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity

from kudubot.logger.PrintLogger import PrintLogger
from kudubot.connection.generic.Message import Message
from kudubot.logger.ExceptionLogger import ExceptionLogger
from kudubot.connection.generic.Connection import Connection
from kudubot.connection.whatsapp.layers.YowsupEchoLayer import YowsupEchoLayer
from kudubot.connection.whatsapp.stacks.YowsupEchoStack import YowsupEchoStack
from kudubot.connection.whatsapp.parsers.WhatsappConfigParser import WhatsappConfigParser


class WhatsappConnection(YowsupEchoLayer, Connection):
    """
    Class that implements the connection to the Whatsapp Messaging service
    """

    identifier = "whatsapp"
    """
    A string identifier with which other parts of the program can identify the type of connection
    """

    def __init__(self) -> None:
        """
        Constructor for the WhatsappConnection class that initializes the Yowsup layer

        :return: None
        """
        super().__init__()
        # noinspection PyCallByClass
        YowInterfaceLayer.__init__(self)
        self.initialize()

    def send_text_message(self, message: Message) -> None:
        """
        Sends a text message to the receiver. Some services allow the use of titles, but some don't,
        so the message title is optional

        :param message: The message to be sent
        :return: None
        """
        message_protocol_entity = self.convert_message_to_text_message_protocol_entity(message)
        self.toLower(message_protocol_entity)

    def send_image_message(self, receiver: str, message_image: str, caption: str = "") -> None:
        """
        Sends an image to the receiver, with an optional caption/title

        :param receiver: The receiver of the message
        :param message_image: The image to be sent
        :param caption: The caption/title to be displayed along with the image, defaults to an empty string
        :return: None
        """
        self.send_image(receiver, message_image, caption)

    def send_audio_message(self, receiver: str, message_audio: str, caption: str = "") -> None:
        """
        Sends an audio file to the receiver, with an optional caption/title

        :param receiver: The receiver of the message
        :param message_audio: The audio file to be sent
        :param caption: The caption/title to be displayed along with the audio, defaults to an empty string
        :return: None
        """
        str(caption)
        self.send_audio(receiver, message_audio)

    @staticmethod
    def establish_connection() -> None:
        """
        Establishes the connection to the specific service

        :return: None
        """
        credentials = WhatsappConfigParser.parse_whatsapp_config(WhatsappConnection.identifier)

        while True:
            try:
                PrintLogger.print("Starting Whatsapp Connection", 1)
                echo_stack = YowsupEchoStack(WhatsappConnection, credentials)
                echo_stack.start()
            except Exception as e:
                stack_trace = traceback.format_exc()
                ExceptionLogger.log_exception(e, stack_trace, "whatsapp")

    @ProtocolEntityCallback("message")
    def on_message(self, message_protocol_entity: TextMessageProtocolEntity):
        """
        Method run when a message is received
        :param message_protocol_entity: the message received
        :return: void
        """
        # Wrap the message protocol entity in a PEP8-compliant Wrapper
        if message_protocol_entity.getType() == "text":
            message = self.convert_text_message_protocol_entity_to_message(message_protocol_entity)
            self.on_incoming_message(message)

    @staticmethod
    def convert_text_message_protocol_entity_to_message(message_protocol_entity: TextMessageProtocolEntity) -> Message:
        """
        Converts an incoming text message protocol entity into a Message object

        :param message_protocol_entity: The entity to convert
        :return: the converted message
        """
        body = message_protocol_entity.getBody()

        sender_number = message_protocol_entity.getFrom(True)
        group_identifier = message_protocol_entity.getFrom(False)
        sender_name = message_protocol_entity.getNotify()
        group = False
        individual_number = ""
        individual_name = ""

        timestamp = float(message_protocol_entity.getTimestamp())

        if re.search(r"[0-9]+-[0-9]+", group_identifier):
            group = True
            individual_number = message_protocol_entity.getParticipant(True)
            individual_name = message_protocol_entity.getNotify()

        return Message(message_body=body, message_title="", address=sender_number, incoming=True, name=sender_name,
                       single_address=individual_number, single_name=individual_name, group=group, timestamp=timestamp)

    @staticmethod
    def convert_message_to_text_message_protocol_entity(message: Message) -> TextMessageProtocolEntity:
        """
        Converts an outgoing message object into a text message protocol entity

        :param message: The message to be converted
        :return: The converted text message protocol entity
        """
        to = message.address
        body = message.message_body

        return TextMessageProtocolEntity(body, to=to)
