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

    def define_help_message(self) -> str:
        raise NotImplementedError()

    def define_syntax_description(self) -> str:
        raise NotImplementedError()

    def define_command_name(self) -> str:
        return "/" + self.define_identifier()

    def define_language_text(self):
        return {
            "@help_message_title": {"en": "Help Message for " + self.identifier},
            "@syntax_message_title": {"en": "Syntax Message for " + self.identifier}
        }

    def determine_language(self, message: Message):
        return "en"

    def handle_message(self, message: Message):

        body = message.message_body
        language = self.determine_language(message)

        if body.startswith(self.define_command_name()):
            body = body.split(self.define_command_name(), 1)[1].strip()

            if body == "help":
                message.reply(self.translate("@help_message_title", language),
                              self.define_help_message(), self.connection)
                return
            elif body == "syntax":
                message.reply(self.translate("@syntax_message_title", language),
                              self.define_syntax_description(), self.connection)
                return
