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
from kudubot.exceptions import InvalidConfigException
from kudubot.config.GlobalConfigHandler import GlobalConfigHandler
from kudubot.tests.helpers.backup_class_variables import backup_global_config_handler_variables


class UnitTests(unittest.TestCase):
    """
    Tests the GlobalConfigHandler class
    """

    def setUp(self):
        """
        Creates a restore point for the class variables of the GlobalConfigHandler and sets these values
        to ones that make sense for the unit tests
        :return: None
        """
        self.restore = backup_global_config_handler_variables()

        GlobalConfigHandler.config_location = "test-kudu"
        GlobalConfigHandler.global_connection_config_location = os.path.join("test-kudu", "connections.conf")
        GlobalConfigHandler.services_config_location = os.path.join("test-kudu", "services.conf")
        GlobalConfigHandler.data_location = os.path.join("test-kudu", "data")
        GlobalConfigHandler.specific_connection_config_location = os.path.join("test-kudu", "connection_config")

    def tearDown(self):
        """
        Restores the class variables and deletes any temporary directories and files
        :return: None
        """
        self.restore()

        if os.path.isdir("test-kudu"):
            shutil.rmtree("test-kudu")

    def test_generating_new_config(self):
        """
        Tests if the configuration generation works as intended
        :return: None
        """
        GlobalConfigHandler.generate_configuration(True)
        self.validate_config_directory()
        GlobalConfigHandler.generate_configuration(False)
        self.validate_config_directory()

    def validate_config_directory(self):
        """
        Validates a configuration directory
        :return: None
        """

        try:
            GlobalConfigHandler()
        except InvalidConfigException:
            self.fail()

        self.assertTrue(os.path.isdir("test-kudu"))
        self.assertTrue(os.path.isfile(os.path.join("test-kudu", "services.conf")))
        self.assertTrue(os.path.isfile(os.path.join("test-kudu", "connections.conf")))
        self.assertTrue(os.path.isdir(os.path.join("test-kudu", "connection_config")))
        self.assertTrue(os.path.isdir(os.path.join("test-kudu", "data")))
