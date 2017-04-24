"""
LICENSE:
Copyright 2017 Hermann Krumrey

This file is part of kudubot-reminder.

    kudubot-reminder is an extension module for kudubot. It provides
    a Service that can send messages at specified times.

    kudubot-reminder is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    kudubot-reminder is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with kudubot-reminder.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

import time
import logging
import datetime
from typing import List
from threading import Thread
from kudubot.entities.Message import Message
from kudubot.services.Service import Service
from kudubot.connections.Connection import Connection
from kudubot.services.reminder.parsing import parse_message
from kudubot.services.reminder.database import initialize_database, store_reminder, get_unsent_reminders,\
    mark_reminder_sent


class ReminderService(Service):
    """
    Class that implements a Service for the Kudubot framework that allows
    users to store reminder message that are then sent at a later time
    """

    logger = logging.getLogger("kudubot_reminder.ReminderService")
    """
    The logger for this class
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
        return "reminder"

    def __init__(self, connection: Connection):
        """
        Starts a background thread that perpetually searches for expired reminders
        :param connection: The connection used with this service.
        """
        super().__init__(connection)

        self.logger.info("Initializing Reminder Database Table")
        initialize_database(self.connection.db)

        self.logger.info("Starting Reminder background thread")
        background = Thread(target=self.background_loop)
        background.daemon = True
        background.start()

    def handle_message(self, message: Message):
        """
        Handles a message received by the Service

        :param message: The message to handle
        :return: None
        """

        help_message = "/remind help\n/remind <time> \"message\"\n\n<time> can be either:\n\n" \
                       "x seconds/minutes/hours\nx days/weeks/years\nYYYY-MM-DD\nYYYY-MM-DD:hh-mm-ss\nhh-mm-ss>"

        command = parse_message(message.message_body)
        target = message.sender if message.sender_group is None else message.sender_group

        if command["status"] == "help":
            self.connection.send_message(Message("Help", help_message, target, self.connection.user_contact))

        elif command["status"] == "store":
            store_reminder(self.connection.db, command["data"]["message"],
                           command["data"]["due_time"], target.database_id)
            self.connection.send_message(Message("Stored", "Reminder Stored", target, self.connection.user_contact))

    def is_applicable_to(self, message: Message) -> bool:
        """
        Checks if the Service is applicable to a message

        :param message: The message to check
        :return: True if the Service is applicable, otherwise False
        """

        applicable = parse_message(message.message_body)["status"] != "no-match"
        if applicable:
            self.logger.info("Message is applicable")
        else:
            self.logger.debug("Message is not applicable")
        return applicable

    def background_loop(self):
        """
        Perpetually checks for expiring reminders.

        :return: None
        """
        db = self.connection.get_database_connection_copy()
        while True:
            self.logger.debug("Checking reminder status")
            unsent = get_unsent_reminders(db)

            for reminder in unsent:
                if reminder["due_time"].timestamp() < datetime.datetime.utcnow().timestamp():
                    self.connection.send_message(Message("Reminder", reminder["message"],
                                                         reminder["receiver"], self.connection.user_contact))
                    mark_reminder_sent(db, reminder["id"])

            time.sleep(1)
