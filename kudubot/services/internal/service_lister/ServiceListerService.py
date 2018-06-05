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

from typing import Dict
from kudubot.entities.Message import Message
from kudubot.services.HelperService import HelperService


class ServiceListerService(HelperService):
    """
    This Service lists all currently active services
    """

    @staticmethod
    def define_identifier() -> str:
        """
        Defines the identifier for this service

        :return: The service's identifier
        """
        return "service_lister"

    def define_command_name(self, language: str) -> str:
        """
        Defines the command prefix for the service.
        By default, '/' followed by the service identifier from
        self.define_identifier() is used.

        :param language: The language in which to define the command name
        :return: The command name in the specified language
        """
        return {
            "en": "/services",
            "de": "/dienste"
        }[language]

    def determine_language(self, message: Message) -> str:
        """
        Determines the language of a message

        :param message: The message to check for the language
        :return: The language of the message
        """
        try:
            return {
                "/services": "en", "/dienste": "de"
            }[message.message_body.strip().split(" ")[0]]
        except KeyError:
            return "en"

    def define_language_text(self) -> Dict[str, Dict[str, str]]:
        """
        Defines the dictionary used for translating strings using the
        self.reply_translated() or self.translate() methods

        The format is:

            term: {lang: value}

        :return: The dictionary for use in translating
        """
        return {
            "@{Title}": {"en": "Service List", "de": "Dienstliste"},
            "@{BodyTitle}": {"en": "Active Services", "de": "Aktive Dienste"}
        }

    def define_help_message(self, language: str) -> str:
        """
        Defines the help message of the service in various languages

        :param language: The language to use
        :return: The help message in the language
        """
        return {
            "en": "Use the `/services` command to get a list of active "
                  "services on this kudubot instance",
            "de": "Benutze den `/dienste` Befehl um eine Liste aktiver "
                  "Dienste auf dieser kudubot Instanz zugesendet zu bekommen."
        }[language]

    def define_syntax_description(self, language: str) -> str:
        """
        Defines the Syntax description of the Service in various languages

        :param language: The language in which to return the syntax message
        :return: The syntax message
        """
        return {
            "en": "/services",
            "de": "/dienste"
        }[language]

    def handle_message(self, message: Message):
        """
        Handles an applicable message.
        Sends a message containing the identifiers of all active services

        :param message: The message to handle
        """
        reply_msg = "@{BodyTitle}:\n\n"
        for service in self.connection.services:
            reply_msg += service.identifier + "\n"
        self.reply_translated("@{TITLE}", reply_msg.strip(), message)

    def is_applicable_to(self, message: Message) -> bool:
        """
        Checks if a Message is applicable to this Service
        Checks if the

        :param message: The message to check
        :return: True if the Message is applicable, False otherwise
        """
        return message.message_body.strip() in [
            "/dienste", "/services"
        ]
