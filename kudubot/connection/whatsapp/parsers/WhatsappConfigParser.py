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
import sys
import configparser
from typing import Tuple

from kudubot.logger.PrintLogger import PrintLogger
from kudubot.config.LocalConfigChecker import LocalConfigChecker


class WhatsappConfigParser(object):
    """
    Class that handles the whatsapp configuration
    """

    blank_config_file_template = "[credentials]\n" \
                                 "number = \n" \
                                 "password = "

    @staticmethod
    def parse_whatsapp_config(connection_identifier: str) -> Tuple[str, str]:
        """
        Parses the Whatsapp config file and generates credentials from it

        :param connection_identifier: The identifier string of the Connection type
        :return: A credential tuple for use with the WhatsappConnection class
        """
        whatsapp_config_file = os.path.join(LocalConfigChecker.config_directory, connection_identifier)

        # First read the current file contents and perform sanity checks
        config_file = open(whatsapp_config_file, 'r')
        contents = config_file.read()
        config_file.close()

        # Is the file empty or doesn't have a credentials section? If yes, create basic template and delete current file
        if contents == "" or "[credentials]" not in contents:
            config_file = open(whatsapp_config_file, 'w')
            config_file.write(WhatsappConfigParser.blank_config_file_template)
            PrintLogger.print("Generated Whatsapp Config Template, please enter your credentials in the file.")
            PrintLogger.print("The file is located at " + whatsapp_config_file)
            sys.exit(1)

        config = configparser.ConfigParser()
        config.read(whatsapp_config_file)
        parsed_config = dict(config.items("credentials"))

        try:
            # Get the values from the config file
            return_tuple = (parsed_config["number"], parsed_config["password"])

            # Check that all elements are entered
            for element in return_tuple:
                if not element:
                    raise ValueError

            # If all went well, return the credentials
            return return_tuple

        except (KeyError, ValueError):
            PrintLogger.print("Invalid Whatsapp config file loaded. Please correct this.")
            sys.exit(1)
