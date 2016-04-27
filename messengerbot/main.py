# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of messengerbot.

    messengerbot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

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

from messengerbot.config.LocalConfigChecker import LocalConfigChecker
from messengerbot.connection.email.EmailConnection import EmailConnection
# from messengerbot.connection.whatsapp.WhatsappConnection import WhatsappConnection

connections = [EmailConnection]
# WhatsappConnection]
"""
A list of possible connections
"""


def main() -> None:
    """
    The main method of the program

    :return: None
    """

    try:
        # Check for invalid amount of arguments
        if len(sys.argv) == 1:
            print("No connection type selected.")
            sys.exit(1)
        elif len(sys.argv) > 2:
            print("Too many connection types defined")
            sys.exit(1)

        # Check if the local configs are OK and if necessary fix them
        LocalConfigChecker.check_and_fix_config(connections)

        # Generate the connection
        connected = False
        for connection in connections:
            if connection.identifier == sys.argv[1]:
                connected = True
                connection.establish_connection()

        if not connected:
            print("No valid connection type selected")
            sys.argv(1)

    except KeyboardInterrupt:
        pass

    print("Thanks for using Messengerbot")


if __name__ == "__main__":
    main()
