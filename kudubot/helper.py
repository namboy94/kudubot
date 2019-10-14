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
import traceback
from typing import Type, Optional
from bokkichat.connection.Connection import Connection
from kudubot.Bot import Bot
from kudubot.exceptions import ConfigurationError
from puffotter.init import cli_start, argparse_add_verbosity


def cli_bot_start(
        bot_cls: Type[Bot],
        connection_cls: Type[Connection],
        sentry_dsn: Optional[str] = None,
        package_name: Optional[str] = None,
        release_name: Optional[str] = None
):
    """
    Implements a standard CLI interface for kudubot implementations
    :param bot_cls: The class of the bot to start
    :param connection_cls: The connection to use with the bot
    :param sentry_dsn: Optional sentry DSN for exception logging
    :param package_name: The name of the package
    :param release_name: Specifies a custom release name for sentry
    :return: None
    """
    def main(args: argparse.Namespace, logger: logging.Logger):
        config_path = args.custom_dir

        if args.initialize:
            if not os.path.isdir(config_path):
                os.makedirs(config_path)
            bot_cls.create_config(connection_cls, config_path)
            print("Successfully generated configuration in " + config_path)

        elif not os.path.isdir(config_path):
            logger.warning("Missing Configuration directory " + config_path)

        else:

            try:
                bot = bot_cls.load(connection_cls, config_path)
            except ConfigurationError as e:
                logger.warning("Invalid Configuration: {}".format(e))
                return
            try:
                bot.start()
            except KeyboardInterrupt as e:
                raise e
            except BaseException as e:
                bot.logger.error(
                    "Fatal Exception: {}\n{}".format(
                        e,
                        "\n".join(traceback.format_tb(e.__traceback__))
                    )
                )

    default_config_path = os.path.join(
        os.path.expanduser("~"),
        ".config/{}".format(bot_cls.name())
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("--initialize", action="store_true",
                        help="Initializes the {} bot".format(bot_cls.name()))
    parser.add_argument("--custom-dir", default=default_config_path,
                        help="Specifies a custom configuration directory")
    argparse_add_verbosity(parser)

    cli_start(
        main,
        parser,
        "Thanks for using kudubot!",
        package_name=package_name,
        sentry_dsn=sentry_dsn,
        release_name=release_name
    )
