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
from typing import Dict, List
from datetime import datetime
from kudubot.users.Contact import Contact


logger = logging.getLogger(__name__)
"""
The logger for this module
"""


def initialize_database(database: sqlite3.Connection):
    """
    Initializes the Database Table for the reminder service

    :param database: The database connection to use
    :return: None
    """
    # noinspection SqlNoDataSourceInspection,SqlDialectInspection
    database.execute("CREATE TABLE IF NOT EXISTS reminder ("
                     "    id INTEGER CONSTRAINT constraint_name PRIMARY KEY,"
                     "    sender_id INTEGER NOT NULL,"
                     "    msg_text VARCHAR(255) NOT NULL,"
                     "    due_time VARCHAR(255) NOT NULL,"
                     "    sent BOOLEAN NOT NULL"
                     ")")
    database.commit()


def convert_datetime_to_string(to_convert: datetime) -> str:
    """
    Converts a datetime object to a string that can be stored in the database

    :param to_convert: The datetime object to convert
    :return: The datetime as a string
    """
    return to_convert.strftime("%Y-%m-%d:%H-%M-%S")


def convert_string_to_datetime(to_convert: str) -> datetime:
    """
    Converts a string of the form '%Y-%m-%d:%H-%M-%S' to a datetime object

    :param to_convert: The string to convert
    :return: the resulting datetime object
    """
    return datetime.strptime(to_convert, "%Y-%m-%d:%H-%M-%S")


# noinspection SqlNoDataSourceInspection,SqlResolve
def get_next_id(database: sqlite3.Connection):
    """
    Fetches the next Reminder ID

    :param database: The database to use
    :return: The next highest reminder ID
    """
    return database.execute(
        "SELECT CASE WHEN COUNT(id) > 0 THEN MAX(id) ELSE 0 END AS max_id "
        "FROM reminder").fetchall()[0][0] + 1


# noinspection SqlNoDataSourceInspection,SqlResolve
def store_reminder(database: sqlite3.Connection, message: str,
                   due_time: datetime, sender_id: int):
    """
    Stores a reminder in the database

    :param database: The database Connection to use
    :param message: The message text to store
    :param due_time: The time at which the message should be sent
    :param sender_id: The initiator's id in the address book table
    :return: None
    """
    database.execute(
        "INSERT INTO reminder (id, sender_id, msg_text, due_time, sent) "
        "VALUES (?, ?, ?, ?, ?)",
        (get_next_id(database), sender_id, message,
         convert_datetime_to_string(due_time), False)
    )
    database.commit()
    logger.info("Reminder stored")


# noinspection SqlNoDataSourceInspection,SqlResolve
def get_unsent_reminders(database: sqlite3.Connection) \
        -> List[Dict[str, str or int or datetime]]:
    """
    Retrieves all unsent reminders from the database

    :param database: The database to use
    :return: A list of dictionaries that contain the reminder information
    """

    results = database.execute(
        "SELECT reminder.id, reminder.msg_text, reminder.due_time, "
        "address_book.address, address_book.id, address_book.display_name "
        "FROM reminder "
        "JOIN address_book ON reminder.sender_id = address_book.id "
        "WHERE reminder.sent = 0")
    formatted_results = []
    for result in results:
        formatted_results.append({
            "id": result[0],
            "message": result[1],
            "due_time": convert_string_to_datetime(result[2]),
            "receiver": Contact(result[4], result[5], result[3])
        })
    return formatted_results


def mark_reminder_sent(database: sqlite3.Connection, reminder_id: int):
    """
    Marks a reminder as sent

    :param database: The database connection to use
    :param reminder_id: The Reminder ID
    :return: None
    """
    logger.info("Marking reminder '" + str(reminder_id) + "' as sent.")
    # noinspection SqlNoDataSourceInspection,SqlResolve
    database.execute("UPDATE reminder SET sent=? WHERE id=?",
                     (True, reminder_id))
    database.commit()
