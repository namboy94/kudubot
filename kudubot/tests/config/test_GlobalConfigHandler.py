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

    def assure_invalid_config_directory(self):
        """
        Makes sure that the current configuration directory is invalid
        :return: None
        """
        try:
            GlobalConfigHandler()
            self.fail()
        except InvalidConfigException:
            pass

    def test_directory_validation(self):
        """
        Tests if the global config validation works correctly and finds errors in the config structure
        :return: None
        """

        self.assure_invalid_config_directory()

        for element in ["services.conf", "connections.conf", "data", "connection_config"]:

            GlobalConfigHandler.generate_configuration(True)
            path = os.path.join("test-kudu", element)

            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)

            self.assure_invalid_config_directory()

    def test_connection_loading(self):
        """
        Tests the loading of connections

        :return: None
        """
        GlobalConfigHandler.generate_configuration(True)
        handler = GlobalConfigHandler()
        connections = handler.load_connections()
        self.assertEqual([], connections)

        with open(os.path.join("test-kudu", "connections.conf"), 'w') as f:
            f.write("from kudubot.tests.helpers.DummyConnection import DummyConnection")

        self.assertEqual(len(handler.load_connections()), 1)

    def test_service_loading(self):
        """
        Tests the loading of services

        :return: None
        """
        GlobalConfigHandler.generate_configuration(True)
        handler = GlobalConfigHandler()
        services = handler.load_services()

        self.assertEqual([], services)

        with open(os.path.join("test-kudu", "services.conf"), 'w') as f:
            f.write("from kudubot.tests.helpers.DummyService import DummyService")

        self.assertEqual(len(handler.load_services()), 1)

    def test_importing(self):
        """
        Tests the String import handler method

        :return: None
        """
        GlobalConfigHandler.generate_configuration(True)
        handler = GlobalConfigHandler()
        os_import = handler.__handle_import_statement__("import os")
        dict_import = handler.__handle_import_statement__("from typing import Dict")
        from typing import Dict

        self.assertEqual(os, os_import)
        self.assertEqual(dict_import, Dict)
