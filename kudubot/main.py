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

import sys
import raven
import logging
import argparse
from kudubot.metadata import version, sentry_dsn
from kudubot.exceptions import InvalidConfigException
from kudubot.connections.Connection import Connection
from kudubot.config.GlobalConfigHandler import GlobalConfigHandler


def main():  # pragma: no cover
    """
    The Main Method of the Program that starts the Connection Listener in accordance with the
    command line arguments

    :return: None
    """

    try:
        args = parse_args()

        # noinspection PyUnresolvedReferences
        if args.debug:
            logging.basicConfig(level=logging.DEBUG)
        elif args.verbose:
            logging.basicConfig(level=logging.INFO)

        # noinspection PyUnresolvedReferences
        connection = initialize_connection(args.connection.lower())

        connection.listen()
    except Exception as e:
        sentry = raven.Client(dsn=sentry_dsn, release=version)
        sentry.captureException()
        raise e


def initialize_connection(identifier: str) -> Connection:  # pragma: no cover
    """
    Loads the connection for the specified identifier
    If the connection was not found in the local configuration, the program exits.

    :param identifier: The identifier for the Connection
    :return: The Connection object
    """

    try:
        config_handler = GlobalConfigHandler()
    except InvalidConfigException as e:
        print("Loading configuration failed:")
        print(str(e))
        sys.exit(1)

    connections = config_handler.load_connections()
    services = config_handler.load_services()

    try:
        connection_type = list(filter(lambda x: x.identifier == identifier, connections))[0]
        return connection_type(services)
    except IndexError:
        print("Connection Type " + identifier + " is not implemented or imported using the config file")
        sys.exit(1)
    except InvalidConfigException as e:
        print("Connection Configuration failed:")
        print(str(e))
        sys.exit(1)


def parse_args() -> argparse.Namespace:  # pragma: no cover
    """
    Parses the Command Line Arguments using argparse

    :return: The parsed arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("connection", help="The Type of Connection to use")

    parser.add_argument("-v", "--verbose", action="store_true", help="Activates verbose output")
    parser.add_argument("-d", "--debug", action="store_true", help="Activates debug-level logging output")

    return parser.parse_args()
