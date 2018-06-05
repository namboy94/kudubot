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
from kudubot.services.AuthenticatedService import AuthenticatedService


class AuthenticationManagerService(HelperService, AuthenticatedService):
    """
    Lets admins manage admin rights of other users and blacklist them.
    """

    @staticmethod
    def define_identifier() -> str:
        """
        Defines the identifier for this service

        :return: The service's identifier
        """
        return "authentication_manager"

    def define_command_name(self, language: str) -> str:
        """
        Defines the command prefix for the service.
        By default, '/' followed by the service identifier from
        self.define_identifier() is used.

        :param language: The language in which to define the command name
        :return: The command name in the specified language
        """
        return {
            "en": "/auth_manage",
            "de": "/auth_verwalten"
        }[language]

    def determine_language(self, message: Message) -> str:
        """
        Determines the language of a message

        :param message: The message to check for the language
        :return: The language of the message
        """
        body = message.message_body.lower()
        for language in self.supported_languages():
            if body.startswith(self.define_command_name(language)):
                return language
        return self.get_stored_language_preference(message.sender)

    def define_language_text(self) -> Dict[str, Dict[str, str]]:
        """
        Defines the dictionary used for translating strings using the
        self.reply_translated() or self.translate() methods

        The format is:

            term: {lang: value}

        :return: The dictionary for use in translating
        """
        return {
            "@{LIST}": {"en": "list", "de": "auflisten"},
            "@{ADMIN_MAKE}": {"en": "makeadmin", "de": "adminmachen"},
            "@{BLACKLIST}": {"en": "blacklist", "de": "blacklisten"},
            "@{LIST_TITLE}": {"en": "User List", "de": "Nutzerliste"},
            "@{LIST_BODY}": {"en": "User List", "de": "Nutzerliste"},
            "@{ADMIN_MAKE_TITLE}": {"en": "Admin", "de": "Administrator"},
            "@{ADMIN_MAKE_BODY}": {"en": "The user was granted administrative "
                                         "privileges.",
                                   "de": "Dem Nutzer wurden Adminrechte "
                                         "zugeschrieben."},
            "@{BLACKLIST_TITLE}": {"en": "Blacklisted", "de": "Blacklisted"},
            "@{BLACKLIST_BODY}": {"en": "The user was blacklisted",
                                  "de": "Der Nutzer wurde geblacklisted"}
        }

    def define_help_message(self, language: str) -> str:
        """
        Defines the help message of the service in various languages

        :param language: The language to use
        :return: The help message in the language
        """
        return {
            "en": "Tool for administrators to manage blacklisted and "
                  "administrative privileges.",
            "de": "Tool für Administratoren, um blackgelistete Nutzer und"
                  "administrative Rechte zu verwalten"
        }[language]

    def define_syntax_description(self, language: str) -> str:
        """
        Defines the Syntax description of the Service in various languages

        :param language: The language in which to return the syntax message
        :return: The syntax message
        """
        return {
            "en": "/auth_manage list\n"
                  "/auth_manage makeadmin <ID>\n"
                  "/auth_manage blacklist <ID>",
            "de": "/auth_verwalten auflisten\n"
                  "/auth_verwalten adminmachen <ID>\n"
                  "/auth_verwalten blacklisten <ID>"
        }[language]

    # noinspection SqlDialectInspection,SqlDialectInspection
    # noinspection SqlNoDataSourceInspection
    def handle_message(self, message: Message):
        """
        Handles an applicable message
        Checks the mode and handles accordingly

        :param message: The message to handle
        """
        args = message.message_body.lower().split(" ")
        mode = args[1]

        if mode in [self.translate("@{LIST}", language)
                    for language in self.supported_languages()]:
            list_body = "@{LIST_BODY}:\n\n"
            results = self.connection.db.execute(
                "SELECT id, display_name, address "
                "FROM address_book").fetchall()

            for result in results:
                user_id = int(result[0])
                list_body += str(user_id) + ": " + str(result[1])
                list_body += "<" + str(result[2]) + "> "

                if self.connection.authenticator.is_admin(user_id):
                    list_body += "✅"
                elif self.connection.authenticator.is_blacklisted(user_id):
                    list_body += "❌"

                list_body += "\n"

            self.reply_translated("@{LIST_TITLE}", list_body.strip(), message)

        elif mode in [self.translate("@{ADMIN_MAKE}", language)
                      for language in self.supported_languages()]:
            user_id = int(args[2])
            self.connection.authenticator.make_admin(user_id)
            self.reply_translated(
                "@{ADMIN_MAKE_TITLE}", "@{ADMIN_MAKE_BODY}", message)

        elif mode in [self.translate("@{BLACKLIST}", language)
                      for language in self.supported_languages()]:
            user_id = int(args[2])
            self.connection.authenticator.blacklist(user_id)
            self.reply_translated(
                "@{BLACKLIST_TITLE}", "@{BLACKLIST_BODY}", message)

    def is_applicable_to(self, message: Message) -> bool:
        """
        Checks if a Message is applicable to this Service

        :param message: The message to check
        :return: True if the Message is applicable, False otherwise
        """
        language = self.determine_language(message)
        print(self.define_command_name(language))
        if not self.starts_with_command_keyword(message, language):
            return False

        body = message.message_body.lower().split(" ")

        if len(body) == 2:
            print("O")
            if body[1] == self.translate("@{LIST}", language):
                return True

        elif len(body) == 3:
            print("A")
            if body[1] in [
                self.translate("@{BLACKLIST}", language),
                self.translate("@{ADMIN_MAKE}", language)
            ]:
                try:
                    int(body[2])
                    return True
                except ValueError:
                    return False

        print("I")
        return False
