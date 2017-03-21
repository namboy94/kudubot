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
import time
import shutil
import unittest
from kudubot.users.AddressBook import Contact
from kudubot.connections.Message import Message
from kudubot.connections.Connection import Connection
from kudubot.tests.helpers.DummyService import DummyService
from kudubot.tests.helpers.DummyConnection import DummyConnection
from kudubot.config.GlobalConfigHandler import GlobalConfigHandler
from kudubot.tests.helpers.backup_class_variables import backup_connection_variables
from kudubot.tests.helpers.backup_class_variables import backup_global_config_handler_variables


class UnitTests(unittest.TestCase):
    """
    Class that tests the Connection class
    """

    def setUp(self):
        """
        :return: None
        """
        self.restore_connection = backup_connection_variables()
        self.restore_config = backup_global_config_handler_variables()

        GlobalConfigHandler.config_location = "test-kudu"
        GlobalConfigHandler.global_connection_config_location = os.path.join("test-kudu", "connections.conf")
        GlobalConfigHandler.services_config_location = os.path.join("test-kudu", "services.conf")
        GlobalConfigHandler.data_location = os.path.join("test-kudu", "data")
        GlobalConfigHandler.specific_connection_config_location = os.path.join("test-kudu", "connection_config")
        Connection.config_file_location = os.path.join("test-kudu", "connection_config")
        Connection.database_file_location = os.path.join("test-kudu", "data")

        GlobalConfigHandler.generate_configuration(True)

    def tearDown(self):
        """
        :return: None
        """
        self.restore_connection()
        self.restore_config()
        try:
            if os.path.isdir("test-kudu"):
                shutil.rmtree("test-kudu")
        except PermissionError:
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
        connection.db.close()
