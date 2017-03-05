"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of kudubot.

    kudubot makes use of various third-party python modules to serve
    information via online chat services.

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

    connection_config_location = os.path.join(config_location, "connections.conf")
    """
    The location of the connections config file, which defines the available connection types
    """

    services_config_location = os.path.join(config_location, "services.conf")
    """
    The location of the services config file, which defines the various service modules available
    """

    def __init__(self):
        """
        Initializes the ConfigHandler. A InvalidConfigException will be raised if the configuration
        could not be read. The exception message will contain more information.

        After the __init__ method is run, it can be assumed that the configuration is valid
        """

        if not os.path.isdir(self.config_location):
            raise InvalidConfigException("Configuration directory " + self.config_location + " does not exist")
        elif not os.path.isfile(self.connection_config_location):
            raise InvalidConfigException("Connection config file does not exist")
        elif not os.path.isfile(self.services_config_location):
            raise InvalidConfigException("Services config file does not exist")

    @staticmethod
    def generate_configuration(delete_old):
        """
        Generates a new, empty config location.

        :param delete_old: If set, all old config files that may exist are overwritten
        :return: None
        """

        if delete_old and os.path.isdir(GlobalConfigHandler.config_location):
            shutil.rmtree(GlobalConfigHandler.config_location)

        if not os.path.isdir(GlobalConfigHandler.config_location):
            open(GlobalConfigHandler.config_location, "w").close()
        if not os.path.isfile(GlobalConfigHandler.connection_config_location):
            open(GlobalConfigHandler.config_location, "w").close()
        if not os.path.isfile(GlobalConfigHandler.services_config_location):
            open(GlobalConfigHandler.config_location, "w").close()

    def load_connections(self) -> List[type]:
        """
        Loads all connections from the connections configuration file

        :return: A list of successfully imported Connection subclasses
        """
        return self.__load_import_config__(self.connection_config_location, Connection)

    def load_service_config(self) -> List[type]:
        """

        :return: A list of successfully imported Service subclasses
        """
        return self.__load_import_config__(self.services_config_location, Service)

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

            if line.strip().startswith("#") or line == "":
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