"""
LICENSE:
Copyright 2017 Hermann Krumrey

This file is part of kudubot-cli.

    kudubot-cli is an extension module for kudubot. It provides
    a Connection that can be used to test new modules more easily.

    kudubot-cli is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    kudubot-cli is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with kudubot-cli.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

import logging
from typing import Dict

from kudubot.connections.Connection import Connection
from kudubot.entities.Message import Message
from kudubot.users.Contact import Contact


class CliConnection(Connection):
    """
    The CLI kudubot connection class.
    """

    @staticmethod
    def define_identifier() -> str:
        """
        Defines the identifier for this Connection

        :return: None
        """
        return "cli"

    logger = logging.getLogger("kudubot_cli.CliConnection")

    def send_video_message(self, receiver: Contact, video_file: str, caption: str = ""):
        """
        Sending videos is not supported in the CLI

        :param receiver: The message's recipient
        :param video_file: The video file to send
        :param caption: The caption to send
        :return: None
        """
        self.logger.debug("Video messages are not supported")

    def send_audio_message(self, receiver: Contact, audio_file: str, caption: str = ""):
        """
        Sending audio files is not supported in the CLI
        :param receiver: The recipient of the file
        :param audio_file: The audio file to send
        :param caption: the caption to send
        :return: None
        """
        self.logger.debug("Audio messages are not supported")

    def send_image_message(self, receiver: Contact, image_file: str, caption: str = ""):
        """
        Sending image files is not supported in the CLI

        :param receiver: The recipient
        :param image_file: The image file to send
        :param caption: The caption to use
        :return: None
        """
        self.logger.debug("Image messages are not supported")

    def define_user_contact(self) -> Contact:
        """
        Specifies the User Contact, which is of no importance for the CLI Connection

        :return: The CLI's user Contact
        """
        return Contact(-1, "Cli", "Cli")

    def load_config(self) -> Dict[str, object]:
        """
        The CLI Connection does not require any configuration

        :return: {}
        """
        self.logger.debug("No configuration required")
        return {}

    def generate_configuration(self):
        """
        The CLI Connection does not require any configuration

        :return: None
        """
        self.logger.debug("No configuration required")

    def send_message(self, message: Message):
        """
        Prints the message to the console

        :param message: The message to 'send'
        :return: None
        """
        print("\033[93m" + message.message_body + "\033[0m")

    def listen(self):
        """
        Starts an endless loop that continuously prompts the user for input

        :return: None
        """
        while True:
            self.apply_services(Message("", input(), self.user_contact, self.user_contact))
