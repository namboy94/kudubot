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

from typing import Dict, List
from kudubot.users.Contact import Contact
from kudubot.entities.Message import Message
from kudubot.services.BaseService import BaseService


# noinspection PyAbstractClass
class MultiLanguageService(BaseService):
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
        Defines the dictionary with which the text is translated
        in the translate() method.
        This should be in the form of a dictionary like this:

        { key: {"language": "text_in_language", ...}, ... }

        Keep in mind that every instance of the 'key'
        value is replaced while translating

        :return: The dictionary to create translations with
        """
        raise NotImplementedError

    # noinspection PyMethodMayBeStatic
    def define_fallback_language(self) -> str:
        """
        Defines a fallback language in case a language
        is not implemented for a key.

        :return: By default, the language "en" is returned
        """
        return "en"

    # ----------------------------------------------------------------------- #
    #                  _,-'/-'/                              Here be dragons! #
    #  .      __,-; ,'( '/                                                    #
    #   \.    `-.__`-._`:_,-._       _ , . ``                                 #
    #    `:-._,------' ` _,`--` -: `_ , ` ,' :                                #
    #       `---..__,,--'            ` -'. -'                                 #
    # Everything below this should not be overridden by subclasses            #
    # -------------------------------------------------------------------------

    lang_switch_command_keywords = ["/language", "/sprache"]
    """
    List of command triggers that can be used to list or change the language
    """

    lang_switch_aliases = {
        "en": ["en", "english", "englisch"],
        "de": ["de", "deutsch", "german"]
    }
    """
    Aliases for language names in other languages
    """

    def supported_languages(self) -> List[str]:
        """
        :return: A list of languages supported by the Service
        """
        supported = []

        dictionary = self.define_language_text()
        for token in dictionary:
            for language in dictionary[token]:
                if language not in supported:
                    supported.append(language)
        return supported

    def translate(self, text: str, language: str,
                  translation_dict: Dict[str, Dict[str, str]]=None) -> str:
        """
        Translates text using the service's dictionary
        in the specified language

        :param text: The text to translate
        :param language: The language to translate into
        :param translation_dict: Can be specified to
                                 determine a custom dictionary
        :return: The translated text
        """

        translated = text
        if translation_dict is None:
            language_text = self.define_language_text()
        else:
            language_text = dict(translation_dict)

        for key in language_text:
            try:
                translated = translated.replace(
                    key, language_text[key][language]
                )
            except KeyError:
                try:
                    translated = translated.replace(
                        key,
                        language_text[key][self.define_fallback_language()]
                    )
                except KeyError:  # No English language defined
                    return text

        return translated

    def reply_translated(self, title: str, body: str, message: Message):
        """
        Provides a helper method that streamlines the process
        of replying to a message.
        Very useful for Services that send a reply immediately
        to cut down on clutter in the code

        In addition to the standard reply method,
        this method translates the text prior to sending it

        :param title: The title of the message to send
        :param body: The body of the message to send
        :param message: The message to reply to
        :return: None
        """
        language = self.determine_language(message)
        self.reply(
            self.translate(title, language),
            self.translate(body, language),
            message
        )

    # noinspection PyMethodMayBeStatic
    def is_applicable_to_multi_language(self, message: Message):
        """
        Checks if a message is applicable for a language list or change
        :param message:
        :return:
        """

        body = message.message_body.lower().strip()
        for keyword in self.lang_switch_command_keywords:
            if body.startswith(keyword + " ") or body == keyword:
                return True
        return False

    def handle_message_multi_language(self, message: Message):
        """
        Analyzes a message for the language used and stores that language
        value in the database as a preference of the user.
        Also implements the /language command which allows a user
        to view and change the current language

        :param message: The message to analyze
        :return: None
        """

        lang_switch_dict = {
            "@{title}": {
                "en": "Language Change",
                "de": "Sprachwechsel"
            },
            "@{success_message}": {
                "en": "Successfully changed language to",
                "de": "Sprache erfolgreich geändert zu"
            },
            "@{fail_message}": {
                "en": "Failed to switch to language",
                "de": "Konnte nicht Sprache wechseln zu"
            }
        }

        params = message.message_body.lower().split(" ")
        contact = message.get_direct_response_contact()

        # Example Message: '/language'
        if len(params) == 1 and params[0] in self.lang_switch_command_keywords:
            language = self.get_stored_language_preference(contact)

            self.reply(self.translate("@{title}", language, lang_switch_dict),
                       language, message)

        # Example Message: '/language english'
        elif len(params) == 2 \
                and params[0] in self.lang_switch_command_keywords:

            found_language = False
            for key in self.lang_switch_aliases:

                for alias in self.lang_switch_aliases[key]:

                    if alias == params[1]:
                        found_language = True
                        self.connection.language_selector.\
                            store_language_preference(contact, key, True)
                        break

            language = self.get_stored_language_preference(contact)
            # the new language will already be stored
            title = self.translate("@{title}", language, lang_switch_dict)

            if found_language:
                self.reply(title, self.translate("@{success_message}: " +
                                                 language, language,
                                                 lang_switch_dict), message)
            else:
                self.reply(title, self.translate("@{fail_message}: " +
                                                 params[1], language,
                                                 lang_switch_dict), message)

        else:
            language = self.determine_language(message)
            self.connection.language_selector.store_language_preference(
                message.get_direct_response_contact(), language
            )

    def get_stored_language_preference(self, contact: Contact) -> str:
        """
        Gets the stored language preference of a contact
        :param contact: The contact to get the stored language preference for
        :return: The language
        """
        return self.connection.language_selector.get_language_preference(
            contact, "en"
        )
