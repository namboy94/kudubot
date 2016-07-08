# coding=utf-8
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

# imports
import os
import configparser
from typing import List

from kudubot.servicehandlers.Service import Service
from kudubot.config.LocalConfigChecker import LocalConfigChecker


class ServiceConfigParser(object):
    """
    Class that parses config files to determine which services to run.
    """

    # noinspection PyTypeChecker
    @staticmethod
    def read_config(all_services: List[Service], connection_identifier: str) -> List[Service]:
        """
        Reads the config file for the specific connection type and returns a list of plugins that
        are active according to the config file

        :param all_services: A list of all available services
        :param connection_identifier: A string that identifies the type of connection used
        :return: a list of the active plugins (according to the config file)
        """
        # Check config file
        config_file = os.path.join(LocalConfigChecker.config_directory, connection_identifier + "-services")

        # Sanity check
        config = open(config_file, 'r')
        config_contents = config.read()
        config.close()

        sane = True
        if not config_contents:
            sane = False
        if "[services]" not in config_contents:
            sane = False
        for service in all_services:
            if service.identifier not in config_contents:
                sane = False

        if not sane:
            ServiceConfigParser.write_standard_config(all_services, config_file)
            return list(all_services)
        else:
            config = configparser.ConfigParser()
            config.read(config_file)
            parsed_config = dict(config.items("services"))

            active_services = []

            try:
                for service in all_services:
                    if parsed_config[service.identifier] == "1":
                        active_services.append(service)
                return active_services
            except KeyError:
                ServiceConfigParser.write_standard_config(all_services, config_file)

    # noinspection PyTypeChecker
    @staticmethod
    def write_standard_config(all_services: List[Service], config_file: str) -> None:
        """
        Writes a service config file with all services enabled

        :param all_services: A list of all available services
        :param config_file: The config file to write to
        :return: None
        """
        config = open(config_file, "w")
        config.write("[services]\n")

        for service in all_services:
            config.write(service.identifier + " = 1\n")

        config.close()
