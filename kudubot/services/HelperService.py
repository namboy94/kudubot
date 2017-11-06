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

from kudubot.entities.Message import Message
from kudubot.services.MultiLanguageService import MultiLanguageService


# noinspection PyAbstractClass
class HelperService(MultiLanguageService):
    """
    Service extension that allows for the automatic sending of
    help and syntax messages. Provides support for multiple languages
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

        :param language: The language for the command name,
                         for supporting different command names for
                         different languages
        :return: The command name for this service.
                 Defaults to a forward slash and the Service's identifier
        """
        return "/" + self.define_identifier()

    # -------------------------------------------------------------------------
    #                  _,-'/-'/                                Here be dragons!
    #  .      __,-; ,'( '/
    #   \.    `-.__`-._`:_,-._       _ , . ``
    #    `:-._,------' ` _,`--` -: `_ , ` ,' :
    #       `---..__,,--'            ` -'. -'
    # Everything below this should not be overridden by subclasses
    # -------------------------------------------------------------------------

    def handle_message_helper(self, message: Message):
        """
        Handles the help message sending.
        Checks if a message qualifies for a help message and then sends
        messages accordingly.

        :param message: The message to handle
        :return: None
        """
        body = message.message_body

        dictionary = {
            "@help_message_title":
                {"en": "Help Message for " + self.identifier,
                 "de": "Hilfnachricht für " + self.identifier},
            "@syntax_message_title":
                {"en": "Syntax Message for " + self.identifier,
                 "de": "Syntaxnachricht für " + self.identifier}
        }
        help_keywords = ["help", "hilfe"]
        syntax_keywords = ["syntax"]

        try:
            language = self.determine_language(message)
        except NotImplementedError:
            language = self.define_fallback_language()
        command_keyword = self.define_command_name(language)

        # Checks if the /help or /syntax commands were used
        # If that's the case, adjust the message text.
        for keyword in help_keywords + syntax_keywords:
            if body.lower().split(" ")[0] == "/" + keyword:
                for service in self.connection.services:
                    identifier = body.lower().split(" ")[1].strip()
                    if service.identifier == identifier:
                        if service.identifier != self.identifier:
                            return
                        else:
                            body = command_keyword + " " + keyword

        if body.startswith(self.define_command_name(language)):
            body = body.split(self.define_command_name(language), 1)[1].strip()

            if body in help_keywords:

                title = self.translate("@help_message_title",
                                       language, dictionary)
                try:
                    body = self.define_help_message(language)
                except KeyError:
                    body = "NOT_DEFINED_FOR_LANG"
                    self.logger.error("Missing language definition: " +
                                      language)

                self.reply(title, body, message)

            elif body in syntax_keywords:

                title = self.translate("@syntax_message_title",
                                       language, dictionary)
                try:
                    body = self.define_syntax_description(language)
                except KeyError:
                    body = "NOT_DEFINED_FOR_LANG"
                    self.logger.error("Missing language definition: " +
                                      language)

                self.reply(title, body, message)

    def is_applicable_to_helper(self, message: Message) -> bool:
        """
        Checks if the message is applicable to the service by checking
        if the command name is followed by the terms 'help' or 'syntax'.

        :param message: The message to analyze
        :return: True if the message is applicable, False otherwise
        """
        language = self.determine_language(message)
        command = self.define_command_name(language).lower()
        params = message.message_body.lower().split(" ")
        identifier = self.identifier

        # Needs at least 2 parameters. Command or identifier + help
        if len(params) < 2:
            return False

        dictionary = {
            "@help_command": {"en": "help",
                              "de": "hilfe"},
            "@syntax_command": {"en": "syntax",
                                "de": "syntax"}
        }

        # Check if help or syntax keyword in message text.
        # Change language accordingly
        for entry, values in dictionary.items():
            for lang, keyword in values.items():
                if params[0] == "/" + keyword:
                    language = lang
                elif params[1] == keyword:
                    language = lang

        help_command = self.translate("@help_command", language, dictionary)
        syntax_command = self.translate("@syntax_command", language,
                                        dictionary)

        if len(params) == 2 and "/" + help_command == params[0] \
                and params[1] == identifier:
            # /help identifier
            return True

        elif len(params) == 2 and "/" + syntax_command == params[0] \
                and params[1] == identifier:
            # /syntax identifier
            return True

        else:
            # /command help
            return message.message_body.lower() in [
                command + " " + help_command,
                command + " " + syntax_command
            ]

    def starts_with_command_keyword(self, message: Message, language: str,
                                    case_sensitive: bool = False) -> bool:
        """
        Checks if a message text starts with the command keyword
        defined by define_command_name()

        :param message: The message to check
        :param language: The language for which to check
        :param case_sensitive: Can be set to True to do a case-sensitive check
        :return: True if the message starts with the command name, else False
        """
        if case_sensitive:
            return message.message_body.\
                startswith(self.define_command_name(language))

        else:
            return message.message_body.lower(). \
                startswith(self.define_command_name(language).lower())
