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

import logging
import sqlite3
from kudubot.users.Contact import Contact


# noinspection SqlDialectInspection,SqlNoDataSourceInspection,SqlResolve
class AddressBook(object):
    """
    Class that tracks and provides user information in the connection's database

    The address book uses the following database schema:

              | id | display_name | address | selected_language | is_admin | is_blacklisted |
    """

    schema = "CREATE TABLE IF NOT EXISTS address_book (" \
             "    id INTEGER CONSTRAINT constraint_name PRIMARY KEY," \
             "    display_name VARCHAR(255) NOT NULL," \
             "    address VARCHAR(255) NOT NULL" \
             ")"
    """
    The Address book's database schema
    """

    def __init__(self, database: sqlite3.Connection):
        """
        Initializes the address book. Makes sure that the address book's database table exists
        and has the correct schema

        :param database: The database connection to use
        """
        self.db = database
        self.db.execute(self.schema)
        self.db.commit()
        logging.info("Address Book initialized")

    def add_or_update_contact(self, contact: Contact) -> Contact:
        """
        Adds or updates a contact in the address book

        :param contact: The contact to insert/update
        :return: The contact, possibly with an altered id value (in case the contact was inserted, not updated)
        """
        # Check if the contact currently exists
        old = self.db.execute("SELECT * FROM address_book WHERE id=? OR address=?",
                              (contact.database_id, contact.address)).fetchall()

        if len(old) != 1:
            # Increment the ID
            logging.info("Address " + contact.address + " does not exist yet. Inserting into address book.")
            max_id = self.db.execute("SELECT CASE WHEN COUNT(id) > 0 THEN MAX(id) ELSE 0 END AS max_id "
                                     "FROM address_book").fetchall()[0][0]
            contact.database_id = max_id + 1
        elif contact.database_id == -1:
            contact.database_id = self.db.execute("SELECT id FROM address_book WHERE address=?",
                                                  (contact.address,)).fetchall()[0][0]

        # Insert into the database
        self.db.execute("INSERT OR REPLACE INTO address_book VALUES (?, ?, ?)",
                        (contact.database_id, contact.display_name, contact.address))
        self.db.commit()
        return contact

    def get_contact_for_address(self, address: str) -> Contact:
        """
        Generates a Contact object for an address in the address book table.

        :param address: The address to look for
        :return: The Contact object, or None if no contact was found
        """

        result = self.db.execute("SELECT * FROM address_book WHERE address=?", (address,)).fetchall()

        if len(result) != 1:
            # noinspection PyTypeChecker
            return None
        else:
            data = result[0]
            return Contact(int(data[0]), str(data[1]), str(data[2]))
