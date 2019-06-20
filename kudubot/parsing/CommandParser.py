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
from kudubot.parsing.Command import Command
from kudubot.exceptions import ParseError


class CommandParser:
    """
    A parser for bot commands
    """

    def parse(self, text: str) -> Tuple[str, Dict[str, Any]]:
        """
        Parses a command
        :param text: The text to parse
        :return: The (command, arguments)
        """

        args = self._argumentize(text)

        try:
            command_arg = args.pop(0)
            if not command_arg.startswith("/"):
                raise ParseError("Incorrect command symbol")
            command_arg = command_arg.replace("/", "")

            valid_command = None
            for command in self.commands():
                if command.validate(command_arg, args):
                    valid_command = command
                    break

            if valid_command is None:
                raise ParseError("Incorrect command name")

            else:
                return command_arg.lower(), valid_command.resolve_args(args)

        except IndexError:
            raise ParseError("Incorrect amount of arguments")

    @staticmethod
    def _argumentize(text: str):
        """
        Turns text into a list of arguments
        :param text: The text to
        :return: The list of arguments
        """
        splitted = text.split("\"")

        first_quote = False
        if splitted[0] == "":
            first_quote = True

        raw_args = []

        for i, arg in enumerate(splitted):

            is_quote = False
            if first_quote and (i % 2) == 0:
                is_quote = True
            if not first_quote and (i % 2) == 1:
                is_quote = True

            if is_quote:
                raw_args.append(arg)
            else:
                raw_args += arg.strip().split(" ")

        args = []

        for arg in raw_args:
            if arg != "":
                args.append(arg)

        return args

    @classmethod
    def help_text(cls, include_title: bool = False) -> str:
        """
        Generates a help message for the parser
        :param include_title: Whether or not to include a title
        :return: The help text for this parser
        """
        if include_title:
            help_text = "!{}\n".format(cls.name())
        else:
            help_text = ""

        divider = "  " if include_title else ""

        for command in cls.commands():
            help_text += divider + str(command) + "\n"
        return help_text.strip()

    @classmethod
    def name(cls) -> str:
        """
        :return: The name of the parser
        """
        raise NotImplementedError()

    @classmethod
    def commands(cls) -> List[Command]:
        """
        Defines the commands the parser supports
        :return: The list of commands
        """
        raise NotImplementedError()
