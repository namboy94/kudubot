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

import time
import telegram
import configparser
from typing import Dict, List
from kudubot.users.Contact import Contact
from kudubot.entities.Message import Message
from kudubot.connections.Connection import Connection
from kudubot.exceptions import InvalidConfigException
from kudubot.config.GlobalConfigHandler import GlobalConfigHandler


class TelegramConnection(Connection):
    """
    A Connection class that connects to Telegram
    """

    @staticmethod
    def define_identifier() -> str:
        """
        Defines the Connection's unique identifier

        :return: The Connection's identifier
        """
        return "telegram"

    def __init__(self, services: List[type],
                 config_handler: GlobalConfigHandler):
        """
        Initializes the Telegram Connection.
        Additionally to the standard Connection, a telegram.Bot object is
        generated to interface with the Telegram API

        :param services: The services to include
        :param config_handler: The GlobalConfigHandler that determines
                               the location of the configuration files
        """
        super().__init__(services, config_handler)
        self.bot = telegram.Bot(self.config["api_key"])

    def load_config(self) -> Dict[str, object]:
        """
        Loads the configuration file for the Telegram Connection
        A Telegram Connection requires only an api_key attribute in the
        [credentials] section of the config file

        Any configuration errors are raised as new InvalidConfigExceptions

        :return: The configuration, as a dictionary
        """

        try:

            self.logger.info("Parsing config at " + self.config_file_location)

            config = configparser.ConfigParser()
            config.read(self.config_file_location)
            parsed_config = dict(config.items("credentials"))

            if parsed_config["api_key"] == "":
                self.logger.warning(
                    "Config Parsing Failed. Empty API Key supplied.")
                raise InvalidConfigException(
                    "Invalid Telegram Configuration File - "
                    "Empty API key detected")

            self.logger.info("Config successfully loaded")

            return parsed_config

        except (configparser.NoSectionError,
                configparser.MissingSectionHeaderError):
            self.logger.warning("Config Parsing Failed. "
                                "No credentials section in config file.")
            raise InvalidConfigException("Invalid Telegram Configuration File "
                                         "- No credentials section")
        except KeyError as e:
            self.logger.warning("Config Parsing Failed. No attribute " +
                                str(e) + " found.")
            raise InvalidConfigException(
                "Invalid Telegram Configuration File - No '" + str(e) +
                "' attribute found")

    def generate_configuration(self):
        """
        Generates a new Configuration file for the Telegram Connection

        :return: None
        """
        with open(self.config_file_location, 'w') as config:
            config.write("[credentials]\napi_key=YourKeyHere\n")
            self.logger.info("Wrote new Configuration file at " +
                             self.config_file_location)

    def define_user_contact(self) -> Contact:
        """
        :return: The Telegram connection's contact information
        """
        return Contact(-1, "Kudubot", self.config["api_key"])

    def send_message(self, message: Message):
        """
        Sends a message using the Telegram connection

        :param message: The message to send
        :return: None
        """
        self.logger.info("Sending text Message to " +
                         message.receiver.display_name)
        self.bot.send_message(
            chat_id=message.receiver.address, text=message.message_body
        )

    def send_image_message(self, receiver: Contact, image_file: str,
                           caption: str = ""):
        """
        Sends an Image Message via Telegram

        :param receiver: The recipient of the message
        :param image_file: The image file to send
        :param caption: The caption to be displayed with the image
        :return:
        """

        with open(image_file, 'rb') as image_data:
            self.logger.info("Sending Image File to " + receiver.display_name)
            self.bot.send_photo(
                chat_id=receiver.address, photo=image_data, caption=caption)

    def send_audio_message(self, receiver: Contact, audio_file: str,
                           caption: str = ""):
        """
        Sends an Audio Message via Telegram

        :param receiver: The recipient of the message
        :param audio_file: The audio file to send
        :param caption: The caption to display together with the audio
        :return:
        """
        with open(audio_file, 'rb') as audio_data:
            self.logger.info("Sending Audio File to " + receiver.display_name)
            self.bot.send_audio(
                chat_id=receiver.address, audio=audio_data, caption=caption)

    def send_video_message(self, receiver: Contact, video_file: str,
                           caption: str = ""):
        """
        Sends a video message via Telegram

        :param receiver: The recipient of the message
        :param video_file: The video file to send
        :param caption: The caption to be displayed together with the video
        :return:
        """
        with open(video_file, 'rb') as video_data:
            self.bot.send_video(
                chat_id=receiver.address, video=video_data, caption=caption)

    def listen(self):
        """
        Listens to new Telegram messages
        Starts an infinite loop that polls for new messages every second,
        and applies the Connection's Services to these received messages.

        :return: None
        """

        try:
            update_id = self.bot.get_updates()[0].update_id
        except IndexError:
            update_id = 0

        while True:

            try:

                for update in self.bot.get_updates(
                        offset=update_id, timeout=10
                ):

                    update_id = update.update_id + 1

                    telegram_message = update.message.to_dict()
                    chat = telegram_message['chat']
                    _from = telegram_message['from']

                    name = _from["username"] \
                        if _from["username"] != "" \
                        else _from["first_name"] + _from["last_name"]

                    if chat['type'] == "group":
                        sender = self.address_book.add_or_update_contact(
                            Contact(-1, name, _from['id'])
                        )
                        group = self.address_book.add_or_update_contact(
                            Contact(-1, chat['title'], str(chat['id']))
                        )
                    else:
                        sender = self.address_book.add_or_update_contact(
                            Contact(-1, name, str(chat['id']))
                        )
                        group = None

                    message = Message(
                        "", telegram_message['text'],
                        self.user_contact, sender, group,
                        telegram_message['date']
                    )
                    self.logger.info(
                        "received message '" + message.message_body +
                        "' from " + message.sender.display_name)
                    self.apply_services(message)

                time.sleep(1)

            except telegram.error.Unauthorized:
                # The self.bot.get_update method may cause an
                # Unauthorized Error if the bot is blocked by the user
                update_id += 1

            except telegram.error.TimedOut:
                pass
