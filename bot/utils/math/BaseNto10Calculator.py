# coding=utf-8
"""
Copyright 2015,2016 Hermann Krumrey

This file is part of whatsapp-bot.

    whatsapp-bot makes use of various third-party python modules to serve
    information via the online chat service Whatsapp.

    whatsapp-bot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    whatsapp-bot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with whatsapp-bot.  If not, see <http://www.gnu.org/licenses/>.
"""


class BaseNto10Calculator(object):
    """
    Class that calculates numbers of base n to decimal numbers
    """

    @staticmethod
    def any_base_to_n(base, input_string):
        """
        Turns any based number (up to 35) into a decimal number
        :param base: the base to decode
        :param input_string: the string to decode
        :return: the resulting decimal number
        """

        exponent = len(input_string) - 1
        result = 0

        try:
            for char in input_string:
                value = BaseNto10Calculator.__turn_letters_to_int__(char)
                if value > base - 1:
                    raise Exception("Invalid Number for this base")
                result += value * pow(base, exponent)
                exponent -= 1
        except Exception as e:
            return str(e)

        return str(result)

    @staticmethod
    def __turn_letters_to_int__(letter):
        """
        Turns letters into their decimal values
        :param letter: The letter to turn into an int
        :return: the resulting decimal value
        """
        try:
            return int(letter)
        except ValueError:
            if letter.lower() == "a":
                return 10
            elif letter.lower() == "b":
                return 11
            elif letter.lower() == "c":
                return 12
            elif letter.lower() == "d":
                return 13
            elif letter.lower() == "e":
                return 14
            elif letter.lower() == "f":
                return 15
            elif letter.lower() == "g":
                return 16
            elif letter.lower() == "h":
                return 17
            elif letter.lower() == "i":
                return 18
            elif letter.lower() == "j":
                return 19
            elif letter.lower() == "k":
                return 20
            elif letter.lower() == "l":
                return 21
            elif letter.lower() == "m":
                return 22
            elif letter.lower() == "n":
                return 23
            elif letter.lower() == "o":
                return 24
            elif letter.lower() == "p":
                return 25
            elif letter.lower() == "q":
                return 26
            elif letter.lower() == "r":
                return 27
            elif letter.lower() == "s":
                return 28
            elif letter.lower() == "t":
                return 29
            elif letter.lower() == "u":
                return 30
            elif letter.lower() == "v":
                return 31
            elif letter.lower() == "w":
                return 32
            elif letter.lower() == "x":
                return 33
            elif letter.lower() == "y":
                return 34
            elif letter.lower() == "z":
                return 35
