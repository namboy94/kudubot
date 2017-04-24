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

from kudubot.connections.Message import Message
from kudubot.services.MultiLanguageService import MultiLanguageService


# noinspection PyAbstractClass
class HelperService(MultiLanguageService):
    """
    Service extension that allows for the automatic sending of help and syntax messages.
    Provides support for multiple languages
    """

    def define_help_message(self, language: str) -> str:
        """
        Defines the help message for the Service

        :param language: The language in which to get the help message in
        :return: The help message in the specified language
        """
        raise NotImplementedError()

    def define_syntax_description(self, language: str) -> str:
        """
        Defines the syntax description for this service.

        :param language: The language in which to get the syntax description in
        :return: The syntax description in the specified language
        """
        raise NotImplementedError()

    # noinspection PyUnusedLocal
    def define_command_name(self, language: str) -> str:
        """
        Defines the command name used to call this Service

        :param language: The language for the command name, for supporting different command names for
                         different languages
        :return: The command name for this service. Defaults to a forward slash and the Service's identifier
        """
        return "/" + self.define_identifier()

    def handle_message(self, message: Message):
        """
        Handles the help message sending. Checks if a message qualifies for a help message and then sends
        messages accordingly.

        Subclasses of the HelperService should call this method using super()

        :param message: The message to handle
        :return: None
        """

        body = message.message_body

        try:
            language = self.determine_language(message)
        except NotImplementedError:
            language = "en"

        dictionary = {
            "@help_message_title": {"en": "Help Message for " + self.identifier,
                                    "de": "Hilfnachricht für " + self.identifier},
            "@syntax_message_title": {"en": "Syntax Message for " + self.identifier,
                                      "de": "Syntaxnachricht für " + self.identifier}
        }
        help_keywords = ["help", "hilfe"]
        syntax_keywords = ["syntax"]

        if body.startswith(self.define_command_name(language)):
            body = body.split(self.define_command_name(language), 1)[1].strip()

            if body in help_keywords:
                self.reply(self.translate("@help_message_title", language, dictionary),
                           self.define_help_message(language), message)
                return
            elif body in syntax_keywords:
                self.reply(self.translate("@syntax_message_title", language, dictionary),
                           self.define_syntax_description(language), message)
                return

    def is_applicable_to(self, message: Message) -> bool:
        """
        Checks if the message is applicable to the service by checking if the command name is followed by
        the terms 'help' or 'syntax'.

        :param message: The message to analyze
        :return: True if the message is applicable, False otherwise
        """
        super().handle_message(message)

        language = self.determine_language(message)
        command = self.define_command_name(language).lower()
        dictionary = {
            "@help_command": {"en": "help",
                              "de": "hilfe"},
            "@syntax_command": {"en": "syntax",
                                "de": "syntax"}
        }

        return message.message_body.lower() in [
            command + self.translate(" @help_command", language, dictionary),
            command + self.translate(" @syntax_command", language, dictionary)
        ]
