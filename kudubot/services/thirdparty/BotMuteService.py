# coding=utf-8
"""
LICENSE:
Copyright 2016 Thomas Schmidt

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
import shutil
from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class BotMuteService(Service):
    """
    The BotMuteService Class that extends the generic Service class.
    This service mutes the bot in an effective manner.
    """

    flood_size = 21000

    identifier = "botmute"
    """
    The identifier for this service
    """

    help_description = {"en": "/botmute\tMutes the bot for an unspecified interval.\n",
                        "de": "/botmute\tStellt den Bot fur einige Zeit stumm."}
    """
    Help description for this service.
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        self.generate_reply_message(message, "WhatsApp: Bot-Muting", "BotMute requested... serving content..")
        for i in range(0, self.flood_size):
            msg = self.generate_reply_message(message, "WhatsApp: Bot-Muting in action", self.generate_loadbar(i, 20))
            self.send_text_message(msg)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        return message.message_body.lower == "/botmute"

    def generate_loadbar(self, pos, size) -> str:
        # calculate current position in loadbar
        real_pos = pos % ((size - 1) * 2)

        # generate loadbar
        output = ""
        for i in range(0, size):
            output += ("~" if i == real_pos else "=")

        return output
