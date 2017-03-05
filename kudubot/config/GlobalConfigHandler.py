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
import logging
from typing import List
from kudubot.services.Service import Service
from kudubot.exceptions import InvalidConfigException
from kudubot.connections.Connection import Connection


class GlobalConfigHandler(object):
    """
    Class that handles the global kudubot configuration files located in $HOME/.kudubot
    """

    config_location = os.path.join(os.path.expanduser("~"), ".kudubot")
    """
    The Location of the global config directory. It is a subdirectory called .kudubot in the
    user's home directory
    """

    global_connection_config_location = os.path.join(config_location, "connections.conf")
    """
    The location of the connections config file, which defines the available connection types
    """

    services_config_location = os.path.join(config_location, "services.conf")
    """
    The location of the services config file, which defines the various service modules available
    """

    data_location = os.path.join(config_location, "data")
    """
    The location of the data directory
    """

    specific_connection_config_location = os.path.join(config_location, "connection_config")
    """
    The location of the config directory for individual connections
    """

    def __init__(self):
        """
        Initializes the ConfigHandler. A InvalidConfigException will be raised if the configuration
        could not be read. The exception message will contain more information.

        After the __init__ method is run, it can be assumed that the configuration is valid
        """

        if not os.path.isdir(self.config_location):
            raise InvalidConfigException("Configuration directory " + self.config_location + " does not exist")
        elif not os.path.isfile(self.global_connection_config_location):
            raise InvalidConfigException("Connection config file does not exist")
        elif not os.path.isfile(self.services_config_location):
            raise InvalidConfigException("Services config file does not exist")
        elif not os.path.isdir(self.data_location):
            raise InvalidConfigException("Data Location directory does not exist")
        elif not os.path.isdir(self.specific_connection_config_location):
            raise InvalidConfigException("Connection Configuration directory does not exist")

        logging.info("Configuration successfully checked")

    @staticmethod
    def generate_configuration(delete_old):
        """
        Generates a new, empty config location.

        :param delete_old: If set, all old config files that may exist are overwritten
        :return: None
        """

        if delete_old and os.path.isdir(GlobalConfigHandler.config_location):
            logging.info("Deleting old configuration files")
            shutil.rmtree(GlobalConfigHandler.config_location)

        if not os.path.isdir(GlobalConfigHandler.config_location):
            logging.info("Creating directory " + GlobalConfigHandler.config_location)
            os.makedirs(GlobalConfigHandler.config_location)

        if not os.path.isfile(GlobalConfigHandler.global_connection_config_location):
            logging.info("Creating file " + GlobalConfigHandler.global_connection_config_location)
            open(GlobalConfigHandler.global_connection_config_location, "w").close()

        if not os.path.isfile(GlobalConfigHandler.services_config_location):
            logging.info("Creating file " + GlobalConfigHandler.services_config_location)
            open(GlobalConfigHandler.services_config_location, "w").close()

        if not os.path.isdir(GlobalConfigHandler.data_location):
            logging.info("Creating directory " + GlobalConfigHandler.data_location)
            os.makedirs(GlobalConfigHandler.data_location)

        if not os.path.isdir(GlobalConfigHandler.data_location):
            logging.info("Creating directory " + GlobalConfigHandler.specific_connection_config_location)
            os.makedirs(GlobalConfigHandler.specific_connection_config_location)

    def load_connections(self) -> List[type]:
        """
        Loads all connections from the connections configuration file

        :return: A list of successfully imported Connection subclasses
        """
        logging.info("Loading connections")
        connections = self.__load_import_config__(self.global_connection_config_location, Connection)

        if len(connections) == 0:
            logging.warning("No connections loaded")

        return connections

    def load_services(self) -> List[type]:
        """
        Loads all Services from the services configuration file

        :return: A list of successfully imported Service subclasses
        """
        logging.info("Loading Services")
        services = self.__load_import_config__(self.services_config_location, Service)

        if len(services) == 0:
            logging.warning("No services loaded")

        return services

    # noinspection PyMethodMayBeStatic
    def __load_import_config__(self, file_location: str, class_type: type) -> List[type]:
        """
        Reads an import config file (A file containing only python import statements)
        and returns a list of the successful imports.

        Imports that fail are simply ignored, as well as those that do not return
        subclasses of the class_type parameter.

        :param file_location: The import config file's location
        :param class_type: The class type all imports must subclass
        :return: The list of successful imports
        """

        modules = []

        with open(file_location, 'r') as config:
            content = config.read().split("\n")

        for line in content:

            logging.debug("Trying to import '" + line + "'")

            if line.strip().startswith("#") or line == "":
                logging.debug("Skipping line: " + line + "")
                continue
            else:
                try:
                    module = __import__(line)

                    if issubclass(module, class_type):
                        modules.append(module)
                        logging.info("Import " + line + " successful")
                    else:
                        logging.warning("Import " + line + " is not of type " + str(class_type))

                except ModuleNotFoundError:  # Ignore invalid imports
                    logging.warning("Import " + line + " has failed")

        return modules
