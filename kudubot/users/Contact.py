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


class Contact(object):
    """
    Class that models a contact in the connection's address book database
    """

    def __init__(self, database_id: int, display_name: str, address: str):
        """
        Initializes the contact object

        :param database_id: The contact's ID in the database
        :param display_name: The display name of the contact
        :param address: The contact's address
        """
        self.database_id = database_id
        self.display_name = display_name
        self.address = address
