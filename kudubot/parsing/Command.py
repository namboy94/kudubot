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

from typing import List


class Command:
    """
    Class that defines a framework for bot commands
    """

    def __init__(self, keyword: str, args: List[type]):
        """
        Intializes a command
        :param keyword: The keyword/command argument
        :param args: The command's argument types
        """
        self.keyword = keyword
        self.args = args

    def validate(self, keyword: str, args: List[str]) -> bool:
        """
        Method that evaluates if a given command argument and argument list
        match the command's parameters
        :param keyword: The command argument
        :param args: The rest of the arguments
        :return:
        """

        valid = True
        valid = valid and keyword.upper() == self.keyword.upper()
        valid = valid and len(args) == len(self.args)

        if valid:
            try:
                self.convert_args(args)
            except (ValueError, TypeError, IndexError):
                valid = False

        return valid

    def convert_args(self, args: List[str]) -> List[object]:
        """
        Converts a list of string arguments into a list of arguments
        converted to their correct types
        :param args: The arguments to convert
        :return: The converted arguments
        """
        converted = []
        for i in range(0, len(args)):
            arg = args[i]
            _type = self.args[i]
            converted.append(_type(arg))
        return converted
