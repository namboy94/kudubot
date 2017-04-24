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

    def define_command_name(self) -> str:
        """
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
            "@help_message_title": {"en": "Help Message for " + self.identifier},
            "@syntax_message_title": {"en": "Syntax Message for " + self.identifier}
        }

        if body.startswith(self.define_command_name()):
            body = body.split(self.define_command_name(), 1)[1].strip()

            if body == "help":
                message.reply(self.translate("@help_message_title", language, dictionary),
                              self.define_help_message(language), self.connection)
                return
            elif body == "syntax":
                message.reply(self.translate("@syntax_message_title", language, dictionary),
                              self.define_syntax_description(language), self.connection)
                return
