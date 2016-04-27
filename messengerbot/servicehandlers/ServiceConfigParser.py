# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via online chat services.

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
from typing import List

from messengerbot.servicehandlers.Service import Service


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
        # TODO implement the parser
        str(connection_identifier)
        return all_services
