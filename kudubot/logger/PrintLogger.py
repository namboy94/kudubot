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
import kudubot.metadata as metadata


class PrintLogger(object):
    """
    Class that handles printing to the console
    """

    @staticmethod
    def print(string: str, verbosity_level: int = 0) -> None:
        """
        Prints a string to the console while catching OSErrors, which can occur if no terminal is available,
        for example after exiting an SSH session

        :param string: the string to print
        :param verbosity_level: after which verbosity level the string is printed
        :return: None
        """
        if metadata.verbosity >= verbosity_level:
            try:
                print(string)
            except OSError:
                pass
