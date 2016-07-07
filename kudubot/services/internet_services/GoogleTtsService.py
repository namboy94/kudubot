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
import os
import re
from gtts import gTTS
from typing import Tuple

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message
from kudubot.config.LocalConfigChecker import LocalConfigChecker


class GoogleTtsService(Service):
    """
    The GoogleTtsService Class that extends the generic Service class.
    The service allows the user to send voice messages generated using Google's text to speech engine
    """

    identifier = "google_text_to_speech"
    """
    The identifier for this service
    """

    help_description = {"en": "/say\tA text-to-speech engine\n"
                              "syntax:\n"
                              "/say \"<text>\" [<language>]",
                        "de": "/sag\tEine text-to-speech Funktion\n"
                              "syntax:\n"
                              "/sag \"<text>\" [<sprache>]"}
    """
    Help description for this service.
    """

    supported_languages = {'af': 'Afrikaans',
                           'sq': 'Albanian',
                           'ar': 'Arabic',
                           'hy': 'Armenian',
                           'ca': 'Catalan',
                           'zh': 'Chinese',
                           'zh-cn': 'Chinese (Mandarin/China)',
                           'zh-tw': 'Chinese (Mandarin/Taiwan)',
                           'zh-yue': 'Chinese (Cantonese)',
                           'hr': 'Croatian',
                           'cs': 'Czech',
                           'da': 'Danish',
                           'nl': 'Dutch',
                           'en': 'English',
                           'en-au': 'English (Australia)',
                           'en-uk': 'English (United Kingdom)',
                           'en-us': 'English (United States)',
                           'eo': 'Esperanto',
                           'fi': 'Finnish',
                           'fr': 'French',
                           'de': 'German',
                           'el': 'Greek',
                           'ht': 'Haitian Creole',
                           'hi': 'Hindi',
                           'hu': 'Hungarian',
                           'is': 'Icelandic',
                           'id': 'Indonesian',
                           'it': 'Italian',
                           'ja': 'Japanese',
                           'ko': 'Korean',
                           'la': 'Latin',
                           'lv': 'Latvian',
                           'mk': 'Macedonian',
                           'no': 'Norwegian',
                           'pl': 'Polish',
                           'pt': 'Portuguese',
                           'pt-br': 'Portuguese (Brazil)',
                           'ro': 'Romanian',
                           'ru': 'Russian',
                           'sr': 'Serbian',
                           'sk': 'Slovak',
                           'es': 'Spanish',
                           'es-es': 'Spanish (Spain)',
                           'es-us': 'Spanish (United States)',
                           'sw': 'Swahili',
                           'sv': 'Swedish',
                           'ta': 'Tamil',
                           'th': 'Thai',
                           'tr': 'Turkish',
                           'vi': 'Vietnamese',
                           'cy': 'Welsh',
                           }
    """
    The languages supported by the text to speech engine
    """

    say_keywords = {"say": "en",
                    "sag": "de"}
    """
    Language keywords for the say command
    """

    def process_message(self, message: Message) -> None:
        """
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        speech_text, language = self.parse_user_input(message.message_body.lower())
        audio_file = self.generate_audio(speech_text, language)
        self.send_audio_message(message.address, audio_file, caption=speech_text)
        self.delete_file_after(audio_file, 5)

    @staticmethod
    def regex_check(message: Message) -> bool:
        """
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = "^/" + Service.regex_string_from_dictionary_keys([GoogleTtsService.say_keywords])
        regex += " \"[^\"]+\"( "
        regex += Service.regex_string_from_dictionary_keys([GoogleTtsService.supported_languages])
        regex += ")?$"

        return re.search(re.compile(regex), message.message_body.lower())

    @staticmethod
    def parse_user_input(user_input) -> Tuple[str, str]:
        """
        Parses the user input and determines the message text to send

        :param user_input: the input to be checked
        :return: a tuple of message text and the requested language
        """

        parts = user_input.split(" ", 1)
        say_key = parts.pop(0)
        language = GoogleTtsService.say_keywords[say_key.split("/")[1]]

        text_message = parts[0].split("\"", 2)[1]

        try:
            language = parts[0].rsplit("\" ", 1)[1]
        except IndexError:
            pass

        return text_message, language

    @staticmethod
    def generate_audio(text_string: str, language: str) -> str:
        """
        Generates an audio file using google's text to speech engine

        :param text_string: The string to be converted into speech
        :param language: The language to be used
        :return: the file path to the audio file
        """
        temp_file = os.path.join(LocalConfigChecker.program_directory, "tts_temp.mp3")
        Service.wait_until_delete(temp_file, 5)

        tts = gTTS(text=text_string, lang=language)
        tts.save(temp_file)
        return temp_file
