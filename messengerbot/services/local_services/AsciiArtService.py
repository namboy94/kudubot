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
import re

from messengerbot.servicehandlers.Service import Service
from messengerbot.connection.generic.Message import Message


class AsciiArtService(Service):
    """
    The AsciiArtService Class that extends the generic Service class.
    It sends an ASCII Art image.
    """

    identifier = "ascii_art"
    """
    The identifier for this service
    """

    help_description = {"en": "/ascii\tSends an image of a specified ASCII art\n"
                              "syntax:\n"
                              "/ascii list (Lists all available images)"
                              "/ascii <image>",
                        "de": "/ascii\tSchickt ein Bild mit ASCII Kunst\n"
                              "syntax:\n"
                              "/ascii liste (Listet alle verfügbaren bilder auf)"
                              "/ascii <bild>"}
    """
    Help description for this service.
    """

    art = {
        "test": "TEST"
    }

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        image_to_show = message.message_body.lower().split(" ", 1)[1]
        if image_to_show.startswith("list"):
            reply = self.list_images()
        else:
            reply = self.art[image_to_show]

        reply_message = self.generate_reply_message(message, "ASCII Art", reply)

        if self.connection.identifier in ["whatsapp", "telegram"] and not image_to_show.startswith("list"):
            self.send_text_as_image_message(reply_message)
        else:
            self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^/ascii (list(e)?|" \
                + Service.regex_string_from_dictionary_keys([AsciiArtService.art]) + ")$"
        regex = regex.replace("+", "\+")
        return re.search(re.compile(regex), message.message_body.lower())

    def list_images(self) -> str:
        """
        Creates a list of implemented images

        :return: the list of implemented images
        """
        list_string = ""
        for image in self.art:
            list_string += image + "\n"
        return list_string.rstrip("\n")
