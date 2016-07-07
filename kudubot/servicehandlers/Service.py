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
import os
import time
from threading import Thread
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from typing import Dict, List

from kudubot.resources.fonts.__init__ import get_location as get_font
from kudubot.connection.generic.Message import Message
from kudubot.config.LocalConfigChecker import LocalConfigChecker

# Weird import structure due to cyclic dependency
try:
    from kudubot.connection.generic.Connection import Connection
except ImportError:
    Connection = object


class Service(object):
    """
    A structure-defining interface for a Service
    """

    has_background_process = False
    """
    Attribute that tells outer classes if this particular service has a background process
    """

    connection = None
    """
    The connection to use to send messages
    """

    help_description = {"en": "A Generic Service Interface",
                        "de": "Eine Generische Dienstleistungsschnittstelle"}
    """
    A dictionary containing help messages in various languages on the use of the service
    """

    identifier = "Service"
    """
    A unique identifier assigned to the plugin.
    """

    protected = False
    """
    Can be set to true if the service may not be deactivated
    """

    def __init__(self, connection: Connection) -> None:
        """
        Basic Constructor for a Service. It stores the connection as a class variable.

        :param connection: The connection to be used by the service
        :return: None
        """
        self.connection = connection
        self.initialize()

    def initialize(self) -> None:
        """
        Can be used to extend the constructor for extra functionality
        :return:
        """
        pass

    def send_text_message(self, message: Message) -> None:
        """
        Sends a text message using the active connection and also logs it using the logging mechanism

        :param message: the message to be sent
        :return: None
        """
        if not self.connection.muted and len(message.message_body) < 2048:
            self.connection.message_logger.log_message(message)
            self.connection.send_text_message(message)

    def send_text_as_image_message(self, message: Message) -> None:
        """
        Sends a text message, converted into a monospaced image.

        :param message: the message to be sent
        :return: None
        """
        image_file_path = os.path.join(LocalConfigChecker.program_directory, "temp_text_image.png")
        image_text = message.message_body

        self.wait_until_delete(image_file_path, 5)

        padding = (2, 2)
        fontsize = 30
        font_file = get_font("NotCourierSans.otf")
        font = ImageFont.truetype(font_file, fontsize)

        image_size_test = Image.new("RGBA", (0, 0), (255, 255, 255))
        draw_size_test = ImageDraw.Draw(image_size_test)
        width, height = draw_size_test.textsize(image_text, font=font)

        width += 2 * padding[0]
        height += 2 * padding[1]

        image = Image.new("RGBA", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.text(padding, image_text, (0, 0, 0), font=font)

        ImageDraw.Draw(image)
        image.save(image_file_path)

        self.send_image_message(message.address, image_file_path)
        self.delete_file_after(image_file_path, 5)

    def send_image_message(self, receiver: str, message_image: str, caption: str = "") -> None:
        """
        Sends an image to the receiver, with an optional caption/title
        :param receiver: The receiver of the message
        :param message_image: The image to be sent
        :param caption: The caption/title to be displayed along with the image, defaults to an empty string
        :return: None
        """
        # TODO Logging
        self.connection.send_image_message(receiver, message_image, caption)

    def send_audio_message(self, receiver: str, message_audio: str, caption: str = "") -> None:
        """
        Sends an audio file to the receiver, with an optional caption/title
        :param receiver: The receiver of the message
        :param message_audio: The audio file to be sent
        :param caption: The caption/title to be displayed along with the audio, defaults to an empty string
        :return: None
        """
        # TODO Logging
        self.connection.send_audio_message(receiver, message_audio, caption)

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        raise NotImplementedError()

    def background_process(self) -> None:
        """
        A method that should be run in the background if has_background_process is True

        :return: None
        """
        if not self.has_background_process:
            return
        else:
            raise NotImplementedError()

    @staticmethod
    def generate_reply_message(message: Message, title: str, body: str) -> Message:
        """
        Generates a reply message object while re-using the original message and just replacing
        the title and body, while flipping the 'incoming' switch

        :param message: the original message
        :param title: the new title of the message
        :param body: the new body of the message
        :return: the new message object
        """
        return Message(message_body=body, address=message.address, message_title=title, incoming=False,
                       name=message.name, group=message.group, single_address=message.single_address,
                       single_name=message.single_name, timestamp=message.timestamp)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Check if the received message is a valid command for this service

        :param message: the message to be checked
        :return: True if the message is a valid command, False otherwise
        """
        raise NotImplementedError()

    @staticmethod
    def regex_string_from_dictionary_keys(dictionaries: List[Dict[str, str]]) -> str:
        """
        Generates a regex string of form (item1|item2|...|item_n) from dictionary keys
        Multiple dictionaries can be used

        :param dictionaries: the dictionaries containing the keys to be used
        :return: the regex string
        """
        dictionary_keys = []

        for dictionary in dictionaries:
            for key in dictionary:
                dictionary_keys.append(key)

        regex_string = "("
        first = True
        for key in dictionary_keys:
            if first:
                regex_string += key
                first = False
            else:
                regex_string += "|" + key
        regex_string += ")"

        return regex_string

    @staticmethod
    def delete_file_after(file_path: str, after_seconds: int) -> None:
        """
        Deletes a file asynchronuously after a period of time

        :param file_path: the path to the file to delete
        :param after_seconds: after how many seconds should the file be deleted
        :return: None
        """

        def delete_file_and_wait() -> None:
            """
            Deletes the file after the amount of seconds specified

            :return: None
            """
            time.sleep(after_seconds)
            try:
                os.remove(file_path)
            except FileNotFoundError:
                pass

        delete_thread = Thread(target=delete_file_and_wait)
        delete_thread.daemon = True
        delete_thread.start()

    @staticmethod
    def wait_until_delete(file_path: str, time_out: int) -> None:
        """
        Waits until a file is deleted. If it is not deleted within a given time period, manually delete the file

        :param file_path: the file to wait for
        :param time_out: the maximum time period to wait
        :return: None
        """
        sleep_seconds = 0
        while os.path.isfile(file_path):
            time.sleep(1)
            sleep_seconds += 1

            if sleep_seconds >= time_out:
                try:
                    os.remove(file_path)
                except FileNotFoundError:
                    pass
