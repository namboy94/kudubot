# coding=utf-8
"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of kudubot.

    kudubot makes use of various third-party python modules to serve
    information via online chat services.

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

# imports
import os

from kudubot.config.LocalConfigChecker import LocalConfigChecker
from kudubot.connection.generic.Message import Message


class Authenticator(object):
    """
    Class that handles the permission leves for various users
    """

    admin_contact_file = ""
    """
    The contact file to use to determine the admin users
    """

    blacklisted_contact_file = ""
    """
    The contact file to use to determine the blacklisted users
    """

    def __init__(self, connection_type: str) -> None:
        """
        Creates a new Authenticator for a specific connection type

        :param connection_type: The connection type used
        :return: None
        """
        self.admin_contact_file = os.path.join(LocalConfigChecker.contacts_directory, connection_type, "admin")
        self.blacklisted_contact_file = \
            os.path.join(LocalConfigChecker.contacts_directory, connection_type, "blacklist")

    @staticmethod
    def is_in_file(user: str, contact_file: str) -> bool:
        """
        Checks if a user is in a conatct file or not

        :param user: The user to search for
        :param contact_file: the contact file to search
        :return: True if the user is in the contact file, False otherwise
        """
        contacts = open(contact_file, 'r')
        content = contacts.read()
        contacts.close()

        return user in content.split("\n")

    def is_from_admin(self, message: Message) -> bool:
        """
        Checks if a message originated from an admin user

        :param message: the message to be checked
        :return: True if admin, False if not
        """
        identifier = message.get_individual_address()

        return Authenticator.is_in_file(identifier, self.admin_contact_file)

    def is_from_blacklisted_user(self, message: Message) -> bool:
        """
        Checks if a message originated from a blacklisted user

        :param message: the message to be checked
        :return: True if blacklisted, False if not
        """
        identifier = message.get_individual_address()

        return Authenticator.is_in_file(identifier, self.blacklisted_contact_file)
