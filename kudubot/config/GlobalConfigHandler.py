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

import os
import sys
import shutil
import logging
import importlib
from typing import List
from kudubot.services.BaseService import BaseService
from kudubot.exceptions import InvalidConfigException


class GlobalConfigHandler(object):
    """
    Class that handles the global kudubot configuration
    files located in $HOME/.kudubot
    """

    logger = logging.getLogger(__name__)
    """
    The Logger for this class
    """

    def __init__(self,
                 config_location: str = os.path.join(
                     os.path.expanduser("~"), ".kudubot")
                 ):
        """
        Initializes the ConfigHandler.
        Determines the config locations using the config_location
        parameter which defaults to a .kudubot directory in the
        user's home directory.
        The configuration may still be invalid once the object is initialized,
        call validate_config_directory() to make sure
        that the configuration is correct.

        :param config_location: The location of the config directory
        """
        self.config_location = config_location
        self.global_connection_config_location = \
            os.path.join(self.config_location, "connections.conf")
        self.services_config_location = \
            os.path.join(self.config_location, "services.conf")
        self.data_location = os.path.join(self.config_location, "data")
        self.specific_connection_config_location = \
            os.path.join(self.config_location, "connection_config")
        self.external_services_directory = \
            os.path.join(self.config_location, "external")
        self.external_services_executables_directory = \
            os.path.join(self.external_services_directory, "bin")
        self.logfile_directory = os.path.join(self.config_location, "logs")
        self.modules_directory = os.path.join(self.config_location, "modules")

    def validate_config_directory(self) -> bool:
        """
        Validates the configuration directory.
        As soon as a discrepancy is detected, the reason is logged
        and False is returned. If the configuration is valid however,
        True is returned
        :return: True if the config is valid, False otherwise
        """

        try:
            if not os.path.isdir(self.config_location):
                raise InvalidConfigException(
                    "Configuration directory " + self.config_location +
                    " does not exist")
            elif not os.path.isfile(self.global_connection_config_location):
                raise InvalidConfigException(
                    "Connection config file does not exist")
            elif not os.path.isfile(self.services_config_location):
                raise InvalidConfigException(
                    "Services config file does not exist")
            elif not os.path.isdir(self.data_location):
                raise InvalidConfigException(
                    "Data Location directory does not exist")
            elif not os.path.isdir(self.specific_connection_config_location):
                raise InvalidConfigException(
                    "Connection Configuration directory does not exist")
            elif not os.path.isdir(self.external_services_directory):
                raise InvalidConfigException(
                    "External Service directory does not exist")
            elif not os.path.isdir(
                    self.external_services_executables_directory):
                raise InvalidConfigException(
                    "External Service executable directory does not exist")
            elif not os.path.isdir(self.logfile_directory):
                raise InvalidConfigException(
                    "Log File Directory does not exist")
            elif not os.path.isdir(self.modules_directory):
                raise InvalidConfigException(
                    "Modules Directory does not exist")
            else:
                self.logger.info("Configuration successfully checked")
                return True

        except InvalidConfigException as e:
            self.logger.warning("Configuration invalid: " + e.args[0])
            return False

    def generate_configuration(self, delete_old=False):
        """
        Generates a new, empty config location.

        :param delete_old: If set, all old config files
                           that may exist are overwritten
        :return: None
        """

        if delete_old and os.path.isdir(self.config_location):
            self.logger.info("Deleting old configuration files")
            shutil.rmtree(self.config_location)

        if not os.path.isdir(self.config_location):
            self.logger.info("Creating directory " + self.config_location)
            os.makedirs(self.config_location)

        if not os.path.isfile(self.global_connection_config_location):
            self.logger.info(
                "Creating file " + self.global_connection_config_location)
            open(self.global_connection_config_location, "w").close()

        if not os.path.isfile(self.services_config_location):
            self.logger.info("Creating file " + self.services_config_location)
            open(self.services_config_location, "w").close()

        if not os.path.isdir(self.data_location):
            self.logger.info("Creating directory " + self.data_location)
            os.makedirs(self.data_location)

        if not os.path.isdir(self.specific_connection_config_location):
            self.logger.info(
                "Creating directory " +
                self.specific_connection_config_location)
            os.makedirs(self.specific_connection_config_location)

        if not os.path.isdir(self.external_services_directory):
            self.logger.info(
                "Creating directory " + self.external_services_directory)
            os.makedirs(self.external_services_directory)

        if not os.path.isdir(self.external_services_executables_directory):
            self.logger.info(
                "Creating directory " +
                self.external_services_executables_directory)
            os.makedirs(self.external_services_executables_directory)

        if not os.path.isdir(self.logfile_directory):
            self.logger.info("Creating directory " + self.logfile_directory)
            os.makedirs(self.logfile_directory)

        if not os.path.isdir(self.modules_directory):
            self.logger.info("Creating directory " + self.modules_directory)
            os.makedirs(self.modules_directory)

    def delete_service_executables(self):
        """
        Deletes all executable service files

        :return: None
        """
        shutil.rmtree(self.external_services_executables_directory)
        os.makedirs(self.external_services_executables_directory)

    def load_connections(self) -> List[type]:
        """
        Loads all connections from the connections configuration file

        :return: A list of successfully imported Connection subclasses
        """
        sys.path.append(self.modules_directory)
        from kudubot.connections.Connection import Connection

        self.logger.info("Loading connections")
        connections = self.__load_import_config__(
            self.global_connection_config_location, Connection)

        if len(connections) == 0:
            self.logger.warning("No connections loaded")

        return self.__remove_duplicate_services_or_connections__(connections)

    # noinspection PyUnresolvedReferences
    def load_services(self) -> List[type]:
        """
        Loads all Services from the services configuration file

        :return: A list of successfully imported Service subclasses
        """
        sys.path.append(self.modules_directory)
        self.logger.info("Loading Services")
        services = self.__load_import_config__(
            self.services_config_location, BaseService
        )

        if len(services) == 0:
            self.logger.warning("No services loaded")

        return self.__remove_duplicate_services_or_connections__(services)

    # noinspection PyMethodMayBeStatic
    def __handle_import_statement__(self, statement: str) -> type:
        """
        Handles an import statement string

        :param statement: The import string to parse and execute
        :return: The retrieved class or module
        """

        for special_import, import_path in {
            "NATIVE": "from kudubot.services.native.",
            "CONNECTION": "from kudubot.connections."
        }.items():

            if statement.startswith("@" + special_import):

                try:
                    class_name = statement.split("@" + special_import + " ")[1]
                except IndexError:
                    raise ImportError("Failed to import " + special_import +
                                      " module")

                module_name = class_name.rsplit("Service", 1)[0]
                module_name = module_name.rsplit("Connection", 1)[0]
                snake_case = ""

                first = True
                for char in module_name:
                    if char.isupper() and not first:
                        snake_case += "_"
                        snake_case += char.lower()
                    else:
                        snake_case += char.lower()
                        first = False

                statement = import_path + snake_case + "." + class_name
                statement += " import " + class_name

        if statement.startswith("import"):
            return importlib.import_module(statement.split("import ", 1)[1])
        else:
            statement = statement.split("from ", 1)[1]
            statement = statement.split(" import ")
            _module = importlib.import_module(statement[0])
            return getattr(_module, statement[1])

    # noinspection PyUnresolvedReferences,PyMethodMayBeStatic
    def __remove_duplicate_services_or_connections__(self, target: List[type])\
            -> List[type]:
        """
        Removes any duplicate Connections or Services from a list

        :param target: The list to remove the duplicates from
        :return: The list with duplicates removed
        """

        results = []

        for element in target:

            hitcount = 0

            for other in target:
                if other.define_identifier() == element.define_identifier():
                    hitcount += 1

            if hitcount == 1:
                results.append(element)
            else:

                exists = False

                for result in results:
                    if result.define_identifier() ==\
                            element.define_identifier():
                        exists = True
                        break

                if not exists:
                    results.append(element)

        return results

    # noinspection PyMethodMayBeStatic
    def __load_import_config__(self, file_location: str, class_type: type) \
            -> List[type]:
        """
        Reads an import config file
        (A file containing only python import statements)
        and returns a list of the successful imports.

        Imports that fail are simply ignored,
        as well as those that do not return subclasses
        of the class_type parameter.

        :param file_location: The import config file's location
        :param class_type: The class type all imports must subclass
        :return: The list of successful imports
        """

        modules = []

        with open(file_location, 'r') as config:
            content = config.read().split("\n")

        for line in content:

            self.logger.debug("Trying to import '" + line + "'")

            if line.strip().startswith("#") or line == "":
                self.logger.debug("Skipping line: " + line + "")
                continue
            else:
                try:
                    _module = self.__handle_import_statement__(line)

                    if issubclass(_module, class_type):
                        modules.append(_module)
                        self.logger.info("Import " + line + " successful")
                    else:
                        self.logger.warning(
                            "Import " + line + " is not of type " +
                            str(class_type)
                        )

                except (ImportError, AttributeError):  # Ignore invalid imports
                    self.logger.warning("Import " + line + " has failed")
                except IndexError:  # Ignore failed parsing attempts
                    self.logger.warning(
                        "Import " + line +
                        " has failed due to an error in the config file."
                    )

        return modules
