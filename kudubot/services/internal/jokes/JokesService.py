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

import requests
from bs4 import BeautifulSoup
from typing import Dict
from kudubot.entities.Message import Message
from kudubot.services.HelperService import HelperService


class JokesService(HelperService):
    """
    A Service that tells jokes
    """

    @staticmethod
    def define_identifier() -> str:
        """
        :return: The service's identifier
        """
        return "jokes"

    def define_syntax_description(self, language: str) -> str:
        """
        :param language: The language to use
        :return: The syntax description for this language
        """
        return {"en": "/joke", "de": "/witz"}[language]

    def define_help_message(self, language: str) -> str:
        """
        :param language: The language to use
        :return: The help message for the specified language
        """
        return {"en": "Tells a joke", "de": "Erzählt einen Witz"}[language]

    def determine_language(self, message: Message) -> str:
        """
        Determines the language for a message
        :param message: The message to analyze
        :return: The language that this message was in
        """
        if message.message_body.lower().strip() == "/witz":
            return "de"
        else:
            return "en"

    def define_language_text(self) -> Dict[str, Dict[str, str]]:
        """
        :return: A dictionary used for translations
        """
        return {"@response_title": {"en": "Joke", "de": "Witz"}}

    def is_applicable_to(self, message: Message):
        """
        Checks if a message is applicable to this service
        :param message: The message to analyze
        :return: True if applicable, False otherwise
        """
        return message.message_body.strip().lower() in ["/joke", "/witz"]

    def handle_message(self, message: Message):
        """
        Handles an incoming message
        :param message:
        :return:
        """
        language = self.determine_language(message)

        if language == "de":
            joke = self.load_german_joke()
        elif language == "en":
            joke = self.load_english_joke()
        else:
            joke = "ERROR_LANG_NOT_FOUND"

        self.reply(self.translate("@response_title", language), joke, message)

    # noinspection PyMethodMayBeStatic
    def load_german_joke(self) -> str:
        """
        Fetches a German joke from the internet
        :return: The joke
        """
        html = requests.get("http://witze.net/zuf%C3%A4llige-witze").text
        return BeautifulSoup(html, "html.parser").select(".joke")[0].text

    # noinspection PyMethodMayBeStatic
    def load_english_joke(self) -> str:
        """
        Fetches an English joke from the internet
        :return: The joke
        """
        html = requests.get("https://www.ajokeaday.com/jokes/random")
        soup = BeautifulSoup(html.text, "html.parser")
        return soup.select("p")[1].text
