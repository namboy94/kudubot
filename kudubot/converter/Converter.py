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
from typing import List
from kudubot.connection.generic.Connection import Connection


class Converter(object):
    """
    Class that converts one messaging service into another
    """

    def __init__(self, destination_connection: Connection, source_connections: List[Connection]) -> None:
        """
        Constructor that sets up the converter
        :param destination_connection: the connection that handles the connection to
                the user's preferred messaging service
        :param source_connections: the connections to be forwarded to the destination connection
        :return: None
        """
        #TODO Nach der Klausurphase
