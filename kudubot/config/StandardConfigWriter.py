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

    @staticmethod
    def write_standard_connection_config():
        """
        Writes the standard connection configuration file

        :return: None
        """

        with open(GlobalConfigHandler.global_connection_config_location, 'w') as config:
            for connection in \
                    ["from kudubot.connections.cli.CliConnection import CliConnection",
                     "from kudubot.connections.whatsapp.WhatsappConnection import WhatsappConnection",
                     "from kudubot.connections.telegram.TelegramConnection import TelegramConnection"]:
                config.write(connection + "\n")

    @staticmethod
    def write_standard_service_config():
        """
        Writes the standard service configuration file

        :return: None
        """

        with open(GlobalConfigHandler.services_config_location, 'w') as config:
            for service in \
                    ["from kudubot.services.simple_responder.SimpleResponderService import SimpleResponderService",
                     "from kudubot.services.reminder.ReminderService import ReminderService",
                     "from kudubot.services.anime_reminder.AnimeReminderService import AnimeReminderService"]:
                config.write(service + "\n")
