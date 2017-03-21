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
from kudubot.connections.Connection import Connection
from kudubot.config.GlobalConfigHandler import GlobalConfigHandler


def backup_global_config_handler_variables() -> callable:
    """
    Backs up the GlobalConfigHandler class variables
    :return: A method to restore the GlobalConfigHandler's variables
    """

    config_location = GlobalConfigHandler.config_location
    global_connection_config_location = GlobalConfigHandler.global_connection_config_location
    services_config_location = GlobalConfigHandler.services_config_location
    data_location = GlobalConfigHandler.data_location
    specific_connection_config_location = GlobalConfigHandler.specific_connection_config_location

    def restore():
        GlobalConfigHandler.config_location = config_location
        GlobalConfigHandler.global_connection_config_location = global_connection_config_location
        GlobalConfigHandler.services_config_location = services_config_location
        GlobalConfigHandler.data_location = data_location
        GlobalConfigHandler.specific_connection_config_location = specific_connection_config_location

    return restore


def backup_connection_variables() -> callable:
    """
    Backs up the Connection class variables

    :return: A method that restores the class's initial values
    """

    database_file_location = Connection.database_file_location
    config_file_location = Connection.config_file_location

    def restore():
        Connection.database_file_location = database_file_location
        Connection.config_file_location = config_file_location

    return restore


def prepare_class_variables_for_use() -> callable:
    """
    Prepares the GlobalConfigHandler and Connection class variables for unit testing

    :return: A method to restore the class variable states
    """

    config = backup_global_config_handler_variables()
    connection = backup_connection_variables()

    GlobalConfigHandler.config_location = "test-kudu"
    GlobalConfigHandler.global_connection_config_location = os.path.join("test-kudu", "connections.conf")
    GlobalConfigHandler.services_config_location = os.path.join("test-kudu", "services.conf")
    GlobalConfigHandler.data_location = os.path.join("test-kudu", "data")
    GlobalConfigHandler.specific_connection_config_location = os.path.join("test-kudu", "connection_config")
    Connection.config_file_location = os.path.join("test-kudu", "connection_config")
    Connection.database_file_location = os.path.join("test-kudu", "data")

    def restore():
        config()
        connection()

    return restore
