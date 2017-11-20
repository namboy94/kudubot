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

import time
import unittest
from kudubot.connections.Connection import Connection
from kudubot.entities.Message import Message
from kudubot.tests.helpers.DummyConnection import DummyConnection
from kudubot.tests.helpers.DummyService import DummyService
from kudubot.tests.helpers.test_config import generate_test_environment, \
    clean_up_test_environment
from kudubot.users.AddressBook import Contact


class UnitTests(unittest.TestCase):
    """
    Class that tests the Connection class
    """

    def setUp(self):
        """
        :return: None
        """
        self.config_handler = generate_test_environment()
        self.connection = DummyConnection([], self.config_handler)

    def tearDown(self):
        """
        :return: None
        """
        clean_up_test_environment()

    def test_abstract_methods(self):
        """
        Tests if the methods of the connection class are abstract
        :return: None
        """
        for method in [(Connection.define_user_contact, 0),
                       (Connection.define_user_contact, 0),
                       (Connection.listen, 0),
                       (Connection.send_message, 1),
                       (Connection.send_image_message, 3),
                       (Connection.send_audio_message, 3),
                       (Connection.send_video_message, 3),
                       (Connection.generate_configuration, 0),
                       (Connection.load_config, 0),
                       (Connection.define_identifier, -1)]:
            try:

                # The self.connection arguments emulate the self parameter
                if method[1] == -1:
                    method[0]()
                if method[1] == 0:
                    method[0](self.connection)
                elif method[1] == 1:
                    method[0](self.connection, None)
                elif method[1] == 2:
                    method[0](self.connection, None, None)
                elif method[1] == 3:
                    method[0](self.connection, None, None, None)
                self.fail()
            except NotImplementedError:
                pass

    def test_daemon_thread_start(self):
        """
        Tests if the daemon thread is started correctly
        :return: None
        """
        class ThreadLessDummyConnection(DummyConnection):
            def listen(self):
                time.sleep(1)

        t = ThreadLessDummyConnection(
            [], self.config_handler).listen_in_separate_thread()

        self.assertTrue(t.is_alive())
        while t.is_alive():
            pass
        self.assertFalse(t.is_alive())

    # noinspection PyMethodMayBeStatic
    def test_processing_message(self):
        """
        Tests if the connection correctly processes a message
        using the services
        :return: None
        """

        class AlwaysApplicableDummyService(DummyService):
            def is_applicable_to(self, message: Message):
                return True

        user = Contact(1, "1", "1")

        connection = DummyConnection([DummyService], self.config_handler)
        connection.apply_services(Message("Test", "Body", user, user))

        connection = DummyConnection([AlwaysApplicableDummyService],
                                     self.config_handler)
        connection.apply_services(Message("Test", "Body", user, user), True)
        connection.apply_services(Message("Test", "Body", user, user), False)

        connection.db.close()
