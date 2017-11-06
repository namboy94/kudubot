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
class LanguageSelector(object):
    logger = logging.getLogger(__name__)
    """
    The Logger for this class
    """

    def __init__(self, db: sqlite3.Connection):
        self.db = db
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS language_preferences ("
            "    user_id INTEGER CONSTRAINT constraint_name PRIMARY KEY, "
            "    lang_pref VARCHAR(255) NOT NULL,"
            "    user_initiated INTEGER NOT NULL"
            ")"
        )
        self.db.commit()
        self.logger.info("Language Selector initialized")

    def store_language_preference(self, contact: Contact, language: str,
                                  user_initiated: bool = False):
        """
        Stores the language preference for a user in the sqlite database
        :param contact: The user for which to store the preference
        :param language: The language to store
        :param user_initiated: Flag that should be set whenever the user
                               manually requests a language store
        :return: None
        """
        fetch = self.db.execute(
            "SELECT user_initiated FROM language_preferences WHERE user_id=?",
            (contact.database_id,)
        ).fetchall()

        was_user_initiated = len(fetch) > 0 and fetch[0][0]
        if was_user_initiated and not user_initiated:
            return  # Don't overwrite user defined language

        else:
            self.db.execute(
                "INSERT OR REPLACE INTO language_preferences "
                "(user_id, lang_pref, user_initiated) VALUES (?,?,?)",
                (contact.database_id, language, user_initiated)
            )
            self.db.commit()

    def get_language_preference(self, contact: Contact, default: str = "en",
                                db: sqlite3.Connection=None) -> str:
        """
        Retrieves a language from the user's preferences in the database

        :param contact: The user to check the language preference for
        :param default: A default language value used
                        in case no entry was found
        :param db: Optionally defines which database connection to use
                   (necessary for access from other thread)
        :return: The language preferred by the user
        """
        db = db if db is not None else self.db
        result = db.execute(
            "SELECT lang_pref FROM language_preferences WHERE user_id=?",
            (contact.database_id,)
        ).fetchall()
        return default if len(result) == 0 else result[0][0]
