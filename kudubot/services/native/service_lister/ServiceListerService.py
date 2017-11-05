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

from typing import List
from kudubot.entities.Message import Message
from kudubot.services.Service import Service


class ServiceListerService(Service):
    """
    This Service lists all currently active services
    """

    @staticmethod
    def define_requirements() -> List[str]:
        """
        Defines the dependencies for the Service

        :return: A list of dependencies
        """
        return []

    @staticmethod
    def define_identifier() -> str:
        """
        Defines the identifier for this service

        :return: The Service's identifier
        """
        return "service_lister"

    def is_applicable_to(self, message: Message) -> bool:
        """
        Checks if the message is applicable to this service

        :param message: The message to check
        :return: True if the message equals '/list'
        """
        return message.message_body == "/list"

    def handle_message(self, message: Message):
        """
        Sends a list of active services

        :param message: The sender message
        """
        reply = "List of active Services:\n\n"
        for service in self.connection.services:
            reply += service.define_identifier() + "\n"
        self.reply("Service List", reply, message)
