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

import time
import unittest
from kudubot.users.AddressBook import AddressBook, Contact
from kudubot.connections.Message import Message
from kudubot.connections.Connection import Connection
from kudubot.tests.helpers.DummyService import DummyService
from kudubot.tests.helpers.DummyConnection import DummyConnection


class UnitTests(unittest.TestCase):
    """
    Class that tests the Connection class
    """

    def setUp(self):
        """
        :return: None
        """
        pass

    def tearDown(self):
        """
        :return: None
        """
        pass

    def test_abstract_methods(self):
        """
        Tests if the methods of the connection class are abstract
        :return: None
        """

        dummy = DummyConnection([])

        for method in [(Connection.define_user_contact, 0),
                       (Connection.define_user_contact, 0),
                       (Connection.listen, 0),
                       (Connection.send_message, 1),
                       (Connection.send_image_message, 3),
                       (Connection.send_audio_message, 3),
                       (Connection.send_video_message, 3),
                       (Connection.generate_configuration, 0),
                       (Connection.load_config, 0)]:
            try:

                if method[1] == 0:
                    method[0](dummy)
                elif method[1] == 1:
                    method[0](dummy, dummy)
                elif method[1] == 2:
                    method[0](dummy, dummy, dummy)
                elif method[1] == 3:
                    method[0](dummy, dummy, dummy, dummy)
                self.fail()
            except NotImplementedError:
                pass

    def test_daemon_thread_start(self):
        """
        Tests if the daemon thread is started correctly
        :return: None
        """

        DummyConnection.listen = lambda x: time.sleep(1)
        t = DummyConnection([]).listen_in_separate_thread()

        self.assertTrue(t.is_alive())
        while t.is_alive():
            pass
        self.assertFalse(t.is_alive())

    # noinspection PyMethodMayBeStatic
    def test_processing_message(self):
        """
        Tests if the connection correctly processes a message using the services
        :return: None
        """
        user = Contact(1, "1", "1")

        connection = DummyConnection([DummyService])
        connection.apply_services(Message("Test", "Body", user, user))

        old = DummyService.is_applicable_to
        DummyService.is_applicable_to = lambda x, y: True

        connection = DummyConnection([DummyService])
        connection.apply_services(Message("Test", "Body", user, user), True)
        connection.apply_services(Message("Test", "Body", user, user), False)

        DummyService.is_applicable_to = old
