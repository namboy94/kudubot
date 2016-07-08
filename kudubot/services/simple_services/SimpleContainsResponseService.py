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
import random

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class SimpleContainsResponseService(Service):
    """
    The SimpleContainsResponseService Class that extends the generic Service class.
    The service responds to strings that contain specific substrings
    """

    identifier = "simple_contains_response"
    """
    The identifier for this service
    """

    help_description = {"en": "No Help Description Available",
                        "de": "Keine Hilfsbeschreibung verfügbar"}
    """
    Help description for this service. It's empty, because this service does not act on actual commands
    per say.
    """

    # noinspection PyRedundantParentheses
    case_insensitive_options = {("keks", "cookie"): ["Ich will auch Kekse!",
                                                     "Wo gibt's Kekse?",
                                                     "Kekse sind klasse!",
                                                     "Ich hab einen Gutschein für McDonald's Kekse!"],
                                ("kuchen", "cake"): ["Ich mag Kuchen",
                                                     "Marmorkuchen!",
                                                     "Kuchen gibt's bei Starbucks"],
                                ("ups", "oops", "uups"): ["Was hast du jetzt schon wieder kaputt gemacht?"],
                                ("wuerfel", "würfel"): ["Würfel sind toll",
                                                        "Du hast eine " + str(random.randint(1, 6)) + " gewürfelt!",
                                                        "https://play.google.com/store/apps/details?id=com.namibsun."
                                                        "android.dice"],
                                ("beste bot", "bester bot"): ["😘"],
                                ("doofer bot", "scheiß bot"): ["🖕🏻", "😡"],
                                ("chicken", "nuggets", "huhn", "hühnchen"): ["🐤", "Die armen Kücken!\n🐤🐤🐤"],
                                ("scheiße", "kacke"): ["💩"],
                                ("kaputt", "zerbrochen"): ["¯\\_(ツ)_/¯"],
                                ("😂", "😂😂"): ["😂😂😂"],
                                ("FC Bayern", "FCB"): ["Mia san mia!", "Deutscher Meister 2016! (+25 andere Jahre)"]}
    """
    Case-insensitive defined response conditions and responses
    """

    case_sensitive_options = {}
    """
    Case-sensitive defined response conditions and responses
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        reply = ""

        for key in SimpleContainsResponseService.case_sensitive_options:
            for ind_key in key:
                if ind_key in message.message_body:
                    reply = random.choice(SimpleContainsResponseService.case_sensitive_options[key])
        for key in SimpleContainsResponseService.case_insensitive_options:
            for ind_key in key:
                if ind_key in message.message_body.lower():
                    reply = random.choice(SimpleContainsResponseService.case_insensitive_options[key])

        reply_message = self.generate_reply_message(message, "Simple Contains Response", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        matches = 0

        for key in SimpleContainsResponseService.case_sensitive_options:
            for ind_key in key:
                if ind_key in message.message_body:
                    matches += 1
        for key in SimpleContainsResponseService.case_insensitive_options:
            for ind_key in key:
                if ind_key in message.message_body.lower():
                    matches += 1

        return matches == 1
