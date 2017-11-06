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

import sqlite3
import logging
from kudubot.users.Contact import Contact


# noinspection SqlDialectInspection,SqlNoDataSourceInspection,SqlResolve
class Authenticator(object):
    """
    Class that handles the authentication of users
    Offers the identification of users as either admin or blacklisted
    """

    logger = logging.getLogger(__name__)
    """
    The Logger for this class
    """

    def __init__(self, db: sqlite3.Connection):
        self.db = db
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS authenticator ("
            "    user_id INTEGER CONSTRAINT constraint_name PRIMARY KEY,"
            "    is_admin INTEGER NOT NULL,"
            "    is_blacklisted INTEGER NOT NULL"
            ")"
        )
        self.db.commit()
        self.logger.info("Authenticator initialized")

    def make_admin(self, contact: Contact or int,
                   database_override: sqlite3.Connection = None):
        """
        Grants admin privileges to a contact
        :param contact: The contact to grant admin privileges to
        :param database_override: Provides a different database connection.
                                  Required for use in other threads.
        """
        user_id = contact if isinstance(contact, int) else contact.database_id
        db = self.db if database_override is None else database_override
        db.execute(
            "INSERT OR REPLACE INTO authenticator "
            "(user_id, is_admin, is_blacklisted) VALUES (?, ?, ?)",
            (user_id, True, False)
        )

    def blacklist(self, contact: Contact or int,
                  database_override: sqlite3.Connection = None):
        """
        Blacklists a contact
        :param contact: The contact to blacklist
        :param database_override: Provides a different database connection.
                                  Required for use in other threads.
        """
        user_id = contact if isinstance(contact, int) else contact.database_id
        db = self.db if database_override is None else database_override
        db.execute(
            "INSERT OR REPLACE INTO authenticator "
            "(user_id, is_admin, is_blacklisted) VALUES (?, ?, ?)",
            (user_id, False, True)
        )

    def is_admin(self, contact: Contact or int,
                 database_override: sqlite3.Connection = None) -> bool:
        """
        Checks if a contact has admin privileges
        :param contact: The contact to check
        :param database_override: Provides a different database connection.
                                  Required for use in other threads.
        :return: True if the contact has admin privileges else False
        """
        if contact is None:
            return False

        user_id = contact if isinstance(contact, int) else contact.database_id
        db = self.db if database_override is None else database_override
        result = db.execute(
            "SELECT * FROM authenticator WHERE user_id=? AND is_admin=1",
            (user_id,)).fetchall()
        return len(result) == 1

    def is_blacklisted(self, contact: Contact or int,
                       database_override: sqlite3.Connection = None) -> bool:
        """
        Checks if a contact is blacklisted
        :param contact: The contact to check
        :param database_override: Provides a different database connection.
                                  Required for use in other threads.
        :return: True if the contact is blacklisted else False
        """
        if contact is None:
            return False

        user_id = contact if isinstance(contact, int) else contact.database_id
        db = self.db if database_override is None else database_override
        result = db.execute(
            "SELECT * FROM authenticator WHERE user_id=? AND is_blacklisted=1",
            (user_id,)).fetchall()
        return len(result) == 1
