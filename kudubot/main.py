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
import time
import logging
import argparse
import traceback
from kudubot import version
from kudubot.exceptions import InvalidConfigException
from kudubot.connections.Connection import Connection
from kudubot.config.GlobalConfigHandler import GlobalConfigHandler


# noinspection PyUnresolvedReferences
def main():  # pragma: no cover
    """
    The Main Method of the Program that starts the Connection Listener in
    accordance with the command line arguments
    """
    print("Kudubot Version " + version)

    args = parse_args()
    config_handler = GlobalConfigHandler(args.config)
    if not os.path.isdir(args.config):
        print(args.config)
        print("Config directory does not exist")
        sys.exit(1)

    # noinspection PyUnresolvedReferences
    try:

        initialize_logging(
            args.quiet,
            args.verbose,
            args.debug,
            config_handler,
            args.connection.lower()
        )
        connection = initialize_connection(
            args.connection.lower(),
            config_handler
        )

        connection.listen()

    except KeyboardInterrupt:
        print("\nBye")

    except BaseException as e:
        crashfile = os.path.join(
            config_handler.logfile_directory,
            "crashes"
        )
        with open(crashfile, 'a') as crashlog:
            crashlog.write("Crash@" + str(time.time()) + ": " + str(e))
            crashlog.write(traceback.format_exc())
        raise e


def initialize_connection(identifier: str,
                          config_handler: GlobalConfigHandler) \
        -> Connection:  # pragma: no cover
    """
    Loads the connection for the specified identifier
    If the connection was not found in the local configuration,
    the program exits.

    :param identifier: The identifier for the Connection
    :param config_handler: The config handler to use
                           to determine file paths etc.
    :return: The Connection object
    """

    try:
        config_handler.validate_config_directory()
    except InvalidConfigException as e:
        print("Loading configuration for service failed:")
        print(str(e))
        sys.exit(1)

    connections = config_handler.load_connections()
    services = config_handler.load_services()

    try:
        connection_type = list(filter(
            lambda x: x.define_identifier() == identifier,
            connections
        ))[0]
        return connection_type(services, config_handler)

    except IndexError:
        print("Connection Type " + identifier +
              " is not implemented or imported using the config file")
        sys.exit(1)
    except InvalidConfigException as e:
        print("Connection Configuration failed:")
        print(str(e))
        sys.exit(1)


def initialize_logging(quiet: bool, verbose: bool, debug: bool,
                       config_handler: GlobalConfigHandler,
                       connection_name: str):
    """
    Initializes the logging levels and files for the program.
    If neither the verbose or debug flags were provided,
    the logging level defaults to WARNING.
    Log files for ERROR, WARNING, DEBUG and INFO are always generated.
    If the size of a previous log file exceeds 1MB,
    the file is renamed and a new one is created.

    :param quiet: Can be set to disable all logging to the console.
                  Text logs are still done however.
    :param verbose: Flag that determines if the verbose mode
                    is switched on ~ INFO
    :param debug: Flag that determines if the debug mode is on ~ DEBUG
    :param config_handler: The config handler used to determine
                           the logging directory location
    :param connection_name: The name of the connection to log
    """

    stdout_handler = logging.StreamHandler(stream=sys.stdout)

    if debug:
        stdout_handler.setLevel(logging.DEBUG)
    elif verbose:
        stdout_handler.setLevel(logging.INFO)
    elif quiet:
        stdout_handler.setLevel(logging.CRITICAL)
    else:
        stdout_handler.setLevel(logging.WARNING)

    logfile = os.path.join(config_handler.logfile_directory,
                           connection_name + ".log")

    if os.path.isfile(logfile):
        if os.path.getsize(logfile) > 1000000:
            os.rename(logfile, logfile + "." + str(time.time()))

    logfile_handler = logging.FileHandler(logfile)
    logfile_handler.setLevel(logging.DEBUG)

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[stdout_handler, logfile_handler]
    )


def parse_args() -> argparse.Namespace:  # pragma: no cover
    """
    Parses the Command Line Arguments using argparse

    :return: The parsed arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("connection", help="The Type of Connection to use")

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Activates verbose output")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Activates debug-level logging output")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Disables all text output")
    parser.add_argument("-c", "--config",
                        default=os.path.join(os.path.expanduser("~"),
                                             ".kudubot"),
                        help="Overrides the configuration directory location")

    return parser.parse_args()
