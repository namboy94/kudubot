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

import os
import shutil
import unittest
from kudubot.users.Contact import Contact
from kudubot.tests.helpers.DummyConnection import DummyConnection
from kudubot.config.GlobalConfigHandler import GlobalConfigHandler
from kudubot.tests.helpers.backup_class_variables import prepare_class_variables_for_use


class UnitTests(unittest.TestCase):
    """
    Class that tests the AddressBook class
    """

    def setUp(self):
        """
        Changes the class variables for testing and creates the testing directory

        :return: None
        """
        self.restore = prepare_class_variables_for_use()
        GlobalConfigHandler.generate_configuration(False)
        self.connection = DummyConnection([])

    def tearDown(self):
        """
        Restores the class variables and deletes the testing directory

        :return: None
        """
        self.restore()
        try:
            if os.path.isdir("test-kudu"):
                shutil.rmtree("test-kudu")
        except PermissionError:
            pass

    def test_contact_operations(self):
        """
        Tests various contact operations in the addressbook.
        Uses subtest methods to make the tests a bit more readable

        :return: None
        """
        self.subtest_updating_contact()
        contact = self.connection.address_book.add_or_update_contact(Contact(-1, "ABC", "DEF"))
        self.assertEqual(contact.display_name, "ABC")
        self.assertEqual(contact.database_id, 1)
        self.assertEqual(contact.address, "DEF")

    def subtest_updating_contact(self):
        """
        Tests Updating a contact

        :return: None
        """

        contact = Contact(-1, "A", "B")
        self.subtest_adding_contact_to_addressbook(contact)

        new_contact = Contact(1, "ABC", "DEF")
        self.connection.address_book.add_or_update_contact(new_contact)

        self.assertEqual(self.connection.address_book.get_contact_for_address("B"), None)
        new_inserted = self.connection.address_book.get_contact_for_address("DEF")

        self.assertEqual(new_inserted.display_name, "ABC")
        self.assertEqual(new_inserted.database_id, 1)
        self.assertEqual(new_inserted.address, "DEF")

    def subtest_adding_contact_to_addressbook(self, contact: Contact):
        """
        Tests adding a contact to the addressbook

        :param contact: The contact to add
        :return: None
        """
        self.assertEqual(-1, contact.database_id)

        result = self.connection.address_book.add_or_update_contact(contact)
        self.assertEqual(1, result.database_id)
        self.assertEqual(contact.display_name, result.display_name)
        self.assertEqual(contact.address, result.address)

        inserted = self.connection.address_book.get_contact_for_address("B")
        self.assertEqual(inserted.display_name, result.display_name)
        self.assertEqual(inserted.database_id, result.database_id)
        self.assertEqual(inserted.address, result.address)
