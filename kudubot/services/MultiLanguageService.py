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
    """
    Service Extension class that enables support for multiple languages
    """

    def determine_language(self, message: Message) -> str:
        """
        Checks a message object for any language indicators to determine
        in which language to reply with
        
        :param message: The message to analyze
        :return: The language key
        """
        raise NotImplementedError()

    def define_language_text(self) -> Dict[str, Dict[str, str]]:
        """
        Defines the dictionary with which the text is translated in the translate() method.
        This should be in the form of a dictionary like this:
        
        { key: {"language": "text_in_language", ...}, ... }
        
        Keep in mind that every instance of the 'key' value is replaced while translating
        
        :return: The dictionary to create translations with
        """
        raise NotImplementedError

    # noinspection PyMethodMayBeStatic
    def define_fallback_language(self) -> str:
        """
        Defines a fallback language in case a language is not implemented for a key.
        
        :return: By default, the language "en" is returned
        """
        return "en"

    def translate(self, text: str, language: str, translation_dict: Dict[str, Dict[str, str]] = None) -> str:
        """
        Translates text using the service's dictionary in the specified language
        
        :param text: The text to translate
        :param language: The language to translate into
        :param translation_dict: Can be specified to determine a custom dictionary
        :return: The translated text
        """

        translated = text
        language_text = self.define_language_text() if translation_dict is None else dict(translation_dict)

        for key in language_text:
            try:
                translated = translated.replace(key, language_text[key][language])
            except KeyError:
                translated = translated.replace(key, language_text[key][self.define_fallback_language()])

        return translated
