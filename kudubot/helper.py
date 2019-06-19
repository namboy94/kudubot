"""LICENSE
Copyright 2015 Hermann Krumrey <hermann@krumreyh.com>

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
LICENSE"""

import os
import argparse
import logging
from typing import Type
from bokkichat.connection.Connection import Connection
from kudubot.Bot import Bot
from kudubot.exceptions import ConfigurationError


def cli_bot_start(bot_cls: Type[Bot], connection_cls: Type[Connection]):
    """
    Implements a standard CLI interface for kudubot implementations
    :param bot_cls: The class of the bot to start
    :param connection_cls: The connection to use with the bot
    :return: None
    """

    default_config_path = os.path.join(
        os.path.expanduser("~"),
        ".config/{}".format(bot_cls.name())
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("--initialize", action="store_true",
                        help="Initializes the {} bot".format(bot_cls.name()))
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Shows more output (INFO level)")
    parser.add_argument("--debug", "-d", action="store_true",
                        help="Shows even more output (DEBUG level)")
    parser.add_argument("--custom-dir", default=default_config_path,
                        help="Specifies a custom configuration directory")
    args = parser.parse_args()

    config_path = args.custom_dir

    if args.initialize:
        if not os.path.isdir(config_path):
            os.makedirs(config_path)
        bot_cls.create_config(connection_cls, config_path)

    if not os.path.isdir(config_path):
        print("Missing Configuration directory {}".format(config_path))
        exit(1)

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    else:
        try:
            bot = bot_cls.load(connection_cls, config_path)
            bot.start()
        except ConfigurationError as e:
            print("Invalid Configuration: {}".format(e))
