"""
LICENSE:
Copyright 2017 Hermann Krumrey

This file is part of kudubot-anime-reminder.

    kudubot-anime-reminder is an extension module for kudubot. It provides
    a Service that can send messages whenever a newly aired anime episode
    has aired.

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

import os
import shutil
import unittest

from kudubot_anime_reminder.tests.helpers import DummyAnimeReminderService

from kudubot.config.GlobalConfigHandler import GlobalConfigHandler
from kudubot.entities.Message import Message
from kudubot.tests.helpers.DummyConnection import DummyConnection
from kudubot.tests.helpers.backup_class_variables import prepare_class_variables_for_use
from kudubot.users.Contact import Contact


class UnitTests(unittest.TestCase):
    """
    Class that executes the unit tests
    """

    def setUp(self):
        """
        Sets up the unit tests
        :return: None
        """
        self.restore = prepare_class_variables_for_use()
        GlobalConfigHandler.generate_configuration(False)
        self.service = DummyAnimeReminderService(DummyConnection([]))

    def tearDown(self):
        """
        Restores the previous program state
        :return: None
        """
        self.restore()
        try:
            if os.path.isdir("test-kudu"):
                shutil.rmtree("test-kudu")
        except PermissionError:
            pass

    @staticmethod
    def generate_message(body) -> Message:
        """
        Generates a simple message from a body string

        :param body: The string to turn into a message
        :return: The generated Message
        """
        # noinspection PyTypeChecker
        return Message("", body, Contact(1, "A", "B"), Contact(1, "A", "B"))

    def test_valid_messages(self):
        """
        Tests the regex checker for valid messages

        :return: None
        """
        self.assertTrue(self.service.is_applicable_to(self.generate_message("/anime-remind list")))
        self.assertTrue(self.service.is_applicable_to(self.generate_message("/anime-remind subscribe \"Some Thing\"")))
        self.assertTrue(self.service.is_applicable_to(self.generate_message("/anime-remind unsubscribe \"Something\"")))

    def test_invalid_message(self):
        """
        Tests the regex checker for invalid messages

        :return: None
        """
        self.assertFalse(self.service.is_applicable_to(self.generate_message("Random Nonsense")))
        self.assertFalse(self.service.is_applicable_to(self.generate_message("/anime-remind something")))
        self.assertFalse(self.service.is_applicable_to(self.generate_message("/anime-remind list \"Some Show\"")))
        self.assertFalse(self.service.is_applicable_to(self.generate_message("/anime-remind subscribe \"Some\"Show\"")))
