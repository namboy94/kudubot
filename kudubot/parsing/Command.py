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

from typing import List, Tuple, Dict, Any


class Command:
    """
    Class that defines a framework for bot commands
    """

    def __init__(self, keyword: str, arg_info: List[Tuple[str, Any]]):
        """
        Intializes a command
        :param keyword: The keyword/command argument
        :param arg_info: A list of tuples modelling the command arguments.
                         The first element in the tuple is the name of the
                         argument, the second one specifies the type
        """
        self.keyword = keyword
        self.arg_info = arg_info

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
        valid = valid and len(args) == len(self.arg_info)

        if valid:
            try:
                self.resolve_args(args)
            except (ValueError, TypeError, IndexError):
                valid = False

        return valid

    def resolve_args(self, args: List[str]) -> Dict[str, Any]:
        """
        Converts a list of string arguments into a dictionary of
        arguments converted to their correct types and associated with the
        appropriate keys.
        :param args: The arguments to resolve
        :return: The resolved arguments
        """
        resolved = {}

        for i in range(0, len(args)):
            arg = args[i]
            key, _type = self.arg_info[i]
            converted = _type(arg)
            resolved[key] = converted

        return resolved

    def __str__(self) -> str:
        """
        :return: A string representation of the command.
                 Useful for help messages
        """
        help_text = "/{}".format(self.keyword)
        for name, _type in self.arg_info:
            help_text += " {}<{}>".format(name, _type.__name__)
        return help_text.lower()
