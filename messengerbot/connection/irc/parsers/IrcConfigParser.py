# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via the online chat services.

    messengerbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    messengerbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with messengerbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
import os
import sys
import configparser
from typing import Tuple

from messengerbot.logger.PrintLogger import PrintLogger
from messengerbot.config.LocalConfigChecker import LocalConfigChecker


class IrcParser(object):
    """
    Class that handles the irc configuration
    """

    blank_config_file_template = "[credentials]\n" \
                                 "irc_username = \n" \
                                 "irc_server = \n" \
                                 "irc_channel = "

    @staticmethod
    def parse_irc_config(connection_identifier: str) -> Tuple[str, str, str]:
        """
        Parses the IRC config file and generates credentials from it

        :param connection_identifier: The identifier string of the Connection type
        :return: the IRC username, the IRC server and the IRC channel
        """
        irc_config_file = os.path.join(LocalConfigChecker.config_directory, connection_identifier)

        # First read the current file contents and perform sanity checks
        config_file = open(irc_config_file, 'r')
        contents = config_file.read()
        config_file.close()

        # Is the file empty or doesn't have a credentials section? If yes, create basic template and delete current file
        if contents == "" or "[credentials]" not in contents:
            config_file = open(irc_config_file, 'w')
            config_file.write(IrcParser.blank_config_file_template)
            PrintLogger.print("Generated IRC Config Template, please enter your credentials in the file.")
            PrintLogger.print("The file is located at " + irc_config_file)
            sys.exit(1)

        config = configparser.ConfigParser()
        config.read(irc_config_file)
        parsed_config = dict(config.items("credentials"))

        try:
            # Get the values from the config file
            return_tuple = (parsed_config["irc_username"], parsed_config["irc_username"], parsed_config["irc_username"])

            # Check that all elements are entered
            for element in return_tuple:
                if not element:
                    raise ValueError

            # If all went well, return the credentials
            return return_tuple

        except (KeyError, ValueError):
            PrintLogger.print("Invalid IRC config file loaded. Please correct this.")
            sys.exit(1)
