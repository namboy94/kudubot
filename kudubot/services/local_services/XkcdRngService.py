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

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class XkcdRngService(Service):
    """
    The XkcdRngService Class that extends the generic Service class.
    The service returns the number 4, as illustrated in XKCD comic #221
    """

    identifier = "xkcd_rng"
    """
    The identifier for this service
    """

    help_description = {"en": "/xkcd-rng\tGenerates a guaranteed random number\n"
                              "syntax:\n"
                              "/xkcd-rng [source]\n"
                              "(the option 'source' sends the source code of the function)",
                        "de": "/xkcd-rng\tGeneriert eine gaantiert zufällige Nummer\n"
                              "/syntax:\n"
                              "/xkcd-rng [quelle]\n"
                              "(Die Option 'quelle' verschickt den Quellcode der Funktion)"}
    """
    Help description for this service.
    """

    source_keywords = {"source": "en",
                       "quelle": "de"}
    """
    Keywords for the source option
    """

    source_code = "int getRandomNumber()\n" \
                  "    return 4;    \\\\chosen by fair dice roll.\n" \
                  "                 \\\\guaranteed to be random.\n" \
                  "}"
    """
    The source code of the 'random' function
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        reply = "4" if message.message_body.lower() == "/xkcd-rng" else self.source_code

        if reply != "4":
            self.connection.last_used_language = self.source_keywords[message.message_body.lower().split(" ")[1]]

        reply_message = self.generate_reply_message(message, "XKCD RNG", reply)
        if reply != "4" and self.connection.identifier in ["telegram", "whatsapp"]:
            self.send_text_as_image_message(reply_message)
        else:
            self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^/xkcd-rng( " + Service.regex_string_from_dictionary_keys([XkcdRngService.source_keywords]) + ")?$"
        return re.search(re.compile(regex), message.message_body.lower())
