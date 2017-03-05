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

import sys
import raven
import argparse
from kudubot.metadata import version, sentry_dsn
from kudubot.connections.Connection import Connection
from kudubot.config.GlobalConfigHandler import GlobalConfigHandler
from kudubot.config.ServiceConfigHandler import ServiceConfigHandler


def main():
    """
    The Main Method of the Program that starts the Connection Listener in accordance with the
    command line arguments

    :return: None
    """

    config_handler = GlobalConfigHandler()

    try:
        args = parse_args()
        connection = initialize_connection(args.connection.lower(), config_handler)
        services = ServiceConfigHandler.load_services(connection.get_identifier())
        connection.load_services(services)

        connection.listen()
    except Exception as e:
        sentry = raven.Client(dsn=sentry_dsn, release=version)
        sentry.captureException()
        raise e


def initialize_connection(identifier: str, config_handler: GlobalConfigHandler) -> Connection:
    """
    Loads the connection for the specified identifier
    If the connection was not found in the local configuration, the program exits.

    :param identifier: The identifier for the Connection
    :param config_handler: An initialized global configuration handler object
    :return: The Connection object
    """

    connections = config_handler.load_connections()

    try:
        connection_type = list(filter(lambda x: x.identifier == identifier, connections))[0]
        return connection_type()
    except IndexError:
        print("Connection Type " + identifier)
        sys.exit(1)


def parse_args() -> argparse.Namespace:
    """
    Parses the Command Line Arguments using argparse

    :return: The parsed arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("connection", help="The Type of Connection to use")
    return parser.parse_args()
