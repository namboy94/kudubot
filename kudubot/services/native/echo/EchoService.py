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
from kudubot.services.BaseService import BaseService


class EchoService(BaseService):
    """
    Service that always replies to a user with the same message body that was
    received
    """

    def is_applicable_to(self, message: Message) -> bool:
        """
        This service is always applicable
        :param message: The message to check for applicability for
        :return: True
        """
        return True

    @staticmethod
    def define_identifier() -> str:
        """
        Defines the identifier of the service
        :return: "echo"
        """
        return "echo"

    def handle_message(self, message: Message):
        """
        Replies with the original message text
        :param message: The original message
        :return: None
        """
        self.reply("Echo", message.message_body, message)
