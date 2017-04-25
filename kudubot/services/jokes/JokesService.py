"""
LICENSE:
Copyright 2015-2017 Hermann Krumrey

This file is part of kudubot.

    kudubot is a chat bot framework. It allows developers to write
    services for arbitrary chat services.

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

from typing import Dict, List
from kudubot.entities.Message import Message
from kudubot.services.HelperService import HelperService


class JokesService(HelperService):

    def define_syntax_description(self, language: str) -> str:
        return {"en": "/joke", "de": "/witz"}[language]

    def determine_language(self, message: Message) -> str:
        if message.message_body.lower().strip() == "/witz":
            return "de"
        else:
            return "en"

    @staticmethod
    def define_requirements() -> List[str]:
        return []

    def define_help_message(self, language: str) -> str:
        return {"en": "Tells a joke", "de": "Erzählt einen Witz"}[language]

    def define_language_text(self) -> Dict[str, Dict[str, str]]:
        return {}

    @staticmethod
    def define_identifier() -> str:
        return "jokes"

    def is_applicable_to(self, message: Message):
        return message.message_body.strip().lower() in ["/joke", "/witz"]

    def handle_message(self, message: Message):
        language = self.determine_language(message)

        if language == "de":
            pass
        elif language == "en":
            pass

    def load_german_joke(self) -> str:
        return "todo"

    def load_english_joke(self) -> str:
        return "todo"
