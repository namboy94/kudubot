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

from typing import Dict
from kudubot.services.Service import Service
from kudubot.connections.Message import Message


# noinspection PyAbstractClass
class MultiLanguageService(Service):

    def determine_language(self, message: Message) -> str:
        raise NotImplementedError()

    def define_language_text(self) -> Dict[str, Dict[str, str]]:
        raise NotImplementedError

    # noinspection PyMethodMayBeStatic
    def define_fallback_language(self) -> str:
        return "en"

    def translate(self, text: str, language: str) -> str:

        translated = text
        language_text = self.define_language_text()

        for key in language_text:
            try:
                translated = translated.replace(key, language_text[key][language])
            except KeyError:
                translated = translated.replace(key, language_text[key][self.define_fallback_language()])

        return translated
