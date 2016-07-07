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
import time

from kudubot.logger.PrintLogger import PrintLogger
from kudubot.connection.generic.Message import Message
from kudubot.config.LocalConfigChecker import LocalConfigChecker


class MessageLogger(object):
    """
    A Message Logger that logs all in- and outgoing messages
    """

    log_directory = ""
    """
    The directory in which the logs reside in
    """

    verbosity = 0
    """
    Can be set to define different kinds of verbosity
    """

    def __init__(self, connection_type: str, verbosity: int = 0) -> None:
        """
        Constructor for the Message Logger class, which stores the log file directory.
        The directory should be different for every service.
        The verbosity can also be set, it default to 0.

        :param connection_type: The connection type to be logged
        :param verbosity: The verbosity of the logger's output
        :return: None
        """
        self.log_directory = os.path.join(LocalConfigChecker.log_directory, connection_type)
        self.verbosity = verbosity

    def log_message(self, message: Message) -> None:
        """
        Logs a message to the log files

        :param message: the message to be logged
        :return: None
        """
        PrintLogger.print(message.to_string(), 1)

        log_dir = os.path.join(self.log_directory, "messages")
        log_dir = os.path.join(log_dir, "groups") if message.group else os.path.join(log_dir, "users")

        identifier = message.address
        log_dir = os.path.join(log_dir, identifier)
        LocalConfigChecker.validate_directory(log_dir)

        log_file = os.path.join(log_dir, time.strftime("%Y-%m-%d"))

        opened_log_file = open(log_file, 'a')

        in_or_outgoing = "RECV" if message.incoming else "SENT"
        log_line = in_or_outgoing + ": " + message.message_title + ": " + message.message_body

        opened_log_file.write(log_line + "\n")
        opened_log_file.close()
