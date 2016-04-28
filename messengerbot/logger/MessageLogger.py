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
import os
import time

from messengerbot.connection.generic.Message import Message
from messengerbot.config.LocalConfigChecker import LocalConfigChecker


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
        if self.verbosity > 0:
            print(message.to_string())

        log_dir = os.path.join(self.log_directory, "messages")

        if message.group:
            log_dir = os.path.join(log_dir, "groups", str(message.identifier))
            log_file = os.path.join(log_dir, time.strftime("%Y-%m-%d"))
        else:
            log_dir = os.path.join(log_dir, "users", str(message.identifier))
            log_file = os.path.join(log_dir, time.strftime("%Y-%m-%d"))

        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)

        opened_log_file = open(log_file, 'a')

        if message.incoming:
            in_or_outgoing = "RECV"
        else:
            in_or_outgoing = "SENT"

        log_line = in_or_outgoing + ": " + message.message_title + ": " + message.message_body

        opened_log_file.write(log_line + "\n")
        opened_log_file.close()
