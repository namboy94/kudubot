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

from typing import List
from kudubot.connections.Message import Message


class Service(object):
    """
    A class that defines how a chat bot service integrates with a Connection
    """

    def __init__(self, connection  # Connection  (Can't import due to circular imports)
                 ):
        """
        Initializes the Service using a specified Connection

        :param connection: The connection used by this service
        """
        self.connection = connection
        self.identifier = self.define_identifier()
        self.requires = self.define_requirements()

    def is_applicable_to(self, message: Message) -> bool:
        """
        Checks if the Service is applicable to a given message

        :param message: The message to check
        :return: True if applicable, else False
        """
        raise NotImplementedError()

    def handle_message(self, message: Message):
        """
        Handles the message, provided this service is applicable to it

        :param message: The message to process
        :return: None
        """
        raise NotImplementedError()

    @staticmethod
    def define_identifier() -> str:
        """
        Defines the unique identifier for the service

        :return: The Service's identifier.
        """
        raise NotImplementedError()

    @staticmethod
    def define_requirements() -> List[str]:
        """
        Defines the requirements for the service

        :return: The required services for this Service.
        """
        raise NotImplementedError()
