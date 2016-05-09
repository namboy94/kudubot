# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via the online chat services.

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
import os
import re
import urllib.request
import urllib.error

from messengerbot.servicehandlers.Service import Service
from messengerbot.connection.generic.Message import Message
from messengerbot.config.LocalConfigChecker import LocalConfigChecker


class ImageSenderService(Service):
    """
    The ImageSenderService Class that extends the generic Service class.
    The service downloads an image from a specified URL and then sends
    it via the selected service.
    """

    identifier = "image_sender"
    """
    The identifier for this service
    """

    help_description = {"en": "/img\tSends images from an URL\n"
                              "syntax: /img <url>",
                        "de": "/img\tVerschickt Bilder von URLs\n"
                              "syntax: /img <url>"}
    """
    Help description for this service.
    """

    image_download_error = {"en": "Error Downloading image",
                            "de": "Fehler beim herunterladen der Bilddatei"}
    """
    Message sent when the service failed to download an image
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        link = message.message_body.split("/img ")[1]
        image_name = link.rsplit("/", 1)[1]

        # Download file via http url
        try:
            local_file = os.path.join(LocalConfigChecker.program_directory, image_name)
            urllib.request.urlretrieve(link, local_file)
            self.send_image_message(message.address, local_file, image_name)
            os.remove(local_file)

        except (urllib.error.HTTPError, urllib.error.URLError):
            reply = self.image_download_error[self.connection.last_used_language]
            reply_message = self.generate_reply_message(message, "Image Sender", reply)
            self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        return re.search(r"^/img (http(s)?://|www.)[^;>\| ]+(.png|.jpg)$", message.message_body)