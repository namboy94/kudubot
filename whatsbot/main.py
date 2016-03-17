# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsbot.

    whatsbot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsbot.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
import argparse
import sys

try:
    from layers.BotLayer import BotLayer
    from layers.BotLayerWithGUI import BotLayerWithGUI
    from startup.config.ConfigParser import ConfigParser
    from startup.installation.Installer import Installer
    from YowsupEchoStack import YowsupEchoStack

except ImportError:
    from whatsbot.layers.BotLayer import BotLayer
    from whatsbot.layers.BotLayerWithGUI import BotLayerWithGUI
    from whatsbot.startup.config.ConfigParser import ConfigParser
    from whatsbot.startup.installation.Installer import Installer
    from whatsbot.YowsupEchoStack import YowsupEchoStack

# Sets the encoding to UTF-8 when running this program in python2
if sys.version_info[0] == 2:
    # noinspection PyUnresolvedReferences
    reload(sys)
    sys.setdefaultencoding('utf8')


def main():
    """
    Starts the main loop of the program
    :return: void
    """

    # Argument Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gui", help="starts the whatsbot with a gui to disable certain plugins",
                        action="store_true")
    parser.add_argument("-r", "--register", help="Registers a new number", action="store_true")
    parser.add_argument("-i", "--install", help="Installs/updates the program", action="store_true")
    args = parser.parse_args()

    # Check if installed
    installed = Installer.is_installed()

    if not installed:
        Installer.install()
        print("Program was installed. Now use --register to register your phone number")
        sys.exit(0)
    if args.install:
        print("Program already installed")
        sys.exit(0)

    try:
        credentials = ConfigParser.parse_credentials()
    except EOFError or Exception as e:
        str(e)
        if args.register:
            number = input("Enter your number including the country code")
            cc = input("Enter your country code")
            print(number + cc)
            sys.exit(1)
        else:
            print("No valid login credentials provided in config file")
            print("Use --register to register a new number or --activate to activate a previously registered number")
            sys.exit(1)

    if args.gui:
        selected_layer = BotLayerWithGUI
    else:
        selected_layer = BotLayer

    echo_stack = YowsupEchoStack(selected_layer, credentials)
    echo_stack.start()

if __name__ == '__main__':
    main()
