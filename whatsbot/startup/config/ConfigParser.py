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

import os
import platform
import re


class ConfigParser(object):
    """
    The ConfigParser class
    """

    @staticmethod
    def parse_credentials():
        """
        Parses a credential file and extracts its password and number
        :return: the number and password as tuple of strings
        """

        file = ""
        if platform.system() == "Linux":
            file = ConfigParser.open_linux_conf()
        elif platform.system() == "Windows":
            file = ConfigParser.open_windows_conf()

        number = ""
        password = ""
        for line in file:
            if line.startswith("number="):
                number = line.split("number=")[1].split("\n")[0]
            if line.startswith("password="):
                password = line.split("password=")[1].split("\n")[0]
        if number and password:
            if not re.search(r"^[0-9]+$", number):
                raise Exception("Invalid Number")
            if not re.search(r"^[^ ]+$", password):
                raise Exception("Invalid Password")
            credentials = (number, password)
            return credentials
        else:
            raise EOFError("Invalid Config")

    @staticmethod
    def open_linux_conf():
        """
        Opens the config file under Linux
        :return: the opened config file
        """
        return open(os.getenv("HOME") + "/.whatsbot/creds", 'r')

    @staticmethod
    def open_windows_conf():
        """
        Opens the config file under Windows
        :return: the opened config file
        """
        username = os.environ.get("USERNAME")
        return open("C:/Users/" + username + "/Documents/whatsbot/config.txt", 'r')
