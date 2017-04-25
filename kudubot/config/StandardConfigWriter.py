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


class StandardConfigWriter(object):
    """
    A config handler class that writes the standard configuration for connections
    and services into the config.
    """

    def __init__(self, config_location: str = GlobalConfigHandler().config_location):
        """
        Initializes the Standard Config Writer's configuration file locations
        :param config_location: The location of the config directory
        """
        handler = GlobalConfigHandler(config_location)
        self.connection_config = handler.global_connection_config_location
        self.service_config = handler.services_config_location

    def write_standard_connection_config(self):
        """
        Writes the standard connection configuration file

        :return: None
        """

        with open(self.connection_config, 'w') as config:
            for connection in \
                    ["from kudubot.connections.cli.CliConnection import CliConnection",
                     "from kudubot.connections.whatsapp.WhatsappConnection import WhatsappConnection",
                     "from kudubot.connections.telegram.TelegramConnection import TelegramConnection"]:
                config.write(connection + "\n")

    def write_standard_service_config(self):
        """
        Writes the standard service configuration file

        :return: None
        """

        with open(self.service_config, 'w') as config:
            for service in \
                    ["from kudubot.services.simple_responder.SimpleResponderService import SimpleResponderService",
                     "from kudubot.services.reminder.ReminderService import ReminderService",
                     "from kudubot.services.anime_reminder.AnimeReminderService import AnimeReminderService"]:
                config.write(service + "\n")
