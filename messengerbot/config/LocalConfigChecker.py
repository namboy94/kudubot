# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

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

import os

from typing import List
from messengerbot.connection.generic.Connection import Connection


class LocalConfigChecker(object):
    """
    The LocalConfigVChecker that makes sure that the local config is in a correct
    state and fixes it in case it is not.
    """

    program_directory = os.path.join(os.path.expanduser("~"), ".messengerbot")
    """
    The parent directory of all config (and other local) files
    """

    resource_directory = os.path.join(program_directory, "resources")
    """
    Directory containing various resources needed by the program
    """

    config_directory = os.path.join(program_directory, "config")
    """
    Directory containing configuration files
    """

    log_directory = os.path.join(program_directory, "logs")
    """
    Directory containing program logs
    """

    contacts_directory = os.path.join(program_directory, "contacts")
    """
    Directory containing contact files
    """

    # noinspection PyTypeChecker
    @staticmethod
    def check_and_fix_config(connection_types: List[Connection]) -> None:
        """
        Checks if the config is correct and fixes it if that is not the case

        :param connection_types: A list of possible connection types to be able to check the individual
                                    connection configs as well
        :return: None
        """

        if not os.path.isdir(LocalConfigChecker.program_directory):
            os.makedirs(LocalConfigChecker.program_directory)
        if not os.path.isdir(LocalConfigChecker.resource_directory):
            os.makedirs(LocalConfigChecker.resource_directory)
        if not os.path.isdir(LocalConfigChecker.config_directory):
            os.makedirs(LocalConfigChecker.config_directory)
        if not os.path.isdir(LocalConfigChecker.log_directory):
            os.makedirs(LocalConfigChecker.log_directory)
        if not os.path.isdir(LocalConfigChecker.contacts_directory):
            os.makedirs(LocalConfigChecker.contacts_directory)

        for connection in connection_types:
            connection_logs = os.path.join(LocalConfigChecker.log_directory, connection.identifier)
            connection_config = os.path.join(LocalConfigChecker.config_directory, connection.identifier)
            connection_contacts = os.path.join(LocalConfigChecker.contacts_directory, connection.identifier)

            if not os.path.isdir(connection_logs):
                os.makedirs(connection_logs)
            if not os.path.isdir(connection_contacts):
                os.makedirs(connection_contacts)
            if not os.path.isfile(connection_config):
                open(connection_config, 'w').close()
