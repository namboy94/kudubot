# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via the online chat services.

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
import sys
import traceback
from threading import Thread

import messengerbot.metadata as metadata
from messengerbot.logger.PrintLogger import PrintLogger
from messengerbot.logger.ExceptionLogger import ExceptionLogger
from messengerbot.config.LocalConfigChecker import LocalConfigChecker
from messengerbot.connection.email.EmailConnection import EmailConnection
# from messengerbot.connection.whatsapp.WhatsappConnection import WhatsappConnection
from messengerbot.connection.telegram.TelegramConnection import TelegramConnection

connections = [EmailConnection,
               # WhatsappConnection,
               TelegramConnection]
"""
A list of possible connections
"""


def main(override: str = "", verbosity: int = 0) -> None:
    """
    The main method of the program

    :param override: Can be used to override the main method to force a specific connection to run
    :param verbosity: Can be set to define how verbose the outpt will be. Defaults to 0, no or only basic output
    :return: None
    """
    metadata.verbosity = verbosity

    PrintLogger.print("Starting program", 1)

    try:
        try:
            if not override:
                # Check for invalid amount of arguments
                if len(sys.argv) == 1:
                    PrintLogger.print("No connection type selected.")
                    sys.exit(1)
                elif len(sys.argv) > 2:
                    PrintLogger.print("Too many connection types defined")
                    sys.exit(1)

            # Check if the local configs are OK and if necessary fix them
            LocalConfigChecker.check_and_fix_config(connections)

            if override == "all" or (len(sys.argv) > 1 and sys.argv[1] == "all"):
                for connection in connections:

                    def connect():
                        """
                        Connects to a service

                        :return: None
                        """
                        try:
                            connection.establish_connection()
                        except Exception as ex:
                            stack_t = traceback.format_exc()
                            ExceptionLogger.log_exception(ex, stack_t, connection.identifier)

                    connection_thread = Thread(target=connect)
                    connection_thread.daemon = True
                    connection_thread.start()
                while True:
                    pass
            else:
                if override:
                    selected_connection = override
                else:
                    selected_connection = sys.argv[1]

                # Generate the connection
                connected = False
                for connection in connections:
                    if connection.identifier == selected_connection:
                        connected = True
                        connection.establish_connection()

                if not connected:
                    PrintLogger.print("No valid connection type selected")
                    sys.exit(1)
        except Exception as e:
            stack_trace = traceback.format_exc()
            ExceptionLogger.log_exception(e, stack_trace, "main")

    except KeyboardInterrupt:
        pass

    PrintLogger.print("Thanks for using messengerbot")
