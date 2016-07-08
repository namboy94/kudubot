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


class MuterService(Service):
    """
    The MuterService Class that extends the generic Service class.
    It allows an authenticated admin user to mute and unmute a connection
    """

    identifier = "muter"
    """
    The identifier for this service
    """

    protected = True
    """
    May not be disabled
    """

    help_description = {"en": "/mute\tmutes the whatsbot (admin)\n"
                              "/unmute\tunmutes the whatsbot (admin)\n",
                        "de": "/stumm\tStellt den Bot auf lautlos (admin)\n"
                              "/laut\tHolt den Bot wieder aus dem Lautlosmodus aus (admin)\n"}
    """
    Help description for this service.
    """

    muter_keywords = {"mute": ("en", "mute"),
                      "unmute": ("en", "unmute"),
                      "stumm": ("de", "mute"),
                      "laut": ("de", "unmute")}
    """
    Keywords that trigger the muting/unmuting
    """

    unauthorized_warning = {"en": "Sorry, I can't let you do that.",
                            "de": "Sorry, das darfst du nicht."}
    """
    Reply for non-admins
    """

    not_muted_warning = {"en": "Bot is not muted",
                         "de": "Bot ist nicht stumm"}
    """
    Reply when the connection is not muted but it is attempted to unmute it
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        authenticated = self.connection.authenticator.is_from_admin(message)

        mode = message.message_body.lower().split("/")[1]
        language = self.muter_keywords[mode][0]

        mute_state = False

        if authenticated:

            if mode == "mute" and not self.connection.muted:
                mute_state = True
                reply = "🤐"
            elif mode == "mute" and self.connection.muted:
                mute_state = True
                reply = ""
            elif mode == "unmute" and self.connection.muted:
                reply = "👍🏻"
            else:
                reply = self.not_muted_warning[language]
        else:
            reply = self.unauthorized_warning[language]

        if not mute_state:
            self.connection.muted = False

        if reply:
            reply_message = self.generate_reply_message(message, "Help", reply)
            self.send_text_message(reply_message)

        self.connection.muted = mute_state

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^/("

        first = True
        for key in MuterService.muter_keywords:
            if first:
                regex += key
                first = False
            else:
                regex += "|" + key

        regex += ")$"

        return re.search(re.compile(regex), message.message_body.lower())
