# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via online chat services.

    messengerbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    messengerbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsbot.  If not, see <http://www.gnu.org/licenses/>.
"""

from messengerbot.connection.generic.Connection import Connection


class Service(object):
    """
    A structure-defining interface for a Service
    """

    has_background_process = False
    """
    Attribute that tells outer classes if this particular service has a background process
    """

    connection = None

    def __init__(self, connection: Connection) -> None:
        """
        Basic Constructor for a Service. It stores the connection as a class variable.

        :param connection: The connection to be used by the service
        :return: None
        """
        self.connection = connection

    @staticmethod
    def regex_check(message: str) -> bool:
        """
        Check if the received message is a valid command for this service

        :param message: the message to be checked
        :return: True if the message is a valid command, False otherwise
        """
        raise NotImplementedError()

    def process_message(self, sender: str, message: str) -> None:
        """
        Process a message according to the service's functionality

        :param sender: the sender of the message
        :param message: the message itself
        :return: None
        """
        raise NotImplementedError()

    def background_process(self) -> None:
        """
        A method that should be run in the background if has_background_process is True

        :return: None
        """
        raise NotImplementedError()
