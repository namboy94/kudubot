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

import sqlite3
from typing import Dict, List
from kudubot.services.Service import Service
from kudubot.connections.Message import Message
from kudubot.connections.Connection import Connection


# noinspection PyAbstractClass,SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
class MultiLanguageService(Service):
    """
    Service Extension class that enables support for multiple languages
    """

    def __init__(self, connection: Connection):
        """
        In addition to the normal initialization of a Service, this service initializes
        its database which stores information about a user's language preferences
        :param connection: The connection which is used to communicate
        """
        super().__init__(connection)
        self.connection.db.execute("CREATE TABLE IF NOT EXISTS language_preferences ("
                                   "user_id INTEGER CONSTRAINT constraint_name PRIMARY KEY, "
                                   "lang_pref VARCHAR(255) NOT NULL,"
                                   "user_initiated INT NOT NULL"
                                   ")")
        self.connection.db.commit()

    def store_language_preference(self, user: int, language: str, user_initiated: bool = False):
        """
        Stores the language preference for a user in the sqlite database
        :param user: The user for which to store the preference
        :param language: The language to store
        :param user_initiated: Flag that should be set whenever the user manually requests a language store
        :return: None
        """
        fetch = self.connection.db.execute("SELECT user_initiated FROM language_preferences WHERE user_id=?",
                                           (user,)).fetchall()

        was_user_initiated = len(fetch) > 0 and fetch[0][0]
        if was_user_initiated and not user_initiated:
            return  # Don't overwrite user defined language

        else:
            self.connection.db.execute("INSERT OR REPLACE INTO language_preferences "
                                       "(user_id, lang_pref, user_initiated) VALUES (?,?,?)",
                                       (user, language, user_initiated))
            self.connection.db.commit()

    def get_language_preference(self, user: int, default: str = "en", db: sqlite3.Connection=None) -> str:
        """
        Retrieves a language from the user's preferences in the database

        :param user: The user to check the language preference for
        :param default: A default language value used in case no entry was found
        :param db: Optionally defines which database connection to use (necessary for access from other thread)
        :return: The language preferred by the user
        """
        db = db if db is not None else self.connection.db
        result = db.execute("SELECT lang_pref FROM language_preferences WHERE user_id=?", (user,)).fetchall()
        return default if len(result) == 0 else result[0][0]

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

    # noinspection PyMethodMayBeStatic
    def define_fallback_language(self) -> str:
        """
        Defines a fallback language in case a language is not implemented for a key.

        :return: By default, the language "en" is returned
        """
        return "en"

    def translate(self, text: str, language: str, translation_dict: Dict[str, Dict[str, str]]=None) -> str:
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

    def reply_translated(self, title: str, body: str, message: Message):
        """
        Provides a helper method that streamlines the process of replying to a message. Very useful
        for Services that send a reply immediately to cut down on clutter in the code

        In addition to the standard reply method, this method translates the text prior to sending it

        :param title: The title of the message to send
        :param body: The body of the message to send
        :param message: The message to reply to
        :return: None
        """
        language = self.get_language_preference(message.get_direct_response_contact().database_id)
        self.reply(self.translate(title, language), self.translate(body, language), message)

    def handle_message(self, message: Message):
        """
        Analyzes a message for the language used and stores that language value in the database as a preference of
        the user.
        Also implements the /language command which allows a user to view and change the current language

        :param message: The message to analyze
        :return: None
        """

        dictionary = {"@title": {"en": "Language Change",
                                 "de": "Sprachwechsel"},
                      "@success_message": {"en": "Successfully changed language to",
                                           "de": "Sprache erfolgreich geändert zu"},
                      "@fail_message": {"en": "Failed to switch to language",
                                        "de": "Konnte nicht Sprache wechseln zu"}}

        command_keywords = ["/language", "/sprache"]
        aliases = {"en": ["en", "english", "englisch"],
                   "de": ["de", "deutsch", "german"]}

        params = message.message_body.lower().split(" ")
        user_id = message.get_direct_response_contact().database_id

        if len(params) == 1 and params[0] in command_keywords:
            language = self.get_language_preference(user_id, "en")
            self.reply(self.translate("@title", language, dictionary),
                       language, message)

        if len(params) == 2 and params[0] in command_keywords:
            found_language = False
            for key in aliases:
                for alias in aliases[key]:
                    if alias == params[1]:
                        found_language = True
                        self.store_language_preference(user_id, key, True)
                        break

            language = self.get_language_preference(user_id, "en")  # the new language will already be stored
            title = self.translate("@title", language, dictionary)

            if found_language:
                self.reply(title, self.translate("@success_message: " + language, language, dictionary), message)
            else:
                self.reply(title, self.translate("@fail_message: " + params[1], language, dictionary), message)

            return

        else:

            try:
                language = self.determine_language(message)
                self.store_language_preference(message.get_direct_response_contact().database_id, language)
            except NotImplementedError:
                pass
