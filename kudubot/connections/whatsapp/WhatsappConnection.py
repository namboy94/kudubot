"""
Copyright 2015-2017 Hermann Krumrey

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
"""

import configparser
from typing import Dict, List
from yowsup.layers import YowLayerEvent
from yowsup.stacks import YowStackBuilder
from kudubot.users.Contact import Contact
from kudubot.entities.Message import Message
from yowsup.layers.network import YowNetworkLayer
from kudubot.connections.Connection import Connection
from kudubot.exceptions import InvalidConfigException
from kudubot.connections.whatsapp.EchoLayer import EchoLayer
from kudubot.config.GlobalConfigHandler import GlobalConfigHandler


class WhatsappConnection(Connection):
    """
    Class that implements a kudubot connection for
    the Whatsapp Messaging Service
    """

    def __init__(self, services: List[type],
                 config_handler: GlobalConfigHandler):
        """
        Extends the default Connection constructor to create a yowsup stack

        :param services: The services to start
        :param config_handler: The GlobalConfigHandler that determines the
                               location of the configuration files
        """
        super().__init__(services, config_handler)

        stack_builder = YowStackBuilder()
        self.yowsup = EchoLayer(self)
        self.stack = \
            stack_builder.pushDefaultLayers(True).push(self.yowsup).build()
        self.stack.setCredentials((self.config["number"], self.config["pass"]))

    @staticmethod
    def define_identifier() -> str:
        """
        Defines a unique identifier for the connection

        :return: 'whatsapp'
        """
        return "whatsapp"

    def define_user_contact(self) -> Contact:
        """
        :return: The Whatsapp connection's contact information
        """
        return Contact(-1, "Kudubot", self.config["number"])

    def generate_configuration(self):
        """
        Generates a new Configuration file for the Whatsapp Connection

        :return: None
        """
        with open(self.config_file_location, 'w') as config:
            config.write(
                "[credentials]\nnumber=YourNumberHere\npass=YourPassHere\n")
            self.logger.info(
                "Wrote new Configuration file at " + self.config_file_location)

    def load_config(self) -> Dict[str, str]:
        """
        Loads the configuration for the Whatsapp Connection
        from the config file

        :return: The parsed configuration,
                 consisting of a dictionary with a number and pass key
        """
        try:

            self.logger.info("Parsing config at " + self.config_file_location)

            config = configparser.ConfigParser()
            config.read(self.config_file_location)
            parsed_config = dict(config.items("credentials"))

            if parsed_config["number"] == "":
                self.logger.warning(
                    "Config Parsing Failed. No number supplied.")
                raise InvalidConfigException(
                    "Invalid Whatsapp Configuration File - "
                    "Missing number detected")
            elif parsed_config["pass"] == "":
                self.logger.warning(
                    "Config Parsing Failed. No password supplied.")
                raise InvalidConfigException(
                    "Invalid Whatsapp Configuration File - "
                    "Missing password detected")

            self.logger.info("Config successfully loaded")

            return parsed_config

        except (configparser.NoSectionError,
                configparser.MissingSectionHeaderError):

            self.logger.warning("Config Parsing Failed. "
                                "No credentials section in config file.")
            raise InvalidConfigException("Invalid Whatsapp Configuration File "
                                         "- No credentials section")
        except KeyError as e:
            self.logger.warning(
                "Config Parsing Failed. No attribute " + str(e) + " found.")
            raise InvalidConfigException(
                "Invalid Whatsapp Configuration File - No '" + str(e) +
                "' attribute found")

    def send_message(self, message: Message):
        """
        Sends a Text message using the Whatsapp Connection

        :param message: The message to send
        :return: None
        """
        self.yowsup.send_text_message(
            message.message_body, message.receiver.address)

    def send_audio_message(self, receiver: Contact, audio_file: str,
                           caption: str = ""):
        """
        Sends an audio message using the Whatsapp Connection

        :param receiver: The receiver of the audio message
        :param audio_file: The audio file to send
        :param caption: An optional caption for the audio message
        :return: None
        """
        self.yowsup.send_audio_message(audio_file, receiver.address, caption)

    def send_video_message(self, receiver: Contact, video_file: str,
                           caption: str = ""):
        """
        Sends a video message using the Whatsapp Connection

        :param receiver: The receiver of the video message
        :param video_file: The video file to send
        :param caption: An optional caption for the video message
        :return: None
        """
        self.yowsup.send_video_message(video_file, receiver.address, caption)

    def send_image_message(self, receiver: Contact, image_file: str,
                           caption: str = ""):
        """
        Sends an image message using the Whatsapp Connection

        :param receiver: The receiver of the image message
        :param image_file: The image file to send
        :param caption: An optional caption for the image message
        :return: None
        """
        self.yowsup.send_image_message(image_file, receiver.address, caption)

    def listen(self):
        """
        Starts the Yowsup listener

        :return: None
        """
        self.stack.broadcastEvent(
            YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT)
        )
        self.stack.loop()
