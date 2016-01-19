# coding=utf-8

"""
Collection of methods containing methods that convert numbers of different bases into the decimal system
@author Hermann Krumrey <hermann@krumreyh.com>
"""

class BaseNto10Calculator(object):

    """
    Turns any based number (up to 35) into a decimal number
    @:return the resulting decimal number
    """
    @staticmethod
    def anyBaseToN(base, input):

        exponent = len(input) - 1
        result = 0

        try:
            for char in input:
                value = BaseNto10Calculator.__turnLettersToInt__(char)
                if value > base - 1: raise Exception("Invalid Number for this base")
                result += value * pow(base, exponent)
                exponent -= 1
        except Exception as e:
            return str(e)

        return str(result)

    """
    Turns letters into their decimal values
    @:return the resulting decimal value
    """
    @staticmethod
    def __turnLettersToInt__(letter):

        try:
            return int(letter)
        except:
            if letter.lower() == "a": return 10
            elif letter.lower() == "b": return 11
            elif letter.lower() == "c": return 12
            elif letter.lower() == "d": return 13
            elif letter.lower() == "e": return 14
            elif letter.lower() == "f": return 15
            elif letter.lower() == "g": return 16
            elif letter.lower() == "h": return 17
            elif letter.lower() == "i": return 18
            elif letter.lower() == "j": return 19
            elif letter.lower() == "k": return 20
            elif letter.lower() == "l": return 21
            elif letter.lower() == "m": return 22
            elif letter.lower() == "n": return 23
            elif letter.lower() == "o": return 24
            elif letter.lower() == "p": return 25
            elif letter.lower() == "q": return 26
            elif letter.lower() == "r": return 27
            elif letter.lower() == "s": return 28
            elif letter.lower() == "t": return 29
            elif letter.lower() == "u": return 30
            elif letter.lower() == "v": return 31
            elif letter.lower() == "w": return 32
            elif letter.lower() == "x": return 33
            elif letter.lower() == "y": return 34
            elif letter.lower() == "z": return 35