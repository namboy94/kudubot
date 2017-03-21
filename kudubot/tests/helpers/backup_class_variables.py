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
